from __future__ import annotations

from typing import Any

import django_client.monday as monday


def sync_users(payload: dict[str, Any] | None = None, *, job_id: str | None = None) -> dict[str, Any]:
    return {"users": monday.list_users(include_disabled=True)}
