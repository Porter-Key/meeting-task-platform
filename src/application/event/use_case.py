from __future__ import annotations

from typing import Any

from application.meeting_wash.ai_cleanup import AICleanupService
from application.meeting_wash.cleanup import MeetingWashService

from .pipeline import EventGenerationPipeline
from .schemas import GenerateEventsResult


class GenerateEventsUseCase:
    """Packaged application use-case. Gate/function must call this, not orchestrate steps."""

    def __init__(self, *, repositories: Any, chat_model: Any, embeddings: Any, logger: Any | None = None) -> None:
        self.logger = logger
        self.meeting_wash = MeetingWashService(repositories.meeting, AICleanupService(chat_model))
        self.pipeline = EventGenerationPipeline(
            meeting_repo=repositories.meeting,
            topic_repo=repositories.topic,
            meeting_graph_repo=repositories.meeting_graph,
            chat_model=chat_model,
            embeddings=embeddings,
            conclusion_repo=repositories.conclusion,
            lifecycle_repo=repositories.lifecycle,
            log_repo=repositories.logs,
            logger=logger,
        )

    def _meeting_context(self, washed: dict[str, Any]) -> dict[str, Any]:
        raw = self.meeting_wash.meeting_repo.get_raw_meeting(washed["meeting_id"]) or {}
        raw_attendees = raw.get("attendees") or raw.get("participants") or raw.get("speakers") or []
        attendees: list[str] = []
        for item in raw_attendees if isinstance(raw_attendees, list) else [raw_attendees]:
            for part in str(item).split(","):
                part = part.strip()
                if part and part not in attendees:
                    attendees.append(part)
        return {
            "id": washed["meeting_id"],
            "title": washed.get("title", ""),
            "date": raw.get("date") or raw.get("meeting_date") or raw.get("scheduled_date"),
            "start_time": raw.get("start_time") or raw.get("started_at") or raw.get("start_at"),
            "end_time": raw.get("end_time") or raw.get("ended_at") or raw.get("end_at"),
            "attendees": attendees,
            "organizer": raw.get("organizer") or raw.get("host") or raw.get("owner"),
            "language": raw.get("language") or raw.get("locale"),
            "source_system": raw.get("source_system") or raw.get("source") or raw.get("provider") or "fireflies",
        }

    def run(self, meeting_id: str, *, use_existing_chunks: bool = True, use_ai_cleanup: bool = False, debug: bool = False, correlation_id: str | None = None) -> GenerateEventsResult:
        if debug and self.logger:
            self.logger.trace_call(
                "GenerateEventsUseCase.run.input",
                input={"meeting_id": meeting_id, "use_existing_chunks": use_existing_chunks, "use_ai_cleanup": use_ai_cleanup},
                stage="event_debug",
                correlation_id=correlation_id,
                meeting_id=meeting_id,
            )
        washed = self.meeting_wash.meeting_repo.get_meeting_with_chunks(meeting_id) if use_existing_chunks else None
        if not washed or not washed.get("chunks"):
            washed = self.meeting_wash.wash_meeting(meeting_id, use_ai_cleanup=use_ai_cleanup)
        result = self.pipeline.generate_for_clean_meeting(self._meeting_context(washed), washed["chunks"], debug=debug, correlation_id=correlation_id)
        if debug and self.logger:
            self.logger.trace_call(
                "GenerateEventsUseCase.run.output",
                output=result.model_dump(),
                stage="event_debug",
                correlation_id=correlation_id,
                meeting_id=meeting_id,
            )
        return result
