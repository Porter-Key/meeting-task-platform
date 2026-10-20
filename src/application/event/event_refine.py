from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from external_client.llm.structured import with_structured_output

from .conclusion_normalizer import chunks_by_index, normalize_conclusion, normalize_event, selected_option_indexes, topic_chunks_by_indexes
from .event_refine_prompts import event_refine_prompt
from .schemas import ConclusionEventSchema


class EventRefineService:
    def __init__(self, chat_model: Any, logger: Any | None = None) -> None:
        self.event_refiner = with_structured_output(chat_model, ConclusionEventSchema)
        self.logger = logger

    def refine_event(self, meeting: dict[str, Any], topics: list[dict[str, Any]], chunks: list[dict[str, Any]], conclusion: dict[str, Any], event_index: int, *, fact_layer: dict[str, Any] | None = None, debug: bool = False, correlation_id: str | None = None) -> dict[str, Any]:
        events = conclusion.get("events") or []
        if event_index >= len(events):
            return conclusion
        chunks_map = chunks_by_index(chunks)
        event = events[event_index]
        event_topic_indexes = selected_option_indexes(event.get("source_topic_indexes"), upper_bound=len(topics)) or list(range(len(topics)))
        event_topics = [topics[idx] for idx in event_topic_indexes]
        event_chunk_indexes = [idx for idx in (event.get("source_chunk_indexes") or topic_chunks_by_indexes(topics, event_topic_indexes)) if idx in chunks_map]
        event_chunks = [chunks_map[idx] for idx in sorted(set(event_chunk_indexes))]
        if not event_chunks:
            return conclusion
        if debug and self.logger:
            self.logger.trace_call(
                "EventRefineService.refine_event.input",
                input={"meeting": meeting, "event_index": event_index, "event": event, "event_topics": event_topics, "event_chunks": event_chunks, "conclusion": conclusion},
                stage="event_debug",
                correlation_id=correlation_id,
                meeting_id=meeting.get("id"),
            )
        try:
            parsed = self.event_refiner.invoke([
                ("system", "You refine one event inside a meeting conclusion. Use the fact layer to avoid factual errors."),
                ("human", event_refine_prompt(meeting, event, event_topics, event_chunks, conclusion, event_index, fact_layer)),
            ])
            replacement = ConclusionEventSchema.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()
        except (ValidationError, ValueError, TypeError) as exc:
            if self.logger:
                self.logger.warning("conclusion_event_refine_failed", "Conclusion event refine failed; keeping original event", stage="event_refine", correlation_id=correlation_id, meeting_id=meeting.get("id"), event_index=event_index, error=repr(exc)[:800])
            replacement = dict(event)
        merged = {**conclusion}
        merged_events = [dict(item) for item in events]
        merged_events[event_index] = replacement
        merged["events"] = merged_events
        refined = normalize_conclusion(merged, topics, allowed_chunk_indexes=set(chunks_map.keys()), fact_layer=fact_layer)
        if debug and self.logger:
            self.logger.trace_call("EventRefineService.refine_event.output", output=refined, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        return refined
