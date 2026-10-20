from __future__ import annotations

from typing import Any


def associate_identity(payload: dict[str, Any] | None = None, *, job_id: str | None = None) -> dict[str, Any]:
    return {"associated": True, "payload": payload or {}}
