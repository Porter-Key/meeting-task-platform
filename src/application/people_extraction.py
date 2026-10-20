from __future__ import annotations

from typing import Any


def extract_people_from_meetings(meetings: list[dict[str, Any]], *, source: str = "fireflies_recent") -> list[dict[str, Any]]:
    by_name: dict[str, dict[str, Any]] = {}
    for meeting in meetings:
        payload = meeting.get("raw_payload") or meeting.get("payload") or meeting
        meeting_ref = {"meeting_id": meeting.get("meeting_id") or payload.get("id"), "title": meeting.get("title") or payload.get("title"), "date_string": meeting.get("date_string") or payload.get("dateString")}
        for person in people_from_fireflies_payload(payload):
            name = (person.get("display_name") or "").strip()
            if not name:
                continue
            existing = by_name.setdefault(name, {"display_name": name, "email": person.get("email"), "aliases": [], "source": source, "metadata": {"seen_in_meetings": []}})
            if not existing.get("email") and person.get("email"):
                existing["email"] = person.get("email")
            aliases = set(existing.get("aliases") or [])
            aliases.update(person.get("aliases") or [])
            aliases.discard(name)
            existing["aliases"] = sorted(aliases)
            seen = existing["metadata"].setdefault("seen_in_meetings", [])
            if meeting_ref not in seen:
                seen.append(meeting_ref)
    return list(by_name.values())


def people_from_fireflies_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    people: list[dict[str, Any]] = []
    for item in payload.get("participants") or []:
        if isinstance(item, str):
            people.extend(_people_from_string(item))
        elif isinstance(item, dict):
            people.extend(_people_from_dict(item))
    for speaker in payload.get("speakers") or []:
        if isinstance(speaker, str):
            people.extend(_people_from_string(speaker))
        elif isinstance(speaker, dict):
            people.extend(_people_from_dict(speaker))
    for key in ["host_email", "organizer_email"]:
        if payload.get(key):
            people.extend(_people_from_string(str(payload[key])))
    return people


def _people_from_dict(item: dict[str, Any]) -> list[dict[str, Any]]:
    email = item.get("email") or item.get("email_address")
    name = item.get("display_name") or item.get("name") or item.get("speaker_name") or item.get("speaker") or email
    emails = _split_values(str(email)) if email else []
    if len(emails) > 1 and (not name or name == email):
        return [_person_from_email(value) for value in emails]
    return [{"display_name": str(name or "").strip(), "email": emails[0] if emails else email, "aliases": emails if emails and emails[0] != name else []}]


def _people_from_string(value: str) -> list[dict[str, Any]]:
    return [_person_from_email(part) if "@" in part else {"display_name": part, "email": None, "aliases": []} for part in _split_values(value)]


def _person_from_email(value: str) -> dict[str, Any]:
    if "@" in value:
        name = value.split("@", 1)[0].replace(".", " ").replace("_", " ").title()
        return {"display_name": name, "email": value, "aliases": [value]}
    return {"display_name": value, "email": None, "aliases": []}


def _split_values(value: str) -> list[str]:
    return [part.strip() for part in value.replace(";", ",").split(",") if part.strip()]
