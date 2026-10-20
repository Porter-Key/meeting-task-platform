from __future__ import annotations

from typing import Any

import django_client.monday as monday


def sync_structure(payload: dict[str, Any] | None = None, *, job_id: str | None = None) -> dict[str, Any]:
    return monday.structure(active_only=False, include_archived_groups=True)
