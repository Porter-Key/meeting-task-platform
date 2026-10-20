from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class FirefliesIngestResult:
    meetings: int
    meeting_ids: list[str]
    transcripts: list[dict[str, Any]]
    candidate_meeting_ids: list[str]
    skipped_existing_meeting_ids: list[str]


class FirefliesIngestService:
    def __init__(self, pull_service: Any, meeting_repo: Any) -> None:
        self.pull_service = pull_service
        self.meeting_repo = meeting_repo

    def ingest_recent(
        self,
        *,
        limit: int,
        skip: int = 0,
        meeting_ids: list[str] | None = None,
        recent_days: int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        completed_only: bool = True,
    ) -> FirefliesIngestResult:
        candidates = [{"id": meeting_id} for meeting_id in meeting_ids] if meeting_ids else self.pull_service.list_transcript_metadata(limit=limit, skip=skip, recent_days=recent_days, from_date=from_date, to_date=to_date, completed_only=completed_only)
        candidate_ids = [str(item["id"]) for item in candidates if item.get("id")]
        existing_ids = self.meeting_repo.list_existing_transcript_ids(candidate_ids)
        missing_ids = [meeting_id for meeting_id in candidate_ids if meeting_id not in existing_ids]
        transcripts = self.pull_service.pull_transcripts(limit=len(missing_ids), skip=0, meeting_ids=missing_ids, recent_days=recent_days, from_date=from_date, to_date=to_date, completed_only=completed_only) if missing_ids else []
        saved_meeting_ids: list[str] = []
        for transcript in transcripts:
            self.meeting_repo.upsert_raw_meeting(transcript)
            saved_meeting_ids.append(transcript["id"])
        return FirefliesIngestResult(meetings=len(saved_meeting_ids), meeting_ids=candidate_ids, transcripts=transcripts, candidate_meeting_ids=candidate_ids, skipped_existing_meeting_ids=[meeting_id for meeting_id in candidate_ids if meeting_id in existing_ids])
