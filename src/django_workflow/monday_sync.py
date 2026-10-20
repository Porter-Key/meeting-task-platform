from __future__ import annotations

from typing import Any

from application.use_case.monday.associate_identity import associate_identity
from application.use_case.monday.sync_structure import sync_structure
from application.use_case.monday.sync_users import sync_users


def run_monday_sync(payload: dict[str, Any] | None = None, *, job_id: str | None = None) -> dict[str, Any]:
    payload = payload or {}
    users = sync_users(payload, job_id=job_id)
    structure = sync_structure(payload, job_id=job_id)
    identity = associate_identity(payload, job_id=job_id)
    return {"users": users, "structure": structure, "identity": identity}
