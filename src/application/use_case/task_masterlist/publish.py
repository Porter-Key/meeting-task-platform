from __future__ import annotations

from typing import Any

from application.use_case.task_masterlist.submit import submit_task_masterlist_items


def publish_task_masterlist(payload: dict[str, Any], *, job_id: str | None = None) -> dict[str, Any]:
    return submit_task_masterlist_items(payload, job_id=job_id)
