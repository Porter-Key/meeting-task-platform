from __future__ import annotations

from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from external_client.llm.structured import with_structured_output

from .meeting_event_prompts import meeting_event_prompt
from .schemas import MeetingEventExtractionSchema
from .topic_cluster import cluster_topics, filter_event_worthy_topics, topic_text
from .vector import safe_embed_texts


DEFAULT_EVENT_WORKERS = 64


def _selected_option_indexes(value: Any, *, upper_bound: int) -> list[int]:
    selected: list[int] = []
    for raw in value or []:
        try:
            idx = int(raw)
        except (TypeError, ValueError):
            continue
        if 0 <= idx < upper_bound and idx not in selected:
            selected.append(idx)
    return selected


def _select_event_topics(item: dict[str, Any], topic_group: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected_indexes = _selected_option_indexes(item.get("source_topic_indexes"), upper_bound=len(topic_group))
    return [topic_group[idx] for idx in selected_indexes]


def _self_text(item: dict[str, Any]) -> str:
    parts = [
        f"Title: {item.get('title') or ''}",
        f"Description: {item.get('description') or ''}",
        f"Background: {item.get('background') or ''}",
        f"Business object: {item.get('business_object') or ''}",
        f"Business process: {item.get('business_process') or ''}",
        f"Platform/system: {item.get('platform_or_system') or ''}",
        f"Decision/action: {item.get('decision_or_action') or ''}",
        f"Current state: {item.get('current_state') or ''}",
        f"Latest progress: {item.get('latest_progress') or ''}",
        f"Why it matters: {item.get('why_it_matters') or ''}",
        f"Actions: {'; '.join(item.get('actions') or [])}",
    ]
    return "\n".join(part for part in parts if part.split(":", 1)[-1].strip())


class MeetingEventService:
    def __init__(self, chat_model: Any, embeddings: Any, logger: Any | None = None) -> None:
        self.extractor = with_structured_output(chat_model, MeetingEventExtractionSchema)
        self.embeddings = embeddings
        self.max_workers = DEFAULT_EVENT_WORKERS
        self.logger = logger

    def generate_meeting_events(self, meeting: dict[str, Any], topics: list[dict[str, Any]], *, debug: bool = False, correlation_id: str | None = None) -> list[dict[str, Any]]:
        if debug and self.logger:
            self.logger.trace_call("MeetingEventService.generate_meeting_events.input", input={"meeting": meeting, "topics": topics}, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        topics = filter_event_worthy_topics(topics)
        groups = cluster_topics(self.embeddings, topics)
        if debug and self.logger:
            self.logger.trace_call("MeetingEventService.cluster_topics.output", output=groups, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        meeting_events: list[dict[str, Any]] = []
        def extract_group(group: dict[str, Any]) -> list[dict[str, Any]]:
            topic_group = [topics[idx] for idx in group["topic_indexes"]]
            if debug and self.logger:
                self.logger.trace_call("MeetingEventService.extract_group.input", input={"group": group, "topic_group": topic_group}, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
            parsed = self.extractor.invoke([("system", "You generate MeetingEvents from Topics only."), ("human", meeting_event_prompt(meeting, topic_group))])
            payload = MeetingEventExtractionSchema.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()
            extracted = []
            for item in payload.get("meeting_events") or []:
                selected_topics = _select_event_topics(item, topic_group)
                if not selected_topics:
                    continue
                item["source_topic_indexes"] = _selected_option_indexes(item.get("source_topic_indexes"), upper_bound=len(topic_group))
                item["topic_ids"] = [topic["local_topic_id"] for topic in selected_topics if topic.get("local_topic_id")]
                item["local_topic_titles"] = [topic.get("title", "") for topic in selected_topics if topic.get("title")]
                item["chunk_indexes"] = sorted({idx for topic in selected_topics for idx in topic.get("chunk_indexes", [])})
                item["keywords"] = sorted({kw for topic in selected_topics for kw in topic.get("keywords", [])})
                item["entities"] = sorted({entity for topic in selected_topics for entity in topic.get("entities", [])})
                item["vector_text"] = "\n\n".join([
                    _self_text(item),
                    "SUPPORTING_TOPIC_EVIDENCE",
                    "\n".join(topic_text(topic) for topic in selected_topics),
                ]).strip()
                item["vector"] = safe_embed_texts(self.embeddings, [item["vector_text"]])[0] if item["vector_text"] else group["vector"]
                extracted.append(item)
            if debug and self.logger:
                self.logger.trace_call("MeetingEventService.extract_group.output", output=extracted, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
            return extracted

        ordered: list[list[dict[str, Any]] | None] = [None] * len(groups)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(extract_group, group): idx for idx, group in enumerate(groups)}
            for future in as_completed(futures):
                ordered[futures[future]] = future.result()
        for group_events in ordered:
            meeting_events.extend(group_events or [])
        if debug and self.logger:
            self.logger.trace_call("MeetingEventService.generate_meeting_events.output", output=meeting_events, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        return meeting_events
