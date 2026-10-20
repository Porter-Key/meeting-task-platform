from __future__ import annotations

from pydantic import BaseModel

from domain.rules.lifecycle import can_change_state
from application.meeting_wash.ai_cleanup import AICleanupService
from application.meeting_wash.cleanup import MeetingWashService
from django_client.ids import new_id
from django_client.repositories import LifecycleRepo, LogRepo, MeetingRepo
from external_client.config import get_config
from external_client.llm.chat import create_chat_model


class WashMeetingRequest(BaseModel):
    meeting_id: str
    use_ai_cleanup: bool = True


def wash_meeting(payload: dict, *, job_id: str | None = None) -> dict:
    request = WashMeetingRequest.model_validate(payload)
    lifecycle = LifecycleRepo()
    chat_model = create_chat_model(get_config().llm_provider(), streaming=False)
    result = MeetingWashService(MeetingRepo(), AICleanupService(chat_model)).wash_meeting(
        request.meeting_id,
        use_ai_cleanup=request.use_ai_cleanup,
    )
    lifecycle.mark(request.meeting_id, "washed", decision=can_change_state(subject_type="meeting", stage="wash", from_status=lifecycle.latest_meeting_status(request.meeting_id, "washed"), to_status="completed"))
    return result


from typing import Any

from pydantic import BaseModel, Field

from application.meeting_wash.ai_cleanup import AICleanupService, DEFAULT_AI_CLEANUP_WORKERS
from application.meeting_wash.cleanup import MeetingWashService


class WashMeetingsRequest(BaseModel):
    meeting_ids: list[str] = Field(default_factory=list)
    limit: int | None = None
    use_ai_cleanup: bool = True
    max_workers: int = DEFAULT_AI_CLEANUP_WORKERS


def _summarize_wash_result(result: dict[str, Any]) -> dict[str, Any]:
    chunks = result.get("chunks") or []
    errors = 0
    changed = 0
    ratios: list[float] = []
    for chunk in chunks:
        raw_text = chunk.get("raw_text") or ""
        clean_text = chunk.get("text") or ""
        last_filter = (chunk.get("ai_filters") or [{}])[-1]
        if last_filter.get("error"):
            errors += 1
        if raw_text and clean_text != raw_text:
            changed += 1
        if raw_text:
            ratios.append(len(clean_text) / len(raw_text))

    return {
        "meeting_id": result.get("meeting_id"),
        "title": result.get("title") or "",
        "chunks": len(chunks),
        "changed_chunks": changed,
        "ai_cleanup_errors": errors,
        "avg_length_ratio": round(sum(ratios) / len(ratios), 3) if ratios else 0,
    }


def wash_meetings(payload: dict | None = None, *, job_id: str | None = None) -> dict:
    request = WashMeetingsRequest.model_validate(payload or {})
    correlation_id = new_id("wash")
    meeting_repo = MeetingRepo()
    lifecycle = LifecycleRepo()
    logger = LogRepo()

    meeting_ids = request.meeting_ids or meeting_repo.list_meeting_ids()
    if request.limit is not None:
        meeting_ids = meeting_ids[: request.limit]

    chat_model = create_chat_model(get_config().llm_provider(), streaming=False)
    ai_cleanup = AICleanupService(chat_model, max_workers=request.max_workers)
    service = MeetingWashService(meeting_repo, ai_cleanup)

    logger.info(
        "meeting_wash_batch_started",
        "Meeting wash batch started",
        stage="meeting_wash",
        correlation_id=correlation_id,
        meeting_ids=meeting_ids,
        use_ai_cleanup=request.use_ai_cleanup,
        max_workers=request.max_workers,
    )

    results = []
    log_ids = []
    for meeting_id in meeting_ids:
        summary = _summarize_wash_result(service.wash_meeting(meeting_id, use_ai_cleanup=request.use_ai_cleanup))
        lifecycle.mark(meeting_id, "washed", metadata=summary, decision=can_change_state(subject_type="meeting", stage="wash", from_status=lifecycle.latest_meeting_status(meeting_id, "washed"), to_status="completed", metadata=summary))
        results.append(summary)
        log_ids.append(
            logger.info(
                "meeting_wash_completed",
                "Meeting wash completed",
                stage="meeting_wash",
                correlation_id=correlation_id,
                meeting_id=meeting_id,
                payload_summary=summary,
            )
        )

    total_chunks = sum(result["chunks"] for result in results)
    total_changed = sum(result["changed_chunks"] for result in results)
    total_errors = sum(result["ai_cleanup_errors"] for result in results)
    batch_log_id = logger.info(
        "meeting_wash_batch_completed",
        "Meeting wash batch completed",
        stage="meeting_wash",
        correlation_id=correlation_id,
        meetings=len(results),
        total_chunks=total_chunks,
        total_changed_chunks=total_changed,
        total_ai_cleanup_errors=total_errors,
        meeting_ids=meeting_ids,
        use_ai_cleanup=request.use_ai_cleanup,
        max_workers=request.max_workers,
    )

    return {
        "meetings": len(results),
        "meeting_ids": meeting_ids,
        "use_ai_cleanup": request.use_ai_cleanup,
        "max_workers": request.max_workers,
        "correlation_id": correlation_id,
        "log_ids": [*log_ids, batch_log_id],
        "total_chunks": total_chunks,
        "total_changed_chunks": total_changed,
        "total_ai_cleanup_errors": total_errors,
    }
