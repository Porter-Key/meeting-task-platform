from __future__ import annotations

from pydantic import BaseModel, Field


class PullFirefliesMeetingsRequest(BaseModel):
    limit: int = Field(default=4, ge=0, le=100)
    skip: int = Field(default=0, ge=0)
    recent_days: int | None = Field(default=None, ge=1)
    meeting_ids: list[str] = Field(default_factory=list)
    from_date: str | None = None
    to_date: str | None = None
    completed_only: bool = True
