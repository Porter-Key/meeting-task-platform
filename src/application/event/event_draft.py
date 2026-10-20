from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError

from external_client.llm.structured import with_structured_output

from .conclusion_normalizer import normalize_conclusion, normalize_event, selected_option_indexes
from .event_draft_prompts import event_draft_prompt, event_grouping_prompt
from .fact_layer import build_fact_layer
from .schemas import ConclusionEventSchema, EventGroupingPlanSchema, MeetingConclusionSchema


def fallback_topic_group_indexes(topics: list[dict[str, Any]], *, target_groups: int = 3) -> list[list[int]]:
    if not topics:
        return []
    if len(topics) == 1:
        return [[0]]
    ordered = sorted(range(len(topics)), key=lambda idx: (topics[idx].get("chunk_indexes") or [10**9])[0])
    group_count = max(1, min(target_groups, len(ordered)))
    return [ordered[idx::group_count] for idx in range(group_count) if ordered[idx::group_count]]


class EventDraftService:
    def __init__(self, chat_model: Any, embeddings: Any, logger: Any | None = None) -> None:
        self.chat_model = chat_model
        self.group_planner = with_structured_output(chat_model, EventGroupingPlanSchema)
        self.event_extractor = with_structured_output(chat_model, ConclusionEventSchema)
        self.embeddings = embeddings
        self.logger = logger

    def plan_topic_groups(self, meeting: dict[str, Any], topics: list[dict[str, Any]], fact_layer: dict[str, Any] | None = None) -> list[list[int]]:
        if not topics:
            return []
        parsed = self.group_planner.invoke([
            ("system", "You group meeting Topics into 3-4 event workstreams. Return topic indexes only."),
            ("human", event_grouping_prompt(meeting, topics, fact_layer)),
        ])
        payload = EventGroupingPlanSchema.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()
        groups: list[list[int]] = []
        used: set[int] = set()
        for group in payload.get("groups") or []:
            indexes = []
            for raw in group.get("topic_indexes") or []:
                try:
                    idx = int(raw)
                except (TypeError, ValueError):
                    continue
                if 0 <= idx < len(topics) and idx not in used:
                    indexes.append(idx)
                    used.add(idx)
            if indexes:
                groups.append(indexes)
        if not groups:
            return fallback_topic_group_indexes(topics)
        if len(groups) > 4:
            head = groups[:3]
            tail = [idx for group in groups[3:] for idx in group]
            groups = head + ([tail] if tail else [])
        missing = [idx for idx in range(len(topics)) if idx not in used]
        if missing:
            target = min(range(len(groups)), key=lambda idx: len(groups[idx]))
            groups[target].extend(missing)
        return [sorted(group) for group in groups[:4]]

    def generate(self, meeting: dict[str, Any], topics: list[dict[str, Any]], chunks: list[dict[str, Any]], *, debug: bool = False, correlation_id: str | None = None) -> dict[str, Any]:
        fact_layer = build_fact_layer(meeting, chunks, max_facts=36)
        groups = self.plan_topic_groups(meeting, topics, fact_layer) if topics else []
        if debug and self.logger:
            self.logger.trace_call("EventDraftService.generate.input", input={"meeting": meeting, "topics": topics, "groups": groups}, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        if not topics:
            draft = MeetingConclusionSchema(title=f"No meeting conclusion for {meeting.get('title') or meeting.get('id')}", fact_layer=fact_layer).model_dump()
        else:
            events: list[dict[str, Any]] = []

            for group_indexes in groups:
                group_topics = [topics[idx] for idx in group_indexes]
                event = self._generate_event_with_retries(meeting, topics, group_indexes, fact_layer, correlation_id=correlation_id)
                event["source_topic_indexes"] = selected_option_indexes(event.get("source_topic_indexes"), upper_bound=len(topics)) or group_indexes
                event["source_chunk_indexes"] = sorted({idx for idx in event.get("source_chunk_indexes") or [] if str(idx).isdigit()}) or sorted(set(idx for topic_idx in group_indexes for idx in (topics[topic_idx].get("chunk_indexes") or []) if str(idx).isdigit()))
                event = normalize_event(event, topics, default_topic_indexes=group_indexes, allowed_chunk_indexes=set(idx for topic in topics for idx in (topic.get("chunk_indexes") or []) if str(idx).isdigit()))
                if event.get("title") or event.get("summary"):
                    events.append(event)
                if debug and self.logger:
                    self.logger.trace_call(
                        "EventDraftService.generate.group_output",
                        output={"group_indexes": group_indexes, "event": event, "group_topics": group_topics},
                        stage="event_debug",
                        correlation_id=correlation_id,
                        meeting_id=meeting.get("id"),
                    )
            draft = MeetingConclusionSchema(title=meeting.get("title") or "Untitled meeting conclusion", events=events, fact_layer=fact_layer).model_dump()
        draft["fact_layer"] = fact_layer
        draft = normalize_conclusion(draft, topics, fact_layer=fact_layer)
        if debug and self.logger:
            self.logger.trace_call("EventDraftService.generate.output", output=draft, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        return draft

    def _generate_event_with_retries(self, meeting: dict[str, Any], topics: list[dict[str, Any]], group_indexes: list[int], fact_layer: dict[str, Any] | None, *, correlation_id: str | None = None) -> dict[str, Any]:
        prompt = event_draft_prompt(meeting, topics, group_indexes, fact_layer)
        errors: list[str] = []
        attempts = [
            [("system", "You generate exactly one MeetingConclusion event from one topic group. Use the fact layer to avoid factual errors."), ("human", prompt)],
            [("system", "Return one complete compact JSON object matching the schema. decisions/open_issues must be arrays of objects with text. No markdown."), ("human", prompt)],
        ]
        for idx, messages in enumerate(attempts, start=1):
            try:
                parsed = self.event_extractor.invoke(messages)
                return ConclusionEventSchema.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()
            except (ValidationError, ValueError, TypeError) as exc:
                errors.append(repr(exc))
                if self.logger:
                    self.logger.warning("conclusion_event_structured_retry", "Conclusion event structured output failed; retrying", stage="event_draft", correlation_id=correlation_id, meeting_id=meeting.get("id"), attempt=idx, error=repr(exc)[:800])
        try:
            response = self.chat_model.invoke(attempts[-1])
            text = getattr(response, "content", response)
            return ConclusionEventSchema.model_validate(_parse_json_object(text if isinstance(text, str) else str(text))).model_dump()
        except Exception as exc:  # noqa: BLE001 - fallback boundary must not fail regenerate
            if self.logger:
                self.logger.error("conclusion_event_generation_failed", "Conclusion event generation failed after retries; using fallback event", stage="event_draft", correlation_id=correlation_id, meeting_id=meeting.get("id"), error=repr(exc)[:800], previous_errors=errors[-2:])
        return {"title": "Untitled event", "summary": "", "details": "", "decisions": [], "tasks": [], "open_issues": [], "sentiment": "neutral", "source_topic_indexes": group_indexes, "source_chunk_indexes": [], "keywords": [], "entities": [], "confidence": 0.0}


def _parse_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        stripped = stripped[start : end + 1]
    return json.loads(stripped)
