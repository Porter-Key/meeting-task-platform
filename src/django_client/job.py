from __future__ import annotations

from typing import Any

from django.utils import timezone

from domain.models.job import ApplicationJob
from domain.models.logs import ApplicationLog
from .ids import new_job_id


def create(*, command: str, payload: dict[str, Any], meeting_ids: list[str] | None = None) -> ApplicationJob:
    return ApplicationJob.objects.create(id=new_job_id(), command=command, status="queued", meeting_ids=meeting_ids or [], payload=payload, result={})


def attach_queue_task(job_id: str, queue_task_id: str | None) -> None:
    ApplicationJob.objects.filter(id=job_id).update(queue_task_id=queue_task_id)


def mark_running(job_id: str) -> None:
    ApplicationJob.objects.filter(id=job_id).update(status="running", started_at=timezone.now())


def mark_completed(job_id: str, result: dict[str, Any]) -> None:
    ApplicationJob.objects.filter(id=job_id).update(status="completed", result=result, finished_at=timezone.now())


def mark_failed(job_id: str, error: str) -> None:
    ApplicationJob.objects.filter(id=job_id).update(status="failed", error=error, finished_at=timezone.now())


def get(job_id: str) -> dict[str, Any] | None:
    job = ApplicationJob.objects.filter(id=job_id).first()
    return dump(job) if job else None


def get_with_progress(job_id: str, *, limit: int = 100) -> dict[str, Any] | None:
    job = ApplicationJob.objects.filter(id=job_id).first()
    if not job:
        return None
    logs = list(ApplicationLog.objects.filter(correlation_id=job_id).order_by("created_at")[:limit])
    data = dump(job)
    data["progress"] = progress(job, logs)
    return data


def list_recent(*, limit: int = 50) -> list[dict[str, Any]]:
    return [dump(job) for job in ApplicationJob.objects.order_by("-created_at")[:limit]]


def dump(job: ApplicationJob) -> dict[str, Any]:
    return {"job_id": job.id, "queue_task_id": job.queue_task_id, "command": job.command, "status": job.status, "meeting_ids": job.meeting_ids or [], "payload": job.payload or {}, "result": job.result or {}, "error": job.error, "created_at": job.created_at, "updated_at": job.updated_at, "started_at": job.started_at, "finished_at": job.finished_at}


def progress(job: ApplicationJob, logs: list[ApplicationLog]) -> dict[str, Any]:
    events = [dump_progress_event(row) for row in logs]
    current = events[-1] if events else None
    total_meetings = len(job.meeting_ids or []) or None
    completed_events = {"meeting_pipeline_completed", "event_generation_completed", "meeting_processing_completed"}
    completed_count = len({str(event.get("meeting_id")) for event in events if event.get("meeting_id") and event.get("event") in completed_events})
    percent = 100 if job.status in {"completed", "failed"} else (min(99, int((completed_count / total_meetings) * 100)) if total_meetings else None)
    return {"status": job.status, "current_stage": current.get("stage") if current else None, "current_event": current.get("event") if current else None, "current_message": current.get("message") if current else None, "current_meeting_id": current.get("meeting_id") if current else None, "total_meetings": total_meetings, "completed_meetings": completed_count, "percent": percent, "started_at": job.started_at, "finished_at": job.finished_at, "error": job.error, "events": events, "event_count": len(events), "has_events": bool(events), "is_stale": job.status == "running" and not events}


def dump_progress_event(row: ApplicationLog) -> dict[str, Any]:
    return {"id": row.id, "created_at": row.created_at, "level": row.level, "stage": row.stage, "event": row.event, "message": row.message, "meeting_id": row.meeting_id, "payload": row.payload or {}}
