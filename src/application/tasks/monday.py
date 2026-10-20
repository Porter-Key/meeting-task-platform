from __future__ import annotations

from typing import Any

from celery import shared_task

from application.tasks.meeting import _run
import django_client.job as job
from django_workflow.monday_sync import run_monday_sync


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def monday_sync_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, run_monday_sync)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def scheduled_monday_sync_task(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {"dry_run": False}
    created = job.create(command="scheduled-monday-sync", payload=payload, meeting_ids=[])
    return _run(created.id, payload, run_monday_sync)
