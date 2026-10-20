from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError

from external_client.llm.structured import with_structured_output

from .conclusion_normalizer import normalize_people_tasks
from .people_tasks_prompts import people_tasks_prompt
from .schemas import PeopleTasksSchema


class PeopleTaskService:
    def __init__(self, chat_model: Any, logger: Any | None = None) -> None:
        self.chat_model = chat_model
        self.extractor = with_structured_output(chat_model, PeopleTasksSchema)
        self.logger = logger

    def generate(self, meeting: dict[str, Any], topics: list[dict[str, Any]], conclusion: dict[str, Any], *, fact_layer: dict[str, Any] | None = None, debug: bool = False, correlation_id: str | None = None) -> list[dict[str, Any]]:
        if debug and self.logger:
            self.logger.trace_call("PeopleTaskService.generate.input", input={"meeting": meeting, "conclusion": conclusion}, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        payload = self._invoke_with_retries(meeting, conclusion, fact_layer, correlation_id=correlation_id)
        temp = {**conclusion, "people_tasks": _realign_owner_refs(payload.get("people_tasks") or [], fact_layer)}
        people_tasks = normalize_people_tasks(temp, topics, default_topic_indexes=list(range(len(topics))), allowed_chunks=set(int(idx) for topic in topics for idx in (topic.get("chunk_indexes") or []) if str(idx).isdigit()))
        if debug and self.logger:
            self.logger.trace_call("PeopleTaskService.generate.output", output=people_tasks, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        return people_tasks

    def _invoke_with_retries(self, meeting: dict[str, Any], conclusion: dict[str, Any], fact_layer: dict[str, Any] | None, *, correlation_id: str | None = None) -> dict[str, Any]:
        prompt = people_tasks_prompt(meeting, conclusion, fact_layer)
        messages = [("system", "You generate only the people_tasks dispatch layer from refined events."), ("human", prompt)]
        errors: list[str] = []
        for attempt in range(2):
            try:
                parsed = self.extractor.invoke(messages if attempt == 0 else [("system", "Return a complete compact JSON object matching the schema. No markdown. Do not truncate."), ("human", _compact_retry_prompt(meeting, conclusion, fact_layer))])
                return PeopleTasksSchema.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()
            except (ValidationError, ValueError, TypeError) as exc:
                errors.append(repr(exc))
                if self.logger:
                    self.logger.warning("people_tasks_structured_retry", "People tasks structured output failed; retrying", stage="people_tasks", correlation_id=correlation_id, meeting_id=meeting.get("id"), attempt=attempt + 1, error=repr(exc)[:800])
        repaired = self._text_fallback(meeting, conclusion, fact_layer, correlation_id=correlation_id, errors=errors)
        if repaired is not None:
            return repaired
        if self.logger:
            self.logger.error("people_tasks_generation_failed", "People tasks generation failed after retries; continuing with empty people_tasks", stage="people_tasks", correlation_id=correlation_id, meeting_id=meeting.get("id"), errors=errors[-2:])
        return {"people_tasks": []}

    def _text_fallback(self, meeting: dict[str, Any], conclusion: dict[str, Any], fact_layer: dict[str, Any] | None, *, correlation_id: str | None = None, errors: list[str] | None = None) -> dict[str, Any] | None:
        try:
            response = self.chat_model.invoke([("system", "Return only valid compact JSON with top-level key people_tasks. No markdown."), ("human", _compact_retry_prompt(meeting, conclusion, fact_layer))])
            text = getattr(response, "content", response)
            data = _parse_json_object(text if isinstance(text, str) else str(text))
            return PeopleTasksSchema.model_validate(data).model_dump()
        except Exception as exc:  # noqa: BLE001 - fallback boundary must not fail regenerate
            if self.logger:
                self.logger.warning("people_tasks_text_fallback_failed", "People tasks text fallback failed", stage="people_tasks", correlation_id=correlation_id, meeting_id=meeting.get("id"), error=repr(exc)[:800], previous_errors=(errors or [])[-2:])
            return None


def _compact_retry_prompt(meeting: dict[str, Any], conclusion: dict[str, Any], fact_layer: dict[str, Any] | None) -> str:
    compact_conclusion = {
        "title": conclusion.get("title"),
        "summary": conclusion.get("summary"),
        "events": [
            {
                "title": item.get("title"),
                "summary": item.get("summary"),
                "decisions": item.get("decisions") or [],
                "open_issues": item.get("open_issues") or [],
                "source_topic_indexes": item.get("source_topic_indexes") or [],
                "source_chunk_indexes": item.get("source_chunk_indexes") or [],
            }
            for item in (conclusion.get("events") or [])
        ],
    }
    return people_tasks_prompt(meeting, compact_conclusion, fact_layer)


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


def _realign_owner_refs(groups: list[dict[str, Any]], fact_layer: dict[str, Any] | None) -> list[dict[str, Any]]:
    candidates = (fact_layer or {}).get("people_candidates") or []
    if not candidates:
        return groups
    by_ref = {str(item.get("ref") or ""): item for item in candidates}
    by_label: dict[str, str] = {}
    for item in candidates:
        ref = str(item.get("ref") or "")
        labels = [item.get("display_label"), item.get("email"), *(item.get("aliases") or [])]
        for label in labels:
            key = _norm_label(str(label or ""))
            if key:
                by_label[key] = ref
    fixed: list[dict[str, Any]] = []
    for group in groups:
        group = dict(group)
        ref = str(group.get("owner_ref") or "")
        expected = _ref_for_group(group, by_label)
        if expected and expected in by_ref and expected != ref:
            group["owner_ref"] = expected
            group["unknown_owner_text"] = None
            for task in group.get("tasks") or []:
                if isinstance(task, dict):
                    task["owner_ref"] = expected
                    task["unknown_owner_text"] = None
        fixed.append(group)
    return fixed


def _ref_for_group(group: dict[str, Any], by_label: dict[str, str]) -> str | None:
    labels = [group.get("person_name"), group.get("suggested_owner"), group.get("unknown_owner_text")]
    for task in group.get("tasks") or []:
        if isinstance(task, dict):
            labels.extend([task.get("owner_person_name"), task.get("suggested_owner"), task.get("unknown_owner_text")])
    for label in labels:
        ref = by_label.get(_norm_label(str(label or "")))
        if ref:
            return ref
    return None


def _norm_label(value: str) -> str:
    return " ".join(value.strip().lower().replace("@anonymous.local", "").replace("-", " ").split())
