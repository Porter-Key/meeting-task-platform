from __future__ import annotations

from typing import Any

from application.use_case.task_masterlist.publish import publish_task_masterlist


def run_task_masterlist_publish(payload: dict[str, Any], *, job_id: str | None = None) -> dict[str, Any]:
    return publish_task_masterlist(payload, job_id=job_id)
