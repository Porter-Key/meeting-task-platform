from __future__ import annotations

from typing import Any

from .conclusion_normalizer import normalize_conclusion
from .event_draft import EventDraftService
from .fact_layer import build_people_candidates
from .event_refine import EventRefineService
from .people_tasks import PeopleTaskService
from .tl_dr import TlDrService
from .schemas import GenerateEventsResult
from .topic_extract import TopicExtractionService
from domain.rules.lifecycle import can_change_state


class EventGenerationPipeline:
    def __init__(self, *, meeting_repo: Any, topic_repo: Any, meeting_graph_repo: Any, chat_model: Any, embeddings: Any, conclusion_repo: Any | None = None, lifecycle_repo: Any | None = None, log_repo: Any | None = None, logger: Any | None = None) -> None:
        self.meeting_repo = meeting_repo
        self.topic_repo = topic_repo
        self.conclusion_repo = conclusion_repo
        self.lifecycle_repo = lifecycle_repo
        self.log_repo = log_repo
        self.meeting_graph_repo = meeting_graph_repo
        self.topic_extraction = TopicExtractionService(chat_model, embeddings, logger=logger)
        self.event_draft = EventDraftService(chat_model, embeddings, logger=logger)
        self.event_refine = EventRefineService(chat_model, logger=logger)
        self.people_tasks = PeopleTaskService(chat_model, logger=logger)
        self.tl_dr = TlDrService(chat_model, logger=logger)
        self.logger = logger

    def generate_for_clean_meeting(self, meeting: dict[str, Any], chunks: list[dict[str, Any]], *, debug: bool = False, correlation_id: str | None = None) -> GenerateEventsResult:
        meeting_id = meeting.get("id")
        self._log("event_pipeline_started", "Event pipeline started", correlation_id=correlation_id, meeting_id=meeting_id, payload={"chunk_count": len(chunks)})
        if debug and self.logger:
            self.logger.trace_call("EventGenerationPipeline.generate_for_clean_meeting.input", input={"meeting": meeting, "chunk_count": len(chunks)}, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        self._log("topic_extraction_started", "Topic extraction started", correlation_id=correlation_id, meeting_id=meeting_id, payload={"chunk_count": len(chunks)})
        topics = self.topic_extraction.extract_topics(meeting, chunks, debug=debug, correlation_id=correlation_id)
        topics = self.topic_repo.replace_topics(meeting["id"], topics)
        self._log("topic_extraction_completed", "Topic extraction completed", correlation_id=correlation_id, meeting_id=meeting_id, payload={"topic_count": len(topics)})
        if self.lifecycle_repo:
            self.lifecycle_repo.mark(meeting["id"], "topic_generated", decision=can_change_state(subject_type="meeting", stage="topic_generated", from_status=self.lifecycle_repo.latest_meeting_status(meeting["id"], "topic_generated"), to_status="completed"))
        self.meeting_graph_repo.upsert_meeting_chunks_topics(meeting, chunks, topics)
        self.topic_repo.replace_meeting_events(meeting["id"], [])
        self._log("event_draft_started", "Event draft started", correlation_id=correlation_id, meeting_id=meeting_id, payload={"topic_count": len(topics)})
        conclusion = self.event_draft.generate(meeting, topics, chunks, debug=debug, correlation_id=correlation_id)
        self._log("event_draft_completed", "Event draft completed", correlation_id=correlation_id, meeting_id=meeting_id, payload={"event_count": len(conclusion.get("events") or [])})
        fact_layer = conclusion.get("fact_layer")
        fact_layer = {**(fact_layer or {}), "people_candidates": build_people_candidates(meeting, chunks)}
        conclusion["fact_layer"] = fact_layer
        for event_index in range(len(conclusion.get("events") or [])):
            self._log("event_refine_started", "Event refine started", correlation_id=correlation_id, meeting_id=meeting_id, payload={"event_index": event_index})
            conclusion = self.event_refine.refine_event(meeting, topics, chunks, conclusion, event_index, fact_layer=fact_layer, debug=debug, correlation_id=correlation_id)
            self._log("event_refine_completed", "Event refine completed", correlation_id=correlation_id, meeting_id=meeting_id, payload={"event_index": event_index})
        self._log("people_tasks_started", "People task extraction started", correlation_id=correlation_id, meeting_id=meeting_id)
        conclusion["people_tasks"] = self.people_tasks.generate(meeting, topics, conclusion, fact_layer=fact_layer, debug=debug, correlation_id=correlation_id)
        self._log("people_tasks_completed", "People task extraction completed", correlation_id=correlation_id, meeting_id=meeting_id, payload={"people_task_count": len(conclusion.get("people_tasks") or [])})
        self._log("tl_dr_started", "TLDR generation started", correlation_id=correlation_id, meeting_id=meeting_id)
        tl_dr = self.tl_dr.generate(meeting, topics, conclusion, fact_layer=fact_layer, debug=debug, correlation_id=correlation_id)
        self._log("tl_dr_completed", "TLDR generation completed", correlation_id=correlation_id, meeting_id=meeting_id)
        conclusion.update(tl_dr)
        conclusion = normalize_conclusion(conclusion, topics, fact_layer=fact_layer)
        saved_conclusion = self.conclusion_repo.replace_for_meeting(meeting["id"], conclusion) if self.conclusion_repo else {}
        self._log("meeting_conclusion_saved", "Meeting conclusion saved", correlation_id=correlation_id, meeting_id=meeting_id, payload={"people_task_count": saved_conclusion.get("people_tasks") or 0})
        if self.lifecycle_repo:
            self.lifecycle_repo.mark(meeting["id"], "conclusion_generated", decision=can_change_state(subject_type="meeting", stage="conclusion_generated", from_status=self.lifecycle_repo.latest_meeting_status(meeting["id"], "conclusion_generated"), to_status="completed"))
            if saved_conclusion.get("people_tasks"):
                self.lifecycle_repo.mark(meeting["id"], "task_extracted", decision=can_change_state(subject_type="meeting", stage="task_extracted", from_status=self.lifecycle_repo.latest_meeting_status(meeting["id"], "task_extracted"), to_status="completed"))
        result = GenerateEventsResult(
            meeting_id=meeting["id"],
            topics=len(topics),
            meeting_events=0,
            meeting_conclusions=1 if conclusion else 0,
            meeting_conclusion=conclusion,
        )
        if debug and self.logger:
            self.logger.trace_call("EventGenerationPipeline.generate_for_clean_meeting.output", output=result.model_dump(), stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        self._log("event_pipeline_completed", "Event pipeline completed", correlation_id=correlation_id, meeting_id=meeting_id, payload={"topic_count": len(topics), "people_task_count": saved_conclusion.get("people_tasks") or 0})
        return result

    def _log(self, event: str, message: str, *, correlation_id: str | None = None, meeting_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
        if self.log_repo:
            self.log_repo.write(level="INFO", logger_name="application.event.pipeline", event=event, message=message, stage="event_pipeline", correlation_id=correlation_id, meeting_id=meeting_id, payload=payload or {})
