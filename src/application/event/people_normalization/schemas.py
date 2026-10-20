from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class NormalizedPersonCandidate(BaseModel):
    ref: str
    email: str
    display_label: str
    aliases: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    confidence: float = 1.0
    review_required: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class MeetingPeopleNormalizationResult(BaseModel):
    meeting_id: str
    candidates: list[NormalizedPersonCandidate] = Field(default_factory=list)
    alias_links: int = 0
    rejected_roles: list[dict[str, Any]] = Field(default_factory=list)
    review_required: list[dict[str, Any]] = Field(default_factory=list)
    llm_plan: dict[str, Any] = Field(default_factory=dict)


class TaskOwnerRepairResult(BaseModel):
    meeting_id: str
    repaired: int = 0
    skipped: list[dict[str, Any]] = Field(default_factory=list)
    rewrites: list[dict[str, Any]] = Field(default_factory=list)


class IdentityMergePlanItem(BaseModel):
    action: str
    target_email: str | None = None
    alias: str | None = None
    alias_email: str | None = None
    from_email: str | None = None
    to_email: str | None = None
    confidence: float = 0.0
    reason: str = ""


class IdentityNormalizationPlan(BaseModel):
    items: list[IdentityMergePlanItem] = Field(default_factory=list)
