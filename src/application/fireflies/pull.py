from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from external_client.fireflies.queries import TRANSCRIPT_QUERY


class FirefliesPullService:
    def __init__(self, client_factory: Any) -> None:
        self.client_factory = client_factory

    def pull_transcripts(
        self,
        *,
        limit: int,
        skip: int = 0,
        meeting_ids: list[str] | None = None,
        recent_days: int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        completed_only: bool = True,
    ) -> list[dict[str, Any]]:
        with self.client_factory() as client:
            listed = ([{"id": meeting_id} for meeting_id in meeting_ids] if meeting_ids else self._list_transcripts(client, limit=limit, skip=skip, from_date=from_date or self._from_date(recent_days), to_date=to_date, completed_only=completed_only))
            transcripts = []
            for item in listed:
                transcript = client.execute(TRANSCRIPT_QUERY, {"transcriptId": item["id"]}).get("transcript")
                if transcript and self._is_completed(transcript, completed_only=completed_only) and self._within_range(transcript, recent_days=recent_days, from_date=from_date, to_date=to_date):
                    transcripts.append(transcript)
            return transcripts

    def list_transcript_metadata(
        self,
        *,
        limit: int,
        skip: int = 0,
        recent_days: int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        completed_only: bool = True,
    ) -> list[dict[str, Any]]:
        with self.client_factory() as client:
            return self._list_transcripts(client, limit=limit, skip=skip, from_date=from_date or self._from_date(recent_days), to_date=to_date, completed_only=completed_only)

    def _list_transcripts(self, client: Any, *, limit: int, skip: int, from_date: str | None, to_date: str | None, completed_only: bool) -> list[dict[str, Any]]:
        if limit != 0:
            return client.list_transcripts(limit=limit, skip=skip, from_date=from_date, to_date=to_date, completed_only=completed_only)
        page_size = 50
        current_skip = skip
        results: list[dict[str, Any]] = []
        while True:
            page = client.list_transcripts(limit=page_size, skip=current_skip, from_date=from_date, to_date=to_date, completed_only=completed_only)
            if not page:
                break
            results.extend(page)
            if len(page) < page_size:
                break
            current_skip += page_size
        return results

    def _is_completed(self, transcript: dict[str, Any], *, completed_only: bool) -> bool:
        if not completed_only:
            return True
        if transcript.get("is_live") is True:
            return False
        info = transcript.get("meeting_info") or {}
        summary_status = str(info.get("summary_status") or "").lower()
        if summary_status and summary_status not in {"completed", "complete", "done", "processed"}:
            return False
        return True

    def _from_date(self, recent_days: int | None) -> str | None:
        if not recent_days:
            return None
        return (datetime.now(UTC) - timedelta(days=recent_days)).isoformat().replace("+00:00", "Z")

    def _within_range(self, transcript: dict[str, Any], *, recent_days: int | None, from_date: str | None, to_date: str | None) -> bool:
        if not recent_days and not from_date and not to_date:
            return True
        value = self._parse_datetime(transcript.get("dateString") or transcript.get("date") or transcript.get("started_at"))
        if value is None:
            return True
        if recent_days and value < datetime.now(UTC) - timedelta(days=recent_days):
            return False
        from_value = self._parse_datetime(from_date)
        if from_value and value < from_value:
            return False
        to_value = self._parse_datetime(to_date)
        if to_value and value > to_value:
            return False
        return True

    def _parse_datetime(self, raw: Any) -> datetime | None:
        if not raw:
            return None
        try:
            if isinstance(raw, (int, float)):
                value = datetime.fromtimestamp(raw / 1000 if raw > 10_000_000_000 else raw, UTC)
            else:
                value = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value
