from __future__ import annotations

from dataclasses import asdict

from application.fireflies.ingest import FirefliesIngestService
from application.fireflies.pull import FirefliesPullService
from application.fireflies.schemas import PullFirefliesMeetingsRequest
from application.people_extraction import extract_people_from_meetings
from django_client.repositories import LifecycleRepo, MeetingRepo, PersonRepo
from domain.models.meeting import MeetingTranscript
from domain.models.task_masterlist import TaskMasterlist, TaskOrigin
from domain.rules.lifecycle import can_change_state
from external_client.config import get_config
from external_client.fireflies.client import create_client
from pydantic import BaseModel


class PullFirefliesMeetingsResult(BaseModel):
    count: int
    meeting_ids: list[str]
    titles: list[str]


def ingest_fireflies_meetings(payload: dict | None = None, *, job_id: str | None = None) -> dict:
    request = PullFirefliesMeetingsRequest.model_validate(payload or {})
    config = get_config()
    meeting_repo = MeetingRepo()
    lifecycle = LifecycleRepo()
    people_repo = PersonRepo()
    service = FirefliesIngestService(FirefliesPullService(lambda: create_client(config.fireflies)), meeting_repo)
    result = asdict(service.ingest_recent(limit=request.limit, skip=request.skip, meeting_ids=request.meeting_ids, recent_days=request.recent_days, from_date=request.from_date, to_date=request.to_date, completed_only=request.completed_only))
    lifecycle_result = register_existing_lifecycle(result.get("candidate_meeting_ids") or result.get("meeting_ids") or [], lifecycle=lifecycle, job_id=job_id)
    result["lifecycle_sync"] = lifecycle_result
    people = extract_people_from_meetings(result.get("transcripts") or [], source="fireflies_ingest")
    result["people_sync"] = people_repo.upsert_many(people)
    result.pop("transcripts", None)
    return result


def register_existing_lifecycle(meeting_ids: list[str], *, lifecycle: LifecycleRepo | None = None, job_id: str | None = None) -> dict:
    lifecycle = lifecycle or LifecycleRepo()
    ids = list(dict.fromkeys(str(meeting_id) for meeting_id in meeting_ids if meeting_id))
    transcript_ids = set(MeetingTranscript.objects.filter(meeting_id__in=ids).values_list("meeting_id", flat=True)) if ids else set()
    origin_task_ids = set(TaskOrigin.objects.filter(meeting_id__in=ids).values_list("meeting_id", flat=True)) if ids else set()
    masterlist_task_ids = set(TaskMasterlist.objects.filter(origin__meeting_id__in=ids).values_list("origin__meeting_id", flat=True)) if ids else set()
    marked = {"ingested": 0, "task_extracted_completed": 0, "masterlist_sync_completed": 0}
    for meeting_id in ids:
        if meeting_id in transcript_ids:
            marked["ingested"] += _mark_once(lifecycle, meeting_id, "ingested", "ingested", job_id=job_id, metadata={"reason": "transcript_exists"})
        if meeting_id in origin_task_ids:
            marked["event_generation_completed"] = marked.get("event_generation_completed", 0) + _mark_once(lifecycle, meeting_id, "event_generation", "completed", job_id=job_id, metadata={"reason": "task_origins_exist"})
            marked["task_extracted_completed"] += _mark_once(lifecycle, meeting_id, "task_extracted", "completed", job_id=job_id, metadata={"reason": "task_origins_exist"})
        if meeting_id in masterlist_task_ids:
            marked["masterlist_sync_completed"] += _mark_once(lifecycle, meeting_id, "masterlist_sync", "completed", job_id=job_id, metadata={"reason": "task_masterlist_exists"})
    return {"candidate_meetings": len(ids), "with_transcript": len(transcript_ids), "with_task_origins": len(origin_task_ids), "with_task_masterlist": len(masterlist_task_ids), "marked": marked}


def _mark_once(lifecycle: LifecycleRepo, meeting_id: str, stage: str, status: str, *, job_id: str | None = None, metadata: dict | None = None) -> int:
    if lifecycle.latest_meeting_status(meeting_id, stage) == status:
        return 0
    lifecycle.mark(meeting_id, stage, status=status, job_id=job_id, metadata=metadata, decision=can_change_state(subject_type="meeting", stage=stage, from_status=lifecycle.latest_meeting_status(meeting_id, stage), to_status=status, metadata=metadata))
    return 1


def ingest_meeting(payload: dict | None = None, *, job_id: str | None = None) -> dict:
    return ingest_fireflies_meetings(payload, job_id=job_id)


def pull_fireflies_meetings(payload: dict | None = None, *, job_id: str | None = None) -> dict:
    request = PullFirefliesMeetingsRequest.model_validate(payload or {})
    config = get_config()
    transcripts = FirefliesPullService(lambda: create_client(config.fireflies)).pull_transcripts(
        limit=request.limit,
        skip=request.skip,
        meeting_ids=request.meeting_ids,
        recent_days=request.recent_days,
        from_date=request.from_date,
        to_date=request.to_date,
        completed_only=request.completed_only,
    )
    return PullFirefliesMeetingsResult(count=len(transcripts), meeting_ids=[transcript["id"] for transcript in transcripts], titles=[transcript.get("title") or "" for transcript in transcripts]).model_dump()
