from __future__ import annotations

from typing import Any

from domain.models.logs import ApplicationLog
from .ids import new_id


def sanitize_log_value(value: Any, *, max_chars: int | None = 4000) -> Any:
    if isinstance(value, str):
        return value if max_chars is None or len(value) <= max_chars else value[:max_chars] + "..."
    if isinstance(value, dict):
        return {str(key): sanitize_log_value(item, max_chars=max_chars) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_log_value(item, max_chars=max_chars) for item in value]
    return value


def write(*, level: str, logger_name: str, event: str, message: str = "", stage: str = "", correlation_id: str | None = None, meeting_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
    ApplicationLog.objects.create(id=new_id("log"), level=level.upper(), logger_name=logger_name, event=event, message=message, stage=stage, correlation_id=correlation_id, meeting_id=meeting_id, payload=sanitize_log_value(payload or {}))


def write_for_payload(*, level: str, logger_name: str, event: str, message: str = "", stage: str = "", correlation_id: str | None = None, payload: dict[str, Any] | None = None, extra: dict[str, Any] | None = None) -> None:
    log_payload = {**(payload or {}), **(extra or {})}
    meeting_ids = list((payload or {}).get("meeting_ids") or [])
    if (payload or {}).get("meeting_id"):
        meeting_ids.append((payload or {})["meeting_id"])
    if not meeting_ids:
        write(level=level, logger_name=logger_name, event=event, message=message, stage=stage, correlation_id=correlation_id, payload=log_payload)
        return
    for meeting_id in meeting_ids:
        write(level=level, logger_name=logger_name, event=event, message=message, stage=stage, correlation_id=correlation_id, meeting_id=str(meeting_id), payload=log_payload)


def list_logs(*, limit: int = 100, meeting_id: str | None = None, correlation_id: str | None = None, stage: str | None = None, event: str | None = None) -> list[dict[str, Any]]:
    query = ApplicationLog.objects.order_by("-created_at")
    if meeting_id:
        query = query.filter(meeting_id=meeting_id)
    if correlation_id:
        query = query.filter(correlation_id=correlation_id)
    if stage:
        query = query.filter(stage=stage)
    if event:
        query = query.filter(event=event)
    return [{"id": row.id, "created_at": row.created_at, "level": row.level, "logger_name": row.logger_name, "stage": row.stage, "event": row.event, "message": row.message, "correlation_id": row.correlation_id, "meeting_id": row.meeting_id, "payload": row.payload or {}} for row in query[:limit]]
