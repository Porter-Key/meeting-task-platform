from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


_DATE_PATTERN = re.compile(
    r"\b(?:"
    r"(?:Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|Sept|September|Oct|October|Nov|November|Dec|December)\s+\d{1,2}(?:,\s*\d{4})?"
    r"|\d{4}-\d{2}-\d{2}"
    r"|\d{1,2}/\d{1,2}(?:/\d{2,4})?"
    r")\b",
    re.IGNORECASE,
)
_TIME_PATTERN = re.compile(r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm)\b|\b\d{1,2}:\d{2}\b", re.IGNORECASE)
_MONEY_PATTERN = re.compile(r"\$\d[\d,]*(?:\.\d+)?|\bUSD\s?\d[\d,]*(?:\.\d+)?\b", re.IGNORECASE)
_PERCENT_PATTERN = re.compile(r"\b\d+(?:\.\d+)?%\b")
_DURATION_PATTERN = re.compile(r"\b\d+(?:\.\d+)?\s?(?:minutes?|hours?|days?|weeks?)\b", re.IGNORECASE)
_COUNT_PATTERN = re.compile(r"\b\d[\d,]*(?:\.\d+)?\b")
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ROLE_WORDS = {"owner", "reviewer", "access", "decision", "dashboard", "reporting", "listing", "workflow", "account", "pricing", "board", "server", "deployment", "data", "task", "tasks", "person", "people"}


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _metadata_value(meeting: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = meeting.get(key)
        if value not in (None, "", []):
            return value
    return None


def _normalize_date_value(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    if text.isdigit():
        raw = int(text)
        seconds = raw / 1000 if raw > 10_000_000_000 else raw
        try:
            return datetime.fromtimestamp(seconds, tz=timezone.utc).date().isoformat()
        except (OverflowError, ValueError):
            return text
    return text


def _meeting_metadata(meeting: dict[str, Any]) -> dict[str, Any]:
    raw_attendees = _metadata_value(meeting, "attendees", "participants", "speakers") or []
    if isinstance(raw_attendees, str):
        attendees = [item.strip() for item in raw_attendees.split(",") if item.strip()]
    else:
        attendees = [str(item).strip() for item in raw_attendees if str(item).strip()]
    return {
        "meeting_id": _clean(meeting.get("id") or meeting.get("meeting_id")),
        "title": _clean(meeting.get("title")),
        "date": _normalize_date_value(_metadata_value(meeting, "date", "meeting_date", "scheduled_date", "started_date")),
        "start_time": _clean(_metadata_value(meeting, "start_time", "started_at", "start_at")) or None,
        "end_time": _clean(_metadata_value(meeting, "end_time", "ended_at", "end_at")) or None,
        "attendees": attendees,
        "organizer": _clean(_metadata_value(meeting, "organizer", "host", "owner")) or None,
        "language": _clean(_metadata_value(meeting, "language", "locale")) or None,
        "source_system": _clean(_metadata_value(meeting, "source_system", "source", "provider")) or None,
    }


def _normalize_name(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _looks_like_email(value: str) -> bool:
    return bool(_EMAIL_PATTERN.match(value.strip().lower()))


def _looks_like_person_name(value: str) -> bool:
    text = _normalize_name(value)
    if not text or _looks_like_email(text) or "/" in text:
        return False
    words = [word.strip(".,:;()[]{}\"'") for word in text.split() if word.strip(".,:;()[]{}\"'")]
    if not (1 <= len(words) <= 4):
        return False
    lower_words = {word.lower() for word in words}
    if lower_words & _ROLE_WORDS:
        return False
    return any(word[:1].isupper() for word in words) or len(words) >= 2


def build_people_candidates(meeting: dict[str, Any], chunks: list[dict[str, Any]], *, max_candidates: int = 12) -> list[dict[str, Any]]:
    metadata = _meeting_metadata(meeting)
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    by_key: dict[str, dict[str, Any]] = {}
    attendee_emails = [str(item).strip().lower() for item in metadata.get("attendees") or [] if _looks_like_email(str(item))]

    def matching_attendee_email(name: str) -> str | None:
        words = {word.lower() for word in re.findall(r"[a-zA-Z]+", name)}
        if not words:
            return None
        for email in attendee_emails:
            local = email.split("@", 1)[0].lower()
            local_tokens = {token for token in re.split(r"[^a-z]+", local) if token}
            if local in words or words & local_tokens:
                return email
            if any(token and any(word.startswith(token) or token.startswith(word) for word in words) for token in local_tokens):
                return email
        return None

    def add(label: str, *, email: str | None = None, sources: list[str] | None = None, confidence: float = 1.0) -> None:
        display = _normalize_name(label or email)
        normalized_email = str(email or "").strip().lower() or None
        if not normalized_email and display:
            normalized_email = matching_attendee_email(display)
        key = normalized_email or display.lower()
        if not display:
            return
        if not normalized_email and not _looks_like_person_name(display):
            return
        if key in seen:
            existing = by_key.get(key)
            if existing:
                aliases = existing.setdefault("aliases", [])
                if display not in aliases:
                    aliases.append(display)
                existing_sources = existing.setdefault("sources", [])
                for source in sources or []:
                    if source not in existing_sources:
                        existing_sources.append(source)
            return
        if len(candidates) >= max_candidates:
            return
        seen.add(key)
        candidate = {"ref": f"P{len(candidates) + 1}", "display_label": display, "email": normalized_email, "aliases": [display], "sources": sources or [], "confidence": confidence}
        candidates.append(candidate)
        by_key[key] = candidate

    for attendee in metadata.get("attendees") or []:
        attendee_text = _normalize_name(attendee)
        add(attendee_text, email=attendee_text if _looks_like_email(attendee_text) else None, sources=["meeting_attendee"], confidence=1.0)
    if metadata.get("organizer"):
        organizer = _normalize_name(metadata["organizer"])
        add(organizer, email=organizer if _looks_like_email(organizer) else None, sources=["meeting_organizer"], confidence=1.0)
    for chunk in chunks:
        speaker = _normalize_name(chunk.get("speaker"))
        if speaker:
            add(speaker, email=speaker if _looks_like_email(speaker) else None, sources=["speaker_name"], confidence=0.9)
    return candidates


def _chunk_snippet(text: str, start: int, end: int, window: int = 24) -> str:
    left = max(0, start - window)
    right = min(len(text), end + window)
    return text[left:right].strip()


def _make_fact(fact_id: str, fact_type: str, value: str, source_text: str, source_chunk_indexes: list[int], *, normalized_value: str | None = None, speaker_turns: list[int] | None = None, timestamp: str | None = None, confidence: float = 0.95) -> dict[str, Any]:
    return {
        "fact_id": fact_id,
        "fact_type": fact_type,
        "value": value,
        "normalized_value": normalized_value or value,
        "source_text": source_text,
        "source_chunk_indexes": source_chunk_indexes,
        "speaker_turns": speaker_turns or [],
        "timestamp": timestamp,
        "confidence": confidence,
    }


def build_fact_layer(meeting: dict[str, Any], chunks: list[dict[str, Any]], *, max_facts: int = 50, include_speakers: bool = False) -> dict[str, Any]:
    metadata = _meeting_metadata(meeting)
    people_candidates = build_people_candidates(meeting, chunks)
    facts: list[dict[str, Any]] = []

    for field in ["meeting_id", "title", "date", "start_time", "end_time", "organizer", "language", "source_system"]:
        value = metadata.get(field)
        if value:
            if len(facts) >= max_facts:
                return {"meeting_metadata": metadata, "people_candidates": people_candidates, "facts": facts}
            facts.append(
                _make_fact(
                    f"meta_{field}",
                    "meeting_metadata",
                    str(value),
                    str(value),
                    [],
                    normalized_value=str(value),
                    confidence=1.0,
                )
            )
    if metadata.get("attendees"):
        for idx, attendee in enumerate(metadata["attendees"]):
            if len(facts) >= max_facts:
                return {"meeting_metadata": metadata, "people_candidates": people_candidates, "facts": facts}
            facts.append(
                _make_fact(
                    f"meta_attendee_{idx}",
                    "meeting_attendee",
                    attendee,
                    attendee,
                    [],
                    normalized_value=attendee,
                    confidence=1.0,
                )
            )

    for chunk in chunks:
        chunk_index = int(chunk.get("chunk_index") or 0)
        speaker = _clean(chunk.get("speaker"))
        text = _clean(chunk.get("text"))
        if not text:
            continue
        speaker_turn = chunk_index if str(chunk.get("chunk_index")).isdigit() else None
        patterns = [
            ("date", _DATE_PATTERN),
            ("time", _TIME_PATTERN),
            ("money", _MONEY_PATTERN),
            ("percent", _PERCENT_PATTERN),
            ("duration", _DURATION_PATTERN),
        ]
        local_count = 0
        for fact_type, pattern in patterns:
            for match in pattern.finditer(text):
                if len(facts) >= max_facts:
                    return {"meeting_metadata": metadata, "people_candidates": people_candidates, "facts": facts}
                value = match.group(0).strip()
                if not value:
                    continue
                source_text = _chunk_snippet(text, match.start(), match.end())
                facts.append(
                    _make_fact(
                        f"chunk_{chunk_index}_{fact_type}_{local_count}",
                        fact_type,
                        value,
                        source_text,
                        [chunk_index],
                        speaker_turns=[speaker_turn] if speaker_turn is not None else [],
                        timestamp=_clean(chunk.get("start_time")) or None,
                    )
                )
                local_count += 1
        if include_speakers and speaker:
            if len(facts) >= max_facts:
                return {"meeting_metadata": metadata, "people_candidates": people_candidates, "facts": facts}
            facts.append(
                _make_fact(
                    f"chunk_{chunk_index}_speaker",
                    "speaker",
                    speaker,
                    f"{speaker}: {text[:120]}",
                    [chunk_index],
                    speaker_turns=[speaker_turn] if speaker_turn is not None else [],
                    timestamp=_clean(chunk.get("start_time")) or None,
                    confidence=0.9,
                )
            )

    return {"meeting_metadata": metadata, "people_candidates": people_candidates, "facts": facts}


def render_fact_layer(fact_layer: dict[str, Any], *, max_facts: int = 12) -> str:
    metadata = fact_layer.get("meeting_metadata") or {}
    facts = fact_layer.get("facts") or []
    lines = [
        f"meeting_id={metadata.get('meeting_id') or ''}",
        f"title={metadata.get('title') or ''}",
    ]
    for field in ["date", "start_time", "end_time", "organizer", "language", "source_system"]:
        value = metadata.get(field)
        if value:
            lines.append(f"{field}={value}")
    attendees = metadata.get("attendees") or []
    if attendees:
        lines.append(f"attendees={', '.join(attendees[:6])}")
    people_candidates = fact_layer.get("people_candidates") or []
    if people_candidates:
        lines.append("PEOPLE_CANDIDATES:")
        for candidate in people_candidates[:12]:
            aliases = ", ".join((candidate.get("aliases") or [])[:4])
            email = candidate.get("email") or "unresolved-email"
            lines.append(f"- {candidate.get('ref')}: {candidate.get('display_label')} | email={email} | aliases={aliases} | sources={', '.join(candidate.get('sources') or [])}")
    for fact in facts[:max_facts]:
        chunk_indexes = fact.get("source_chunk_indexes") or []
        prefix = f"[{fact.get('fact_type')}]"
        if chunk_indexes:
            prefix = f"[c{','.join(str(idx) for idx in chunk_indexes[:3])}] {prefix}"
        lines.append(f"{prefix} {fact.get('value')} | {fact.get('source_text')}")
    return "\n".join(lines)
