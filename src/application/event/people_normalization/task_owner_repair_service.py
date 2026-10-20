from __future__ import annotations

from typing import Any

from django_client.people import canonical_person_email
from django_client.uow import maybe_atomic

from django_client.ids import new_id
from domain.models.meeting import MeetingPeopleCandidate
from domain.models.people import PersonAlias
from domain.models.task_masterlist import TaskAssigneeLink, TaskMasterlist, TaskOrigin

from .schemas import TaskOwnerRepairResult


class TaskOwnerRepairService:
    def __init__(self, session_factory: Any | None = None) -> None:
        self.session_factory = session_factory

    def repair_task_owners(self, meeting_id: str, *, apply: bool = True, only_unsubmitted: bool = True) -> dict[str, Any]:
        repaired = 0
        skipped: list[dict[str, Any]] = []
        rewrites: list[dict[str, Any]] = []
        with maybe_atomic():
            candidates = {row.ref: row for row in MeetingPeopleCandidate.objects.filter(meeting_id=meeting_id)}
            candidate_aliases = _candidate_alias_index(candidates)
            origins = list(TaskOrigin.objects.filter(meeting_id=meeting_id).order_by("created_at"))
            for origin in origins:
                task = TaskMasterlist.objects.filter(origin_id=origin.id).first()
                if task is not None and only_unsubmitted and task.status == "submitted":
                    skipped.append({"task_id": task.id, "reason": "submitted"})
                    continue
                candidate = _resolve_origin_candidate(origin, candidates, candidate_aliases)
                if candidate is None and origin.unknown_owner_text:
                    alias_row = PersonAlias.objects.filter(normalized_alias=_normalize_alias(origin.unknown_owner_text)).first()
                    if alias_row and alias_row.email_id:
                        candidate = _AliasCandidate(email=alias_row.email_id, alias_id=alias_row.id, confidence=alias_row.confidence)
                if candidate is None and origin.owner_email_id:
                    candidate = _AliasCandidate(email=origin.owner_email_id, alias_id=origin.owner_alias_id, confidence=0.9)
                if candidate is None:
                    skipped.append({"task_id": task.id if task else None, "origin_id": origin.id, "reason": "candidate_missing"})
                    continue
                effective_email = canonical_person_email(candidate.email)
                if not effective_email:
                    skipped.append({"task_id": task.id if task else None, "origin_id": origin.id, "reason": "email_missing"})
                    continue
                current = TaskAssigneeLink.objects.filter(masterlist_task_id=task.id, relation="assignee").order_by("created_at").first() if task else None
                rewrite = {"task_id": task.id if task else None, "origin_id": origin.id, "owner_ref": origin.owner_ref, "from_email": current.email_id if current else origin.owner_email_id, "to_email": effective_email, "to_alias_id": candidate.alias_id}
                if origin.owner_email_id == effective_email and origin.owner_alias_id == candidate.alias_id and (task is None or (current and current.email_id == effective_email and current.alias_id == candidate.alias_id)):
                    skipped.append({**rewrite, "reason": "already_current"})
                    continue
                rewrites.append(rewrite)
                if apply:
                    origin.owner_email_id = effective_email
                    origin.owner_alias_id = candidate.alias_id
                    origin.unknown_owner_text = None
                    origin.save(update_fields=["owner_email", "owner_alias", "unknown_owner_text"])
                    if task is None:
                        repaired += 1
                        continue
                    if current is None:
                        current = TaskAssigneeLink(id=new_id("assignee"), masterlist_task_id=task.id, relation="assignee", source="owner_repair", confidence=candidate.confidence, metadata_payload={})
                    current.email_id = effective_email
                    current.alias_id = candidate.alias_id
                    current.source = "owner_repair"
                    current.confidence = float(candidate.confidence or 0.0)
                    current.metadata_payload = {**(current.metadata_payload or {}), "origin_id": origin.id, "owner_ref": origin.owner_ref, "resolution_method": "people_normalization_repair"}
                    current.save()
                    repaired += 1
        return TaskOwnerRepairResult(meeting_id=meeting_id, repaired=repaired, skipped=skipped, rewrites=rewrites).model_dump()


class _AliasCandidate:
    def __init__(self, *, email: str, alias_id: str | None, confidence: float) -> None:
        self.email = email
        self.alias_id = alias_id
        self.confidence = confidence

    @property
    def email_id(self) -> str:
        return self.email


def _normalize_alias(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _candidate_alias_index(candidates: dict[str, MeetingPeopleCandidate]) -> dict[str, Any]:
    index: dict[str, Any] = {}
    for candidate in candidates.values():
        labels = [candidate.display_label, str(candidate.email_id)]
        labels.extend((candidate.metadata_payload or {}).get("aliases") or [])
        for value in labels:
            normalized = _normalize_alias(str(value or ""))
            if normalized:
                index[normalized] = candidate
    return index


def _resolve_origin_candidate(origin: TaskOrigin, candidates: dict[str, MeetingPeopleCandidate], candidate_aliases: dict[str, Any]) -> Any | None:
    payload = origin.payload or {}
    labels = [payload.get("owner_person_name"), payload.get("person_name"), payload.get("suggested_owner"), origin.unknown_owner_text]
    for label in labels:
        candidate = candidate_aliases.get(_normalize_alias(str(label or "")))
        if candidate:
            return candidate
    return candidates.get(origin.owner_ref or "")
