from __future__ import annotations

from typing import Any

from domain.models.people import Person


def upsert_meeting_person(payload: dict[str, Any], *, job_id: str | None = None) -> dict[str, Any]:
    email = str(payload.get("email") or payload.get("person_email") or "")
    if not email:
        return {"updated": False, "reason": "missing_email"}
    person, _ = Person.objects.update_or_create(email=email, defaults={"identity_type": payload.get("identity_type") or "person", "role": payload.get("role"), "is_active": True, "source": payload.get("source") or "manual", "metadata_payload": payload.get("metadata") or {}})
    return {"updated": True, "email": person.email}
