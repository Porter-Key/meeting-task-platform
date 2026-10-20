from __future__ import annotations

from typing import Any

from application.use_case.beat.dispatch import dispatch_due_schedules


def run_beat_dispatch(payload: dict[str, Any] | None = None, *, job_id: str | None = None) -> dict[str, Any]:
    return dispatch_due_schedules(payload, job_id=job_id)
