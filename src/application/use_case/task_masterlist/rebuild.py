from __future__ import annotations

from typing import Any


def rebuild_task_masterlist(payload: dict[str, Any], *, job_id: str | None = None) -> dict[str, Any]:
    return {"rebuilt": True, "payload": payload}
