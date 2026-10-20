from __future__ import annotations

from typing import Any

from django.utils import timezone

from domain.models.job import ApplicationJob
from domain.models.lifecycle import BeatSchedule
from domain.models.meeting import MeetingPipelineRun
from .ids import new_id


def list_object(subject_type: str, subject_id: str, *, stage: str | None = None, limit: int = 100) -> dict[str, Any]:
    if subject_type == "meeting":
        rows = MeetingPipelineRun.objects.filter(meeting_id=subject_id)
        if stage:
            rows = rows.filter(stage=stage)
        events = [dump_meeting_run(row) for row in rows.order_by("-created_at")[:limit]]
        return {"subject_type": subject_type, "subject_id": subject_id, "events": events, "latest": events[0] if events else None}
    if subject_type == "beat_schedule":
        row = BeatSchedule.objects.filter(id=subject_id).first()
        lifecycle = ((row.metadata_payload or {}).get("lifecycle") or {}) if row else {}
        return {"subject_type": subject_type, "subject_id": subject_id, "events": [lifecycle] if lifecycle else [], "latest": lifecycle or None}
    if subject_type == "job":
        row = ApplicationJob.objects.filter(id=subject_id).first()
        event = {"status": row.status, "error": row.error, "updated_at": row.updated_at, "started_at": row.started_at, "finished_at": row.finished_at} if row else None
        return {"subject_type": subject_type, "subject_id": subject_id, "events": [event] if event else [], "latest": event}
    return {"subject_type": subject_type, "subject_id": subject_id, "events": [], "latest": None}


def mark_meeting(meeting_id: str, stage: str, *, status: str = "completed", job_id: str | None = None, metadata: dict[str, Any] | None = None, error: str | None = None, decision: Any | None = None) -> None:
    now = timezone.now()
    payload = dict(metadata or {})
    if decision is not None:
        payload["domain_decision"] = decision.model_dump() if hasattr(decision, "model_dump") else decision
    MeetingPipelineRun.objects.create(id=new_id("run"), meeting_id=meeting_id, pipeline_name=pipeline_name(stage), stage=stage, status=status, job_id=job_id, started_at=now, finished_at=now if status not in {"running", "queued"} else None, error=error, metadata_payload=payload)


def mark_meeting_running(meeting_id: str, stage: str, *, job_id: str | None = None, metadata: dict[str, Any] | None = None, decision: Any | None = None) -> None:
    mark_meeting(meeting_id, stage, status="running", job_id=job_id, metadata=metadata, decision=decision)


def mark_meeting_completed(meeting_id: str, stage: str, *, job_id: str | None = None, metadata: dict[str, Any] | None = None, decision: Any | None = None) -> None:
    mark_meeting(meeting_id, stage, status="completed", job_id=job_id, metadata=metadata, decision=decision)


def mark_meeting_failed(meeting_id: str, stage: str, *, job_id: str | None = None, error: str | None = None, metadata: dict[str, Any] | None = None, decision: Any | None = None) -> None:
    mark_meeting(meeting_id, stage, status="terminal_failed", job_id=job_id, metadata=metadata, error=error, decision=decision)


def latest_meeting_status(meeting_id: str, stage: str) -> str | None:
    row = MeetingPipelineRun.objects.filter(meeting_id=meeting_id, stage=stage).order_by("-created_at").first()
    return row.status if row else None


def pipeline_name(stage: str) -> str:
    if stage in {"pulled", "ingested", "source_synced", "transcript_saved"}:
        return "ingest"
    if stage in {"washed"}:
        return "wash"
    if stage in {"pipeline"}:
        return "pipeline"
    return "generate"


def dump_meeting_run(row: MeetingPipelineRun) -> dict[str, Any]:
    return {"run_id": row.id, "meeting_id": row.meeting_id, "pipeline_name": row.pipeline_name, "stage": row.stage, "status": row.status, "job_id": row.job_id, "started_at": row.started_at, "finished_at": row.finished_at, "error": row.error, "metadata": row.metadata_payload or {}}


def meeting(meeting_id: str, *, limit: int = 100) -> dict[str, Any]:
    return list_object("meeting", meeting_id, limit=limit)


def beat_schedule(schedule_id: str, *, limit: int = 100) -> dict[str, Any]:
    return list_object("beat_schedule", schedule_id, limit=limit)
