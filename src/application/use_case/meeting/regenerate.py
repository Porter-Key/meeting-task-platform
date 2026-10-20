from __future__ import annotations

from typing import Any

from application.use_case.meeting.generate_events import generate_events


def regenerate_meeting(payload: dict[str, Any], *, job_id: str | None = None) -> dict[str, Any]:
    return generate_events(payload, job_id=job_id)
