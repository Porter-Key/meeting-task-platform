from __future__ import annotations

import re
from typing import Any

from domain.models.people import Person, PersonAlias, PersonEmailAlias
from .ids import new_id
from .uow import atomic

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def upsert_person(*, email: str, identity_type: str = "alias", role: str | None = None, is_active: bool = True, source: str = "manual", metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    normalized = email.strip().lower()
    with atomic():
        row, _ = Person.objects.update_or_create(email=normalized, defaults={"identity_type": identity_type, "role": role, "is_active": is_active, "source": source, "metadata_payload": metadata or {}})
        return dump_person(row)


def upsert_alias(*, alias: str, email: str | None = None, source: str = "manual", confidence: float = 1.0, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    normalized_alias = " ".join(alias.strip().lower().split())
    normalized_email = email.strip().lower() if email else None
    with atomic():
        if normalized_email:
            Person.objects.get_or_create(email=normalized_email, defaults={"identity_type": "alias", "source": source, "metadata_payload": {}})
        row, _ = PersonAlias.objects.get_or_create(normalized_alias=normalized_alias, defaults={"id": new_id("alias"), "alias": alias.strip()})
        row.alias = alias.strip()
        row.email_id = normalized_email or row.email_id
        row.source = source
        row.confidence = confidence
        row.metadata_payload = {**(row.metadata_payload or {}), **(metadata or {})}
        row.save()
        return dump_alias(row)


def add_email_alias(*, owner_email: str, alias_email: str, is_primary: bool = False, source: str = "manual", metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    owner = owner_email.strip().lower()
    alias = alias_email.strip().lower()
    with atomic():
        Person.objects.get_or_create(email=owner, defaults={"identity_type": "alias", "source": source, "metadata_payload": {}})
        Person.objects.get_or_create(email=alias, defaults={"identity_type": "alias", "source": source, "metadata_payload": {}})
        row, _ = PersonEmailAlias.objects.get_or_create(owner_email_id=owner, alias_email_id=alias, defaults={"id": new_id("email_alias")})
        row.is_primary = is_primary
        row.source = source
        row.metadata_payload = metadata or row.metadata_payload or {}
        row.save()
        return {"id": row.id, "owner_email": row.owner_email_id, "alias_email": row.alias_email_id, "is_primary": row.is_primary, "source": row.source, "metadata_payload": row.metadata_payload or {}}


def normalize_email(value: Any) -> str:
    return str(value or "").strip().lower()


def is_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value or ""))


def canonical_person_email(value: Any) -> str | None:
    """Return canonical people.email for Person/FK/raw/alias values.

    This is the django_client boundary for email primitives: callers outside the
    client should receive/write plain canonical email strings, not Django model
    objects or FK reprs.
    """
    if value in (None, ""):
        return None
    email = getattr(value, "email", value)
    email = normalize_email(email)
    if not is_email(email):
        match = re.search(r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})", email, re.IGNORECASE)
        email = normalize_email(match.group(1)) if match else email
    if not is_email(email):
        return None
    alias = PersonEmailAlias.objects.filter(alias_email_id=email).order_by("-is_primary", "-updated_at").first()
    return str(alias.owner_email_id) if alias else email


def dump_person(row: Person) -> dict[str, Any]:
    return {"email": row.email, "identity_type": row.identity_type, "role": row.role, "is_active": row.is_active, "source": row.source, "metadata_payload": row.metadata_payload or {}}


def dump_alias(row: PersonAlias) -> dict[str, Any]:
    return {"id": row.id, "alias": row.alias, "normalized_alias": row.normalized_alias, "email": row.email_id, "source": row.source, "confidence": row.confidence, "metadata_payload": row.metadata_payload or {}}
