from __future__ import annotations

from typing import Any

from domain.models.lifecycle import BeatSchedule


def dispatch_due_schedules(payload: dict[str, Any] | None = None, *, job_id: str | None = None) -> dict[str, Any]:
    schedules = list(BeatSchedule.objects.filter(enabled=True).values("id", "name", "task_name", "workflow_key"))
    return {"schedules": schedules, "count": len(schedules)}
