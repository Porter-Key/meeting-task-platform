from __future__ import annotations

from typing import Any

from celery import shared_task

from application.tasks.meeting import _run
from django_workflow.beat_dispatch import run_beat_dispatch


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def dispatch_due_beat_schedules_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, run_beat_dispatch)
