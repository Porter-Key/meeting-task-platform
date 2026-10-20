from __future__ import annotations

from typing import Any

from application.use_case.meeting.generate_events import generate_events
from application.use_case.meeting.ingest import ingest_meeting
from application.use_case.meeting.wash import wash_meeting


def run_meeting_pipeline(payload: dict[str, Any], *, job_id: str | None = None) -> dict[str, Any]:
    ingested = ingest_meeting(payload, job_id=job_id)
    washed = wash_meeting({**payload, **ingested}, job_id=job_id)
    generated = generate_events({**payload, **washed}, job_id=job_id)
    return {"ingested": ingested, "washed": washed, "generated": generated}
