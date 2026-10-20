from __future__ import annotations

from typing import Any

from celery import shared_task

from application.tasks.meeting import _run
from django_workflow.task_masterlist_publish import run_task_masterlist_publish


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def submit_task_masterlist_items_task(self, job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _run(job_id, payload, run_task_masterlist_publish)
