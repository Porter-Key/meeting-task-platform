from __future__ import annotations

from application.event.schemas import GenerateEventsRequest
from application.event.use_case import GenerateEventsUseCase
from application.event.people_normalization import MeetingPeopleNormalizationService, TaskOwnerRepairService
from application.task_masterlist import TaskMasterlistSyncService
from django_client.ids import new_id
from django_client.repositories import LogRepo, repositories
from domain.rules.lifecycle import can_change_state
from external_client.config import get_config
from external_client.llm.chat import create_chat_model
from external_client.llm.embeddings import create_embeddings


def generate_events(payload: dict, *, job_id: str | None = None) -> dict:
    request = GenerateEventsRequest.model_validate(payload)
    correlation_id = new_id("event")
    config = get_config()
    repos = repositories()
    logger = LogRepo()
    chat_model = create_chat_model(config.llm_provider(), streaming=False)
    embeddings = create_embeddings(config.embedding)
    start_log_id = logger.info(
        "event_generation_started",
        "Event generation started",
        stage="event_generation",
        correlation_id=correlation_id,
        meeting_id=request.meeting_id,
        model=getattr(chat_model, "model_name", None),
        use_existing_chunks=request.use_existing_chunks,
        use_ai_cleanup=request.use_ai_cleanup,
        debug=request.debug,
    )
    if request.debug:
        logger.trace_call(
            "generate_events.input",
            input=request.model_dump(),
            stage="event_debug",
            correlation_id=correlation_id,
            meeting_id=request.meeting_id,
        )
    try:
        metadata = {"correlation_id": correlation_id}
        repos.lifecycle.mark_meeting_running(request.meeting_id, "event_generation", metadata=metadata, decision=can_change_state(subject_type="meeting", stage="event_generation", from_status=repos.lifecycle.latest_meeting_status(request.meeting_id, "event_generation"), to_status="running", metadata=metadata))
        result = GenerateEventsUseCase(repositories=repos, chat_model=chat_model, embeddings=embeddings, logger=logger).run(
            request.meeting_id,
            use_existing_chunks=request.use_existing_chunks,
            use_ai_cleanup=request.use_ai_cleanup,
            debug=request.debug,
            correlation_id=correlation_id,
        ).model_dump()
        logger.info("people_normalization_started", "Meeting people normalization started", stage="event_people_normalization", correlation_id=correlation_id, meeting_id=request.meeting_id)
        result["people_normalization"] = MeetingPeopleNormalizationService(chat_model=chat_model).normalize_meeting_people(request.meeting_id, apply=True)
        logger.info("people_normalization_completed", "Meeting people normalization completed", stage="event_people_normalization", correlation_id=correlation_id, meeting_id=request.meeting_id, result=result["people_normalization"])
        logger.info("task_owner_repair_started", "Task owner repair started", stage="event_people_normalization", correlation_id=correlation_id, meeting_id=request.meeting_id)
        result["task_owner_repair"] = TaskOwnerRepairService().repair_task_owners(request.meeting_id, apply=True)
        logger.info("task_owner_repair_completed", "Task owner repair completed", stage="event_people_normalization", correlation_id=correlation_id, meeting_id=request.meeting_id, result=result["task_owner_repair"])
        result["task_masterlist_sync"] = TaskMasterlistSyncService(repos.task_masterlist).sync_meeting(meeting_id=request.meeting_id)
        repos.lifecycle.mark_meeting_completed(request.meeting_id, "masterlist_sync", metadata=result["task_masterlist_sync"], decision=can_change_state(subject_type="meeting", stage="masterlist_sync", from_status=repos.lifecycle.latest_meeting_status(request.meeting_id, "masterlist_sync"), to_status="completed", metadata=result["task_masterlist_sync"]))
    except Exception as exc:
        repos.meeting.clear_generated_artifacts(request.meeting_id)
        logger.error(
            "event_generation_failed",
            "Event generation failed",
            stage="event_generation",
            correlation_id=correlation_id,
            meeting_id=request.meeting_id,
            error=repr(exc),
        )
        raise
    if request.debug:
        logger.trace_call(
            "generate_events.output",
            output=result,
            stage="event_debug",
            correlation_id=correlation_id,
            meeting_id=request.meeting_id,
        )
    complete_log_id = logger.info(
        "event_generation_completed",
        "Event generation completed",
        stage="event_generation",
        correlation_id=correlation_id,
        meeting_id=request.meeting_id,
        result=result,
        debug=request.debug,
    )
    sync_result = result.get("task_masterlist_sync") or {}
    if int(sync_result.get("created") or 0) == 0:
        repos.lifecycle.mark(request.meeting_id, "task_extracted", status="no_tasks_terminal", metadata={"correlation_id": correlation_id, "log_id": complete_log_id})
    else:
        metadata = {"correlation_id": correlation_id, "log_id": complete_log_id}
        repos.lifecycle.mark_meeting_completed(request.meeting_id, "event_generation", metadata=metadata, decision=can_change_state(subject_type="meeting", stage="event_generation", from_status=repos.lifecycle.latest_meeting_status(request.meeting_id, "event_generation"), to_status="completed", metadata=metadata))
    return {**result, "correlation_id": correlation_id, "log_ids": [start_log_id, complete_log_id]}
