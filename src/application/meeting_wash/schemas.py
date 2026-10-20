from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class CleanChunk(BaseModel):
    chunk_index: int
    speaker: str
    start_time: float
    end_time: float
    sentence_indexes: list[int | None] = Field(default_factory=list)
    text: str = ""
    ai_filters: list[dict] = Field(default_factory=list)


class AICleanChunkResult(BaseModel):
    clean_text: str = ""
    quality_notes: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    uncertain_terms: list[str] = Field(default_factory=list)

    @field_validator("quality_notes", "entities", "uncertain_terms", mode="before")
    @classmethod
    def _coerce_list(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value] if value else []
        if isinstance(value, list):
            return [str(item) for item in value if item is not None and str(item)]
        return [str(value)]


class CleanMeeting(BaseModel):
    meeting_id: str
    title: str = ""
    chunks: list[CleanChunk] = Field(default_factory=list)
