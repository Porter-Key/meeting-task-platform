from __future__ import annotations

from typing import Any

from celery import current_app

import django_client.job as job
import django_client.logs as logs


def enqueue_task(*, command: str, task_func: Any, payload: dict[str, Any], meeting_ids: list[str] | None = None) -> dict[str, Any]:
    current_app.config_from_object("django.conf:settings", namespace="CELERY")
    created = job.create(command=command, payload=payload, meeting_ids=meeting_ids or [])
    logs.write_for_payload(level="INFO", logger_name="web.graphql", event="graphql_mutation_accepted", message=f"Accepted mutation {command}", stage="graphql_mutation", correlation_id=created.id, payload=payload, extra={"command": command, "job_id": created.id})
    result = task_func.delay(created.id, payload)
    job.attach_queue_task(created.id, str(result.id))
    return {"job_id": created.id, "queue_task_id": str(result.id), "command": command, "status": created.status, "meeting_ids": meeting_ids or []}
