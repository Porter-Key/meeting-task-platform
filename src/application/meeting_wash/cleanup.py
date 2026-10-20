from __future__ import annotations

from typing import Any

from .ai_cleanup import AICleanupService
from .chunking import build_chunks


class MeetingWashService:
    def __init__(self, meeting_repo: Any, ai_cleanup: AICleanupService | None = None) -> None:
        self.meeting_repo = meeting_repo
        self.ai_cleanup = ai_cleanup

    def wash_meeting(self, meeting_id: str, *, use_ai_cleanup: bool | None = None) -> dict[str, Any]:
        transcript = self.meeting_repo.get_raw_meeting(meeting_id)
        if not transcript:
            raise ValueError(f"Meeting not found: {meeting_id}")
        chunks = build_chunks(transcript.get("sentences") or [])
        should_ai_clean = self.ai_cleanup is not None if use_ai_cleanup is None else use_ai_cleanup
        if should_ai_clean and self.ai_cleanup is not None:
            chunks = self.ai_cleanup.clean_chunks(transcript, chunks)
        chunks = self.meeting_repo.replace_chunks(meeting_id, chunks)
        return {"meeting_id": meeting_id, "title": transcript.get("title") or "", "chunks": chunks}
