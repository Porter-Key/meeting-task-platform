from __future__ import annotations

from typing import Any

from .ingest import FirefliesIngestResult, FirefliesIngestService
from .pull import FirefliesPullService


class FirefliesPipeline:
    def __init__(self, *, client_factory: Any, meeting_repo: Any) -> None:
        self.ingest_service = FirefliesIngestService(FirefliesPullService(client_factory), meeting_repo)

    def ingest_recent(self, *, limit: int, skip: int = 0) -> FirefliesIngestResult:
        return self.ingest_service.ingest_recent(limit=limit, skip=skip)
