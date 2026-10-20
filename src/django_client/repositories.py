from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any

from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils import timezone

from domain.models.logs import ApplicationLog
from domain.models.meeting import Meeting, MeetingChunk, MeetingConclusion, MeetingPeopleCandidate, MeetingPipelineRun, MeetingSource, MeetingTopic, MeetingTranscript
from domain.models.people import Person, PersonAlias
from domain.models.task_masterlist import TaskAssigneeLink, TaskExternalLink, TaskMasterlist, TaskOrigin, TaskVersion
from django_client.ids import new_id
from django_client.people import canonical_person_email
from django_client.uow import atomic

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ANONYMOUS_DOMAIN = "anonymous.local"


@dataclass(slots=True)
class Repositories:
    meeting: "MeetingRepo"
    topic: "TopicRepo"
    conclusion: "MeetingConclusionRepo"
    lifecycle: "LifecycleRepo"
    logs: "LogRepo"
    people: "PersonRepo"
    task_masterlist: "TaskMasterlistRepo"
    meeting_graph: "NoopMeetingGraphRepo"


def repositories() -> Repositories:
    return Repositories(MeetingRepo(), TopicRepo(), MeetingConclusionRepo(), LifecycleRepo(), LogRepo(), PersonRepo(), TaskMasterlistRepo(), NoopMeetingGraphRepo())


class LogRepo:
    def write(self, *, level: str, logger_name: str, event: str, message: str = "", stage: str = "", correlation_id: str | None = None, meeting_id: str | None = None, payload: dict[str, Any] | None = None) -> str:
        log_id = new_id("log")
        ApplicationLog.objects.create(id=log_id, level=level.upper(), logger_name=logger_name, stage=stage, event=event, message=message, correlation_id=correlation_id, meeting_id=meeting_id, payload=_jsonable(payload or {}))
        return log_id

    def info(self, event: str, message: str = "", **payload: Any) -> str:
        return self.write(level="INFO", logger_name="application", event=event, message=message, stage=str(payload.pop("stage", "")), correlation_id=payload.pop("correlation_id", None), meeting_id=payload.pop("meeting_id", None), payload=payload)

    def error(self, event: str, message: str = "", **payload: Any) -> str:
        return self.write(level="ERROR", logger_name="application", event=event, message=message, stage=str(payload.pop("stage", "")), correlation_id=payload.pop("correlation_id", None), meeting_id=payload.pop("meeting_id", None), payload=payload)

    def trace_call(self, event: str, *, input: Any | None = None, output: Any | None = None, **payload: Any) -> str:
        if input is not None:
            payload["input"] = input
        if output is not None:
            payload["output"] = output
        return self.write(level="DEBUG", logger_name="application", event=event, message=event, stage=str(payload.pop("stage", "")), correlation_id=payload.pop("correlation_id", None), meeting_id=payload.pop("meeting_id", None), payload=payload)


class LifecycleRepo:
    def latest_meeting_status(self, meeting_id: str, stage: str) -> str | None:
        row = MeetingPipelineRun.objects.filter(meeting_id=meeting_id, stage=stage).order_by("-created_at").first()
        return row.status if row else None

    def mark(self, meeting_id: str, stage: str, *, status: str = "completed", job_id: str | None = None, metadata: dict[str, Any] | None = None, error: str | None = None, decision: Any | None = None) -> None:
        payload = dict(metadata or {})
        if decision is not None:
            payload["domain_decision"] = decision.model_dump() if hasattr(decision, "model_dump") else decision
        now = timezone.now()
        MeetingPipelineRun.objects.create(id=new_id("run"), meeting_id=meeting_id, pipeline_name=_pipeline_name(stage), stage=stage, status=status, job_id=job_id, started_at=now, finished_at=now if status not in {"running", "queued"} else None, error=error, metadata_payload=payload)

    def mark_meeting_running(self, meeting_id: str, stage: str, **kwargs: Any) -> None:
        self.mark(meeting_id, stage, status="running", **kwargs)

    def mark_meeting_completed(self, meeting_id: str, stage: str, **kwargs: Any) -> None:
        self.mark(meeting_id, stage, status="completed", **kwargs)

    def change_state(self, subject_type: str, subject_id: str, *, stage: str, status: str, metadata: dict[str, Any] | None = None, error: str | None = None, decision: Any | None = None) -> None:
        if subject_type == "meeting":
            self.mark(subject_id, stage, status=status, metadata=metadata, error=error, decision=decision)


class MeetingRepo:
    def upsert_raw_meeting(self, transcript: dict[str, Any]) -> str:
        meeting_id = str(transcript["id"])
        with atomic():
            meeting, _ = Meeting.objects.update_or_create(id=meeting_id, defaults={"title": transcript.get("title") or "", "started_at": _parse_meeting_datetime(transcript), "duration_seconds": _duration_seconds(transcript.get("duration")), "metadata_payload": {"fireflies_date_string": transcript.get("dateString")}})
            source = MeetingSource.objects.filter(provider="fireflies", provider_record_id=meeting_id).first()
            if source is None:
                source = MeetingSource(id=new_id("src"), meeting=meeting, provider="fireflies", provider_record_id=meeting_id)
            source.meeting = meeting
            source.provider_url = transcript.get("transcript_url")
            source.raw_payload = transcript
            source.sync_status = "synced"
            source.synced_at = timezone.now()
            source.metadata_payload = {"summary_status": (transcript.get("meeting_info") or {}).get("summary_status")}
            source.save()
            transcript_row = MeetingTranscript.objects.filter(meeting=meeting, source=source).first()
            if transcript_row is None:
                transcript_row = MeetingTranscript(id=new_id("transcript"), meeting=meeting, source=source, format="fireflies_sentences")
            transcript_row.content = _transcript_text(transcript)
            transcript_row.segments = transcript.get("sentences") or []
            transcript_row.language = transcript.get("language") or transcript.get("locale")
            transcript_row.metadata_payload = {"sentence_count": len(transcript.get("sentences") or [])}
            transcript_row.save()
        return meeting_id

    def get_raw_meeting(self, meeting_id: str) -> dict[str, Any] | None:
        row = MeetingSource.objects.filter(meeting_id=meeting_id).order_by("-created_at").first()
        return dict(row.raw_payload) if row else None

    def replace_chunks(self, meeting_id: str, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        saved: list[dict[str, Any]] = []
        with atomic():
            transcript = MeetingTranscript.objects.filter(meeting_id=meeting_id).order_by("-created_at").first()
            MeetingChunk.objects.filter(meeting_id=meeting_id).delete()
            for chunk in chunks:
                row = MeetingChunk.objects.create(id=new_id("chunk"), meeting_id=meeting_id, transcript=transcript, chunk_index=int(chunk.get("chunk_index") or 0), text=chunk.get("text") or "", start_ms=_seconds_to_ms(chunk.get("start_time")), end_ms=_seconds_to_ms(chunk.get("end_time")), metadata_payload={"speaker": chunk.get("speaker") or "", "sentence_indexes": chunk.get("sentence_indexes") or [], "ai_filters": chunk.get("ai_filters") or []})
                saved.append({**chunk, "id": row.id})
        return saved

    def get_meeting_with_chunks(self, meeting_id: str) -> dict[str, Any] | None:
        meeting = Meeting.objects.filter(id=meeting_id).first()
        if not meeting:
            return None
        return {"meeting_id": meeting.id, "title": meeting.title, "chunks": [self._chunk_snapshot(row) for row in MeetingChunk.objects.filter(meeting_id=meeting_id).order_by("chunk_index")]}

    def list_meeting_ids(self) -> list[str]:
        return list(Meeting.objects.values_list("id", flat=True))

    def list_existing_transcript_ids(self, meeting_ids: list[str]) -> set[str]:
        ids = list(dict.fromkeys(str(meeting_id) for meeting_id in meeting_ids if meeting_id))
        return set(MeetingTranscript.objects.filter(meeting_id__in=ids, content__isnull=False).values_list("meeting_id", flat=True)) if ids else set()

    def clear_generated_artifacts(self, meeting_id: str, *, clear_chunks: bool = False) -> dict[str, int]:
        with atomic():
            origin_ids = list(TaskOrigin.objects.filter(meeting_id=meeting_id).values_list("id", flat=True))
            task_query = TaskMasterlist.objects.filter(Q(metadata_payload__meeting_id=meeting_id) | Q(origin_id__in=origin_ids))
            task_ids = list(task_query.values_list("id", flat=True))
            counts = {"task_external_links": TaskExternalLink.objects.filter(masterlist_task_id__in=task_ids).delete()[0] if task_ids else 0, "task_versions": TaskVersion.objects.filter(masterlist_task_id__in=task_ids).delete()[0] if task_ids else 0, "task_assignee_links": TaskAssigneeLink.objects.filter(masterlist_task_id__in=task_ids).delete()[0] if task_ids else 0, "task_masterlist": task_query.delete()[0] if task_ids else 0, "task_origins": TaskOrigin.objects.filter(meeting_id=meeting_id).delete()[0], "people_candidates": MeetingPeopleCandidate.objects.filter(meeting_id=meeting_id).delete()[0], "conclusions": MeetingConclusion.objects.filter(meeting_id=meeting_id).delete()[0], "topics": MeetingTopic.objects.filter(meeting_id=meeting_id).delete()[0], "chunks": 0}
            if clear_chunks:
                counts["chunks"] = MeetingChunk.objects.filter(meeting_id=meeting_id).delete()[0]
        return counts

    def _chunk_snapshot(self, row: MeetingChunk) -> dict[str, Any]:
        metadata = row.metadata_payload or {}
        return {"id": row.id, "chunk_id": row.id, "meeting_id": row.meeting_id, "chunk_index": row.chunk_index, "speaker": metadata.get("speaker") or "", "speaker_alias_id": row.speaker_alias_id, "start_time": _ms_to_seconds(row.start_ms), "end_time": _ms_to_seconds(row.end_ms), "sentence_indexes": metadata.get("sentence_indexes") or [], "text": row.text, "ai_filters": metadata.get("ai_filters") or [], "metadata": metadata}


class TopicRepo:
    def replace_topics(self, meeting_id: str, topics: list[dict[str, Any]]) -> list[dict[str, Any]]:
        saved = []
        with atomic():
            MeetingTopic.objects.filter(meeting_id=meeting_id).delete()
            for index, topic in enumerate(topics):
                topic_id = topic.get("local_topic_id") or topic.get("id") or new_id("topic")
                MeetingTopic.objects.create(id=topic_id, meeting_id=meeting_id, topic_index=index, title=topic.get("title") or "", summary=topic.get("summary") or "", source_chunk_indexes=topic.get("representative_chunk_indexes") or topic.get("chunk_indexes") or [], confidence=float(topic.get("confidence") or 0.0), payload=topic)
                saved.append({**topic, "id": topic_id, "local_topic_id": topic_id, "topic_index": index})
        return saved

    def replace_meeting_events(self, meeting_id: str, meeting_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return meeting_events


class MeetingConclusionRepo:
    def replace_for_meeting(self, meeting_id: str, conclusion: dict[str, Any]) -> dict[str, Any]:
        with atomic():
            TaskOrigin.objects.filter(meeting_id=meeting_id).delete()
            MeetingPeopleCandidate.objects.filter(meeting_id=meeting_id).delete()
            MeetingConclusion.objects.filter(meeting_id=meeting_id).delete()
            conclusion_id = new_id("conclusion")
            MeetingConclusion.objects.create(id=conclusion_id, meeting_id=meeting_id, title=conclusion.get("title") or "", summary=conclusion.get("summary") or "", one_sentence_summary=conclusion.get("one_sentence_summary"), tl_dr=conclusion.get("tl_dr") or [], source_topic_indexes=conclusion.get("source_topic_indexes") or [], source_chunk_indexes=conclusion.get("source_chunk_indexes") or [], confidence=float(conclusion.get("confidence") or 0.0), payload=conclusion)
            candidates = self._persist_fact_candidates(meeting_id, conclusion)
            aliases = self._candidate_alias_index(candidates)
            origin_count = 0
            for group in conclusion.get("people_tasks") or []:
                owner_ref = self._resolve_owner_ref(group, candidates, aliases) or group.get("owner_ref")
                candidate = candidates.get(owner_ref or "")
                owner_email = canonical_person_email(candidate.email_id) if candidate else None
                owner_alias_id = candidate.alias_id if candidate else None
                unknown_owner_text = None if candidate else (group.get("unknown_owner_text") or group.get("suggested_owner") or group.get("person_name"))
                for task in group.get("tasks") or []:
                    task_owner_ref = self._resolve_owner_ref(task, candidates, aliases) or owner_ref
                    task_candidate = candidates.get(task_owner_ref or "") if task_owner_ref else candidate
                    owner_email_id = canonical_person_email(task_candidate.email_id) if task_candidate else owner_email
                    TaskOrigin.objects.create(id=new_id("origin"), origin_type="meeting_conclusion", meeting_id=meeting_id, conclusion_id=conclusion_id, title=task.get("title") or "", action=task.get("action") or "", context=task.get("context") or task.get("description") or "", priority=task.get("priority") or "medium", owner_ref=task_owner_ref if task_candidate else owner_ref, owner_email_id=owner_email_id, owner_alias_id=task_candidate.alias_id if task_candidate else owner_alias_id, unknown_owner_text=task.get("unknown_owner_text") or unknown_owner_text, assignment_reason=group.get("assignment_reason") or task.get("assignment_reason"), source_topic_indexes=task.get("source_topic_indexes") or [], source_chunk_indexes=task.get("source_chunk_indexes") or [], source_quote=task.get("source_quote") or task.get("context") or task.get("action") or "", payload={**task, "owner_ref": task_owner_ref if task_candidate else owner_ref, "owner_email": owner_email_id, "unknown_owner_text": task.get("unknown_owner_text") or unknown_owner_text})
                    origin_count += 1
        return {"conclusion_id": conclusion_id, "task_origins": origin_count, "people_tasks": origin_count}

    def _persist_fact_candidates(self, meeting_id: str, conclusion: dict[str, Any]) -> dict[str, MeetingPeopleCandidate]:
        candidates: dict[str, MeetingPeopleCandidate] = {}
        by_email: dict[str, MeetingPeopleCandidate] = {}
        for item in ((conclusion.get("fact_layer") or {}).get("people_candidates") or []):
            value = str(item.get("display_label") or item.get("email") or "").strip()
            if not value:
                continue
            email = canonical_person_email(item.get("email"))
            alias_id = _alias_id(value)
            alias = PersonAlias.objects.filter(id=alias_id).first() if alias_id else None
            if not email and alias and alias.email_id:
                email = canonical_person_email(alias.email_id)
            sources = item.get("sources") or ["fact_layer"]
            if not email:
                email = anonymous_email_for_name(value)
                Person.objects.get_or_create(email=email, defaults={"identity_type": "anonymous", "source": "anonymous_generated", "metadata_payload": {"source_name": value, "meeting_id": meeting_id}})
                if alias:
                    alias.email_id = email
                    alias.save(update_fields=["email"])
                identity_type = "anonymous"
                sources = [*sources, "anonymous_generated"]
            else:
                person, _ = Person.objects.get_or_create(email=email, defaults={"identity_type": "anonymous" if email.endswith("@anonymous.local") else "fireflies", "source": "fact_layer", "metadata_payload": {"source_name": value, "meeting_id": meeting_id}})
                identity_type = person.identity_type
            ref = str(item.get("ref") or f"P{len(by_email) + 1}")
            if email in by_email:
                candidates[ref] = by_email[email]
                continue
            candidate = MeetingPeopleCandidate.objects.create(id=new_id("candidate"), meeting_id=meeting_id, ref=ref, email_id=email, alias_id=alias_id, identity_type=identity_type, display_label=value, sources=sources, confidence=float(item.get("confidence") or (0.7 if identity_type == "anonymous" else 1.0)), metadata_payload={"generated_from": "fact_layer", "aliases": item.get("aliases") or []})
            by_email[email] = candidate
            candidates[ref] = candidate
        return candidates

    def _candidate_alias_index(self, candidates: dict[str, MeetingPeopleCandidate]) -> dict[str, str]:
        index: dict[str, str] = {}
        for candidate in candidates.values():
            labels = [candidate.display_label, candidate.email_id, *((candidate.metadata_payload or {}).get("aliases") or [])]
            for value in labels:
                normalized = normalize_alias(str(value or ""))
                if normalized:
                    index[normalized] = candidate.ref
        return index

    def _resolve_owner_ref(self, item: dict[str, Any], candidates: dict[str, MeetingPeopleCandidate], candidate_aliases: dict[str, str]) -> str | None:
        current = str(item.get("owner_ref") or "")
        for label in [item.get("owner_person_name"), item.get("person_name"), item.get("suggested_owner")]:
            resolved = candidate_aliases.get(normalize_alias(str(label or "")))
            if resolved:
                return resolved
        return candidates[current].ref if current in candidates else None


class PersonRepo:
    def upsert_many(self, people: list[dict[str, Any]]) -> dict[str, Any]:
        upserted: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []
        for person in people:
            try:
                email = normalize_email(person.get("email") or "")
                if not is_email(email):
                    raise ValueError("email_required")
                row, _ = Person.objects.update_or_create(email=email, defaults={"identity_type": person.get("identity_type") or ("fireflies" if person.get("source") == "fireflies_ingest" else "alias"), "source": person.get("source") or "ingest", "metadata_payload": person.get("metadata") or {}})
                for alias in person.get("aliases") or []:
                    _upsert_alias(alias=alias, email=email, source=person.get("source") or "ingest", metadata=person.get("metadata") or {})
                upserted.append({"email": row.email, "identity_type": row.identity_type})
            except ValueError as exc:
                alias = person.get("alias") or person.get("display_name") or person.get("name")
                if alias:
                    _upsert_alias(alias=alias, email=None, source=person.get("source") or "unresolved", metadata=person.get("metadata") or {})
                skipped.append({"alias": alias or person.get("email"), "reason": str(exc)})
        return {"upserted": len(upserted), "people": upserted, "skipped": skipped}


class TaskMasterlistRepo:
    def sync_from_meeting(self, *, meeting_id: str, task_date: date | None = None) -> dict[str, Any]:
        created = 0
        with atomic():
            meeting = Meeting.objects.filter(id=meeting_id).first()
            resolved_date = task_date or (meeting.started_at.date() if meeting and meeting.started_at else timezone.now().date())
            for origin in TaskOrigin.objects.filter(meeting_id=meeting_id).order_by("created_at"):
                if TaskMasterlist.objects.filter(origin_id=origin.id).exists():
                    continue
                row = TaskMasterlist.objects.create(id=new_id("task"), task_date=resolved_date, title=origin.title, action=origin.action, context=origin.context, priority=origin.priority, status="draft", origin_id=origin.id, origin_type=origin.origin_type, version=1, metadata_payload={"meeting_id": meeting_id, "archived_columns": {"due_date": "deprecated_use_monday_field_values", "due_note": "deprecated_use_monday_field_values"}})
                if origin.owner_email_id or origin.owner_alias_id:
                    alias = PersonAlias.objects.filter(id=origin.owner_alias_id).first() if origin.owner_alias_id else None
                    email_id = canonical_person_email(origin.owner_email_id) or canonical_person_email(alias.email_id if alias else None)
                    TaskAssigneeLink.objects.create(id=new_id("assignee"), masterlist_task=row, email_id=email_id, alias_id=origin.owner_alias_id, relation="assignee", source="origin", confidence=0.7, metadata_payload={"origin_id": origin.id, "owner_ref": origin.owner_ref, "resolution_method": "fact_candidate" if origin.owner_ref else "alias"})
                TaskVersion.objects.create(id=new_id("version"), masterlist_task=row, version=1, change_type="initialized", changed_by="system", changed_at=timezone.now(), snapshot=_task_snapshot(row), patch={"origin_id": origin.id})
                created += 1
        return {"meeting_id": meeting_id, "created": created, "updated": 0}


class NoopMeetingGraphRepo:
    def upsert_meeting_chunks_topics(self, meeting: dict[str, Any], chunks: list[dict[str, Any]], topics: list[dict[str, Any]]) -> None:
        return None


def normalize_email(value: str) -> str:
    return str(value or "").strip().lower()


def is_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value or ""))


def normalize_alias(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def anonymous_email_for_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", ".", normalize_alias(name)).strip(".") or "unknown"
    return f"{slug}@{ANONYMOUS_DOMAIN}"


def _upsert_alias(*, alias: str, email: str | None, source: str, metadata: dict[str, Any]) -> PersonAlias:
    normalized = normalize_alias(alias)
    row, _ = PersonAlias.objects.get_or_create(normalized_alias=normalized, defaults={"id": new_id("alias"), "alias": alias.strip(), "email_id": email, "source": source, "confidence": 1.0, "metadata_payload": metadata})
    row.alias = alias.strip()
    if email:
        row.email_id = email
    row.source = source
    row.metadata_payload = {**(row.metadata_payload or {}), **metadata}
    row.save()
    return row


def _alias_id(value: str | None) -> str | None:
    if not value or not normalize_alias(value):
        return None
    return _upsert_alias(alias=value, email=None, source="meeting_conclusion", metadata={}).id


def _pipeline_name(stage: str) -> str:
    if stage in {"pulled", "ingested", "source_synced", "transcript_saved"}:
        return "ingest"
    if stage in {"washed"}:
        return "wash"
    if stage == "pipeline":
        return "pipeline"
    return "generate"


def _parse_meeting_datetime(transcript: dict[str, Any]) -> datetime | None:
    return _parse_datetime_value(transcript.get("dateString") or transcript.get("date") or transcript.get("started_at"))


def _parse_datetime_value(raw: Any) -> datetime | None:
    if raw is None:
        return None
    try:
        value = datetime.fromtimestamp(raw / 1000 if isinstance(raw, (int, float)) and raw > 10_000_000_000 else raw, UTC) if isinstance(raw, (int, float)) else datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value


def _duration_seconds(raw: Any) -> int | None:
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return int(value * 60) if value < 10_000 else int(value)


def _seconds_to_ms(raw: Any) -> int | None:
    try:
        return None if raw is None else int(float(raw) * 1000)
    except (TypeError, ValueError):
        return None


def _ms_to_seconds(raw: int | None) -> float | None:
    return None if raw is None else raw / 1000


def _transcript_text(transcript: dict[str, Any]) -> str:
    return "\n".join(str(sentence.get("text") or "") for sentence in transcript.get("sentences") or [] if isinstance(sentence, dict))


def _task_snapshot(row: TaskMasterlist) -> dict[str, Any]:
    return {"task_id": row.id, "task_date": row.task_date.isoformat() if row.task_date else None, "title": row.title, "action": row.action, "context": row.context, "priority": row.priority, "status": row.status, "origin_id": row.origin_id, "origin_type": row.origin_type, "version": row.version, "metadata": row.metadata_payload or {}}


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump())
    if hasattr(value, "_meta"):
        return _jsonable(model_to_dict(value))
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value
