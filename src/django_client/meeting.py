from __future__ import annotations

from typing import Any

from domain.models.meeting import Meeting, MeetingChunk, MeetingConclusion, MeetingPeopleCandidate, MeetingPersonLink, MeetingPipelineRun, MeetingSource, MeetingTopic, MeetingTranscript
from domain.models.people import Person


def list_meetings(*, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
    return [dump_meeting(row) for row in Meeting.objects.order_by("-started_at", "-created_at")[offset:offset + limit]]


def get_meeting(meeting_id: str) -> dict[str, Any] | None:
    row = Meeting.objects.filter(id=meeting_id).first()
    return dump_meeting(row) if row else None


def get_chunks(meeting_id: str) -> list[dict[str, Any]]:
    return [{"id": row.id, "chunk_index": row.chunk_index, "text": row.text, "start_ms": row.start_ms, "end_ms": row.end_ms, "metadata": row.metadata_payload or {}} for row in MeetingChunk.objects.filter(meeting_id=meeting_id).order_by("chunk_index")]


def get_sources(meeting_id: str) -> list[dict[str, Any]]:
    return [{"id": row.id, "provider": row.provider, "provider_record_id": row.provider_record_id, "provider_url": row.provider_url, "sync_status": row.sync_status, "synced_at": row.synced_at, "metadata": row.metadata_payload or {}} for row in MeetingSource.objects.filter(meeting_id=meeting_id)]


def get_transcripts(meeting_id: str) -> list[dict[str, Any]]:
    return [{"id": row.id, "format": row.format, "content": row.content, "segments": row.segments, "language": row.language, "metadata": row.metadata_payload or {}} for row in MeetingTranscript.objects.filter(meeting_id=meeting_id)]


def get_topics(meeting_id: str) -> list[dict[str, Any]]:
    return [{"id": row.id, "topic_index": row.topic_index, "title": row.title, "summary": row.summary, "source_chunk_indexes": row.source_chunk_indexes or [], "confidence": row.confidence, "payload": row.payload or {}} for row in MeetingTopic.objects.filter(meeting_id=meeting_id).order_by("topic_index")]


def get_conclusion(meeting_id: str) -> dict[str, Any] | None:
    row = MeetingConclusion.objects.filter(meeting_id=meeting_id).order_by("-created_at").first()
    return {"id": row.id, "title": row.title, "summary": row.summary, "one_sentence_summary": row.one_sentence_summary, "tl_dr": row.tl_dr or [], "payload": row.payload or {}} if row else None


def get_person_links(meeting_id: str) -> list[dict[str, Any]]:
    return [{"id": row.id, "email": row.email_id, "alias_id": row.alias_id, "relation": row.relation, "source": row.source, "confidence": row.confidence, "metadata": row.metadata_payload or {}} for row in MeetingPersonLink.objects.filter(meeting_id=meeting_id)]


def get_pipeline_runs(meeting_id: str) -> list[dict[str, Any]]:
    return [{"id": row.id, "pipeline_name": row.pipeline_name, "stage": row.stage, "status": row.status, "job_id": row.job_id, "started_at": row.started_at, "finished_at": row.finished_at, "error": row.error, "metadata": row.metadata_payload or {}} for row in MeetingPipelineRun.objects.filter(meeting_id=meeting_id).order_by("-created_at")]


def get_people_candidates(meeting_id: str) -> list[dict[str, Any]]:
    return [{"id": row.id, "ref": row.ref, "email": row.email_id, "alias_id": row.alias_id, "identity_type": row.identity_type, "display_label": row.display_label, "sources": row.sources or [], "confidence": row.confidence, "metadata": row.metadata_payload or {}} for row in MeetingPeopleCandidate.objects.filter(meeting_id=meeting_id)]


def list_people(*, include_inactive: bool = False, limit: int = 200, identity_type: str | None = None) -> list[dict[str, Any]]:
    query = Person.objects.all()
    if not include_inactive:
        query = query.filter(is_active=True)
    if identity_type:
        query = query.filter(identity_type=identity_type)
    return [{"email": row.email, "identity_type": row.identity_type, "role": row.role, "is_active": row.is_active, "source": row.source, "metadata": row.metadata_payload or {}} for row in query.order_by("email")[:limit]]


def get_person(email: str) -> dict[str, Any] | None:
    row = Person.objects.filter(email=email).first()
    return {"email": row.email, "identity_type": row.identity_type, "role": row.role, "is_active": row.is_active, "source": row.source, "metadata": row.metadata_payload or {}} if row else None


def dump_meeting(row: Meeting) -> dict[str, Any]:
    return {"id": row.id, "title": row.title, "started_at": row.started_at, "ended_at": row.ended_at, "duration_seconds": row.duration_seconds, "timezone": row.timezone, "metadata": row.metadata_payload or {}}
