from __future__ import annotations

import re
from typing import Any

from django_client.uow import maybe_atomic

from application.event.fact_layer import build_people_candidates
from django_client.ids import new_id
from django_client.repositories import anonymous_email_for_name, normalize_alias
from domain.models.meeting import Meeting, MeetingChunk, MeetingPeopleCandidate, MeetingSource
from domain.models.people import Person, PersonAlias, PersonEmailAlias
from domain.models.task_masterlist import TaskOrigin
from external_client.llm.structured import with_structured_output

from .prompts import identity_normalization_prompt
from .schemas import IdentityNormalizationPlan, MeetingPeopleNormalizationResult, NormalizedPersonCandidate


ROLE_WORDS = {"owner", "reviewer", "access", "decision", "dashboard", "reporting", "listing", "workflow", "account", "pricing", "board", "server", "deployment", "data", "task", "tasks"}


class MeetingPeopleNormalizationService:
    def __init__(self, session_factory: Any | None = None, chat_model: Any | None = None) -> None:
        self.session_factory = session_factory
        self.identity_planner = with_structured_output(chat_model, IdentityNormalizationPlan) if chat_model is not None else None

    def normalize_meeting_people(self, meeting_id: str, *, apply: bool = True, confidence_threshold: float = 0.9) -> dict[str, Any]:
        with maybe_atomic():
            meeting = Meeting.objects.filter(id=meeting_id).first()
            if meeting is None:
                raise ValueError("meeting_not_found")
            chunks = list(MeetingChunk.objects.filter(meeting_id=meeting_id).order_by("chunk_index"))
            source = MeetingSource.objects.filter(meeting_id=meeting_id).order_by("-created_at").first()
            raw_candidates = build_people_candidates(_meeting_snapshot(meeting, source.raw_payload if source else {}), [_chunk_snapshot(row) for row in chunks])
            unknown_owners = [str(row.unknown_owner_text).strip() for row in TaskOrigin.objects.filter(meeting_id=meeting_id, unknown_owner_text__isnull=False) if str(row.unknown_owner_text or "").strip()]
            llm_plan = self._llm_plan(meeting_id=meeting_id, raw_candidates=raw_candidates, unknown_owners=unknown_owners)
            self._apply_plan_to_raw_candidates(raw_candidates, llm_plan)
            raw_candidates = _dedupe_candidates(raw_candidates)
            candidates: list[NormalizedPersonCandidate] = []
            rejected_roles: list[dict[str, Any]] = []
            review_required: list[dict[str, Any]] = []
            for item in raw_candidates:
                label = str(item.get("display_label") or item.get("email") or "").strip()
                if _is_role_label(label):
                    rejected_roles.append({"input": label, "reason": "role_label"})
                    continue
                email = self._resolve_email(item)
                if not email:
                    planned_anonymous = self._planned_anonymous(llm_plan, label)
                    if not planned_anonymous:
                        review_required.append({"input": label, "reason": "unresolved_email"})
                        continue
                    email = anonymous_email_for_name(label)
                    item.setdefault("aliases", []).append(label)
                    item.setdefault("sources", []).append("unknown_owner_text")
                confidence = float(item.get("confidence") or 1.0)
                review = confidence < confidence_threshold
                candidate = NormalizedPersonCandidate(ref=str(item.get("ref") or f"P{len(candidates) + 1}"), email=email, display_label=label or email, aliases=list(dict.fromkeys(item.get("aliases") or [label])), sources=list(dict.fromkeys(item.get("sources") or [])), confidence=confidence, review_required=review, metadata={"normalization_stage": "event_people_normalization"})
                candidates.append(candidate)
                if review:
                    review_required.append({"input": label, "email": email, "confidence": confidence, "reason": "below_threshold"})
            candidates = _dedupe_normalized_candidates(candidates)
            alias_links = 0
            if apply:
                MeetingPeopleCandidate.objects.filter(meeting_id=meeting_id).delete()
                self._apply_identity_plan(llm_plan)
                for idx, candidate in enumerate(candidates, start=1):
                    person, _ = Person.objects.get_or_create(email=candidate.email, defaults={"identity_type": "anonymous" if candidate.email.endswith("@anonymous.local") else "fireflies", "source": "people_normalization", "metadata_payload": {}})
                    alias_id = None
                    for alias in candidate.aliases:
                        alias_id = self._upsert_alias(alias=alias, email=candidate.email, confidence=candidate.confidence) or alias_id
                        alias_links += 1
                    MeetingPeopleCandidate.objects.create(id=new_id("candidate"), meeting_id=meeting_id, ref=f"P{idx}", email_id=candidate.email, alias_id=alias_id, identity_type=person.identity_type, display_label=candidate.display_label, sources=candidate.sources, confidence=candidate.confidence, metadata_payload={**candidate.metadata, "aliases": candidate.aliases, "review_required": candidate.review_required})
                    candidate.ref = f"P{idx}"
            return MeetingPeopleNormalizationResult(meeting_id=meeting_id, candidates=candidates, alias_links=alias_links, rejected_roles=rejected_roles, review_required=review_required, llm_plan=llm_plan).model_dump()

    def _llm_plan(self, *, meeting_id: str, raw_candidates: list[dict[str, Any]], unknown_owners: list[str]) -> dict[str, Any]:
        if self.identity_planner is None:
            return {"items": []}
        people = list(Person.objects.filter(is_active=True).order_by("email")[:200])
        aliases = list(PersonAlias.objects.order_by("-updated_at")[:300])
        email_aliases = list(PersonEmailAlias.objects.order_by("-updated_at")[:200])
        context = {
            "meeting_id": meeting_id,
            "primary_email_domain": "example.com",
            "raw_candidates": raw_candidates,
            "unknown_owner_texts": list(dict.fromkeys(unknown_owners)),
            "strong_merge_suggestions": _strong_merge_suggestions(raw_candidates, aliases),
            "people": [{"email": row.email, "identity_type": row.identity_type, "metadata": row.metadata_payload or {}} for row in people],
            "person_aliases": [{"alias": row.alias, "email": row.email_id, "confidence": row.confidence} for row in aliases],
            "person_email_aliases": [{"owner_email": row.owner_email_id, "alias_email": row.alias_email_id, "is_primary": row.is_primary} for row in email_aliases],
        }
        parsed = self.identity_planner.invoke([("system", "You normalize people identities and aliases."), ("human", identity_normalization_prompt(context))])
        return IdentityNormalizationPlan.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()

    def _apply_plan_to_raw_candidates(self, raw_candidates: list[dict[str, Any]], llm_plan: dict[str, Any]) -> None:
        for plan in llm_plan.get("items") or []:
            action = plan.get("action")
            target_email = str(plan.get("target_email") or plan.get("to_email") or "").strip().lower()
            alias = str(plan.get("alias") or plan.get("alias_email") or "").strip()
            if "@" in alias:
                target_email, alias = _prefer_primary_email(target_email, alias.lower())
            if action not in {"merge_alias", "email_alias", "merge_anonymous_into_real"} or not target_email or not alias:
                continue
            for item in raw_candidates:
                labels = [str(item.get("display_label") or ""), *[str(x) for x in item.get("aliases") or []]]
                emails = [str(item.get("email") or "").lower()]
                if any(normalize_alias(label) == normalize_alias(alias) for label in labels) or alias.lower() in emails or target_email in emails:
                    item["email"] = target_email
                    if "@" not in alias:
                        item.setdefault("aliases", []).append(alias)
                    else:
                        item.setdefault("email_aliases", []).append(alias.lower())
                    item.setdefault("sources", []).append("llm_identity_plan")
                    item["confidence"] = max(float(item.get("confidence") or 0.0), float(plan.get("confidence") or 0.0))

    def _planned_anonymous(self, llm_plan: dict[str, Any], label: str) -> bool:
        normalized = normalize_alias(label)
        for plan in llm_plan.get("items") or []:
            if plan.get("action") == "create_anonymous" and normalize_alias(str(plan.get("alias") or "")) == normalized:
                return True
        return False

    def _apply_identity_plan(self, llm_plan: dict[str, Any]) -> None:
        for plan in llm_plan.get("items") or []:
            action = plan.get("action")
            confidence = float(plan.get("confidence") or 0.0)
            if action == "merge_alias" and plan.get("target_email") and plan.get("alias") and confidence >= 0.75:
                target_email = str(plan["target_email"]).strip().lower()
                if "@" in str(plan["alias"]):
                    owner_email, alias_email = _prefer_primary_email(target_email, str(plan["alias"]).strip().lower())
                    self._upsert_email_alias(owner_email=owner_email, alias_email=alias_email, confidence=confidence)
                    continue
                Person.objects.get_or_create(email=target_email, defaults={"identity_type": "alias", "source": "people_normalization_llm", "metadata_payload": {}})
                self._upsert_alias(alias=str(plan["alias"]), email=target_email, confidence=confidence)
            elif action == "email_alias" and plan.get("target_email") and plan.get("alias_email") and confidence >= 0.75:
                owner_email, alias_email = _prefer_primary_email(str(plan["target_email"]).strip().lower(), str(plan["alias_email"]).strip().lower())
                self._upsert_email_alias(owner_email=owner_email, alias_email=alias_email, confidence=confidence)
                for alias in PersonAlias.objects.filter(email_id=alias_email):
                    alias.email_id = owner_email
                    alias.metadata_payload = {**(alias.metadata_payload or {}), "email_alias_owner": owner_email, "confidence": confidence}
                    alias.save(update_fields=["email", "metadata_payload"])
            elif action == "merge_anonymous_into_real" and plan.get("from_email") and plan.get("to_email") and confidence >= 0.75:
                from_email, to_email = _prefer_merge_direction(str(plan["from_email"]).strip().lower(), str(plan["to_email"]).strip().lower())
                self._merge_email(from_email=from_email, to_email=to_email, confidence=confidence)
            elif action == "create_anonymous" and plan.get("alias") and confidence >= 0.75:
                alias = str(plan["alias"])
                email = anonymous_email_for_name(alias)
                Person.objects.get_or_create(email=email, defaults={"identity_type": "anonymous", "source": "people_normalization_llm", "metadata_payload": {"source_name": alias}})
                self._upsert_alias(alias=alias, email=email, confidence=confidence)

    def _resolve_email(self, item: dict[str, Any]) -> str | None:
        email = str(item.get("email") or "").strip().lower() or None
        if email:
            return email
        for alias in item.get("aliases") or [item.get("display_label")]:
            normalized = normalize_alias(str(alias or ""))
            if not normalized:
                continue
            row = PersonAlias.objects.filter(normalized_alias=normalized).first()
            if row and row.email_id:
                return row.email_id
        return None

    def _upsert_alias(self, *, alias: str, email: str, confidence: float) -> str | None:
        normalized = normalize_alias(alias)
        if not normalized:
            return None
        row = PersonAlias.objects.filter(normalized_alias=normalized).first()
        if row is None:
            row = PersonAlias(id=new_id("alias"), alias=alias.strip(), normalized_alias=normalized)
        row.alias = alias.strip()
        row.email_id = email
        row.source = "people_normalization"
        row.confidence = confidence
        row.metadata_payload = {**(row.metadata_payload or {}), "normalized_from_meeting": True}
        row.save()
        return row.id

    def _upsert_email_alias(self, *, owner_email: str, alias_email: str, confidence: float) -> None:
        if owner_email == alias_email:
            return
        Person.objects.get_or_create(email=owner_email, defaults={"identity_type": "alias", "source": "people_normalization_llm", "metadata_payload": {}})
        Person.objects.get_or_create(email=alias_email, defaults={"identity_type": "alias", "source": "people_normalization_llm", "metadata_payload": {}})
        row = PersonEmailAlias.objects.filter(owner_email_id=owner_email, alias_email_id=alias_email).first()
        if row is None:
            row = PersonEmailAlias(id=new_id("email_alias"), owner_email_id=owner_email, alias_email_id=alias_email)
        row.source = "people_normalization_llm"
        row.metadata_payload = {**(row.metadata_payload or {}), "confidence": confidence}
        row.save()

    def _merge_email(self, *, from_email: str, to_email: str, confidence: float) -> None:
        if from_email == to_email:
            return
        Person.objects.get_or_create(email=to_email, defaults={"identity_type": "alias", "source": "people_normalization_llm", "metadata_payload": {}})
        for alias in PersonAlias.objects.filter(email_id=from_email):
            alias.email_id = to_email
            alias.metadata_payload = {**(alias.metadata_payload or {}), "merged_from_email": from_email, "confidence": confidence}
            alias.save(update_fields=["email", "metadata_payload"])
        self._upsert_email_alias(owner_email=to_email, alias_email=from_email, confidence=confidence)
        person = Person.objects.filter(email=from_email).first()
        if person:
            person.is_active = False
            person.metadata_payload = {**(person.metadata_payload or {}), "merged_to": to_email, "merge_confidence": confidence}
            person.save(update_fields=["is_active", "metadata_payload"])


def _is_primary_domain_email(email: str | None) -> bool:
    return str(email or "").strip().lower().endswith("@example.com")


def _prefer_primary_email(owner_email: str, alias_email: str) -> tuple[str, str]:
    owner_email = str(owner_email or "").strip().lower()
    alias_email = str(alias_email or "").strip().lower()
    if _is_primary_domain_email(alias_email) and not _is_primary_domain_email(owner_email):
        return alias_email, owner_email
    return owner_email, alias_email


def _prefer_merge_direction(from_email: str, to_email: str) -> tuple[str, str]:
    preferred_owner, alias_email = _prefer_primary_email(to_email, from_email)
    return alias_email, preferred_owner


def _meeting_snapshot(row: Meeting, raw_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    metadata = row.metadata_payload or {}
    raw_payload = raw_payload or {}
    attendees = _split_attendees(raw_payload.get("participants") or metadata.get("attendees") or metadata.get("participants") or [])
    for key in ["organizer_email", "host_email"]:
        if raw_payload.get(key):
            attendees.append(str(raw_payload[key]))
    return {"id": row.id, "meeting_id": row.id, "title": row.title, "started_at": row.started_at.isoformat() if row.started_at else None, "attendees": list(dict.fromkeys(attendees)), "source_system": "fireflies"}


def _split_attendees(raw: Any) -> list[str]:
    values = raw if isinstance(raw, list) else [raw]
    attendees: list[str] = []
    for value in values:
        for item in str(value or "").replace(";", ",").split(","):
            item = item.strip().lower()
            if item:
                attendees.append(item)
    return attendees


def _chunk_snapshot(row: MeetingChunk) -> dict[str, Any]:
    metadata = row.metadata_payload or {}
    return {"chunk_index": row.chunk_index, "speaker": metadata.get("speaker") or "", "text": row.text, "start_time": row.start_ms / 1000 if row.start_ms is not None else None}


def _is_role_label(value: str) -> bool:
    text = value.strip().lower()
    if "/" in text:
        return True
    words = set(re.findall(r"[a-z]+", text))
    return bool(words & ROLE_WORDS) and len(words) <= 5


def _strong_merge_suggestions(raw_candidates: list[dict[str, Any]], aliases: list[PersonAlias]) -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    alias_rows = [row for row in aliases if row.email_id and row.alias]
    for item in raw_candidates:
        email = str(item.get("email") or "").strip().lower()
        if not email:
            continue
        local = re.sub(r"\d+$", "", email.split("@", 1)[0].lower())
        local_key = re.sub(r"[^a-z]", "", local)
        for row in alias_rows:
            alias_words = re.findall(r"[a-z]+", row.alias.lower())
            if len(alias_words) < 2:
                continue
            first, last = alias_words[0], alias_words[-1]
            patterns = {f"{first[0]}{last}", f"{first}{last}", f"{first}.{last}", f"{first}-{last}"}
            compact_patterns = {re.sub(r"[^a-z]", "", p) for p in patterns}
            if local_key in compact_patterns and row.email_id != email:
                suggestions.append({"alias_email": email, "target_email": row.email_id, "alias": row.alias, "reason": "email_local_part_matches_initial_surname"})
    return suggestions


def _dedupe_candidates(raw_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for item in raw_candidates:
        email = str(item.get("email") or item.get("display_label") or "").strip().lower()
        if not email:
            continue
        existing = merged.setdefault(email, {**item, "aliases": [], "sources": []})
        existing["aliases"] = list(dict.fromkeys([*existing.get("aliases", []), *item.get("aliases", [])]))
        existing["sources"] = list(dict.fromkeys([*existing.get("sources", []), *item.get("sources", [])]))
        existing["confidence"] = max(float(existing.get("confidence") or 0.0), float(item.get("confidence") or 0.0))
    return list(merged.values())


def _dedupe_normalized_candidates(candidates: list[NormalizedPersonCandidate]) -> list[NormalizedPersonCandidate]:
    merged: dict[str, NormalizedPersonCandidate] = {}
    for candidate in candidates:
        existing = merged.get(candidate.email)
        if existing is None:
            merged[candidate.email] = candidate
            continue
        existing.aliases = list(dict.fromkeys([*existing.aliases, candidate.display_label, *candidate.aliases]))
        existing.sources = list(dict.fromkeys([*existing.sources, *candidate.sources]))
        existing.confidence = max(existing.confidence, candidate.confidence)
        existing.review_required = existing.review_required or candidate.review_required
        existing.metadata = {
            **existing.metadata,
            "merged_refs": list(dict.fromkeys([*(existing.metadata.get("merged_refs") or []), candidate.ref])),
            "merged_labels": list(dict.fromkeys([*(existing.metadata.get("merged_labels") or []), candidate.display_label])),
        }
    return list(merged.values())
