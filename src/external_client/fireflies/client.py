from __future__ import annotations

from typing import Any

import httpx

from external_client.config import FirefliesConfig
from .errors import FirefliesGraphQLError, FirefliesHTTPError
from .queries import ACTIVE_MEETINGS_QUERY, ANALYTICS_QUERY, TRANSCRIPT_QUERY, TRANSCRIPTS_QUERY


class FirefliesClient:
    def __init__(self, config: FirefliesConfig, *, http_client: httpx.Client | None = None) -> None:
        self.config = config
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=config.timeout_seconds)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "FirefliesClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._client.post(
            self.config.graphql_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}",
            },
            json={"query": query, "variables": variables or {}},
        )
        if response.status_code >= 400:
            raise FirefliesHTTPError(f"Fireflies HTTP {response.status_code}: {response.text}")
        payload = response.json()
        errors = payload.get("errors")
        if errors:
            raise FirefliesGraphQLError(errors)
        return payload.get("data", {})

    def get_transcript(self, transcript_id: str) -> dict[str, Any] | None:
        data = self.execute(TRANSCRIPT_QUERY, {"transcriptId": transcript_id})
        return data.get("transcript")

    def list_transcripts(
        self,
        *,
        keyword: str | None = None,
        scope: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        limit: int | None = 50,
        skip: int | None = 0,
        host_email: str | None = None,
        organizers: list[str] | None = None,
        participants: list[str] | None = None,
        user_id: str | None = None,
        mine: bool | None = None,
        channel_id: str | None = None,
        completed_only: bool | None = None,
    ) -> list[dict[str, Any]]:
        variables = _without_none({
            "keyword": keyword,
            "scope": scope,
            "fromDate": from_date,
            "toDate": to_date,
            "limit": limit,
            "skip": skip,
            "hostEmail": host_email,
            "organizers": organizers,
            "participants": participants,
            "userId": user_id,
            "mine": mine,
            "channelId": channel_id,
        })
        data = self.execute(TRANSCRIPTS_QUERY, variables)
        rows = data.get("transcripts", [])
        if completed_only:
            return [row for row in rows if _is_completed_transcript(row)]
        return rows

    def get_active_meetings(self, *, email: str | None = None, states: list[str] | None = None) -> list[dict[str, Any]]:
        data = self.execute(ACTIVE_MEETINGS_QUERY, _without_none({"email": email, "states": states}))
        return data.get("active_meetings", [])

    def get_analytics(self, *, start_time: str | None = None, end_time: str | None = None) -> dict[str, Any] | None:
        data = self.execute(ANALYTICS_QUERY, _without_none({"startTime": start_time, "endTime": end_time}))
        return data.get("analytics")


def create_client(config: FirefliesConfig, *, http_client: httpx.Client | None = None) -> FirefliesClient:
    return FirefliesClient(config, http_client=http_client)


def _without_none(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def _is_completed_transcript(row: dict[str, Any]) -> bool:
    if row.get("is_live") is True:
        return False
    info = row.get("meeting_info") or {}
    summary_status = str(info.get("summary_status") or "").lower()
    if summary_status and summary_status not in {"completed", "complete", "done", "processed"}:
        return False
    return True
