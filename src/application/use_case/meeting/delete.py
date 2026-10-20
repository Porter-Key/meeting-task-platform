from __future__ import annotations

from typing import Any

from domain.models.meeting import Meeting


def delete_meeting(payload: dict[str, Any], *, job_id: str | None = None) -> dict[str, Any]:
    meeting_id = str(payload.get("meeting_id") or "")
    deleted, _ = Meeting.objects.filter(id=meeting_id).delete()
    return {"meeting_id": meeting_id, "deleted": deleted}
