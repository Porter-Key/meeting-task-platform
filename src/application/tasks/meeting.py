from __future__ import annotations

from typing import Any, Callable

from celery import shared_task

from application.use_case.meeting.delete import delete_meeting
from application.use_case.meeting.generate_events import generate_events
from application.use_case.meeting.ingest import ingest_fireflies_meetings, ingest_meeting
from application.use_case.meeting.regenerate import regenerate_meeting
from application.use_case.meeting.upsert_person import upsert_meeting_person
from application.use_case.meeting.wash import wash_meeting, wash_meetings
import django_client.job as job
import django_client.logs as logs
from django_workflow.meeting_pipeline import run_meeting_pipeline


def _job_id(payload: dict[str, Any], prefix: str) -> str:
    existing = payload.get("job_id")
    if existing:
        return str(existing)
    created = job.create(command=prefix, payload=payload, meeting_ids=list(payload.get("meeting_ids") or []))
    return created.id


def _run(job_id: str, payload: dict[str, Any], func: Callable[..., dict[str, Any]]) -> dict[str, Any]:
    job.mark_running(job_id)
    try:
        result = func(payload, job_id=job_id)
        job.mark_completed(job_id, result)
        return result
    except Exception as exc:
        job.mark_failed(job_id, repr(exc))
        logs.write_for_payload(level="ERROR", logger_name="application.tasks.meeting", event="task_failed", message=repr(exc), stage="celery", correlation_id=job_id, payload=payload)
        raise


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def meeting_pipeline_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, run_meeting_pipeline)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def ingest_fireflies_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, ingest_meeting)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def scheduled_ingest_fireflies_task(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {"recent_days": 60, "limit": 0, "skip": 0, "meeting_ids": [], "completed_only": True}
    return _run(_job_id(payload, "scheduled-ingest-fireflies"), payload, ingest_fireflies_meetings)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def wash_meeting_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, wash_meeting)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def wash_meetings_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, wash_meetings)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def generate_events_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, generate_events)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def delete_meeting_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, delete_meeting)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def regenerate_meeting_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, regenerate_meeting)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def upsert_meeting_person_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, upsert_meeting_person)
