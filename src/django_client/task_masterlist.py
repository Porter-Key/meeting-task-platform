from __future__ import annotations

from datetime import date
from typing import Any

from django.utils import timezone

from domain.models.people import Person, PersonAlias
from domain.models.task_masterlist import TaskAssigneeLink, TaskMasterlist, TaskOrigin, TaskVersion
from .ids import new_assignee_id, new_origin_id, new_task_id, new_version_id
from .uow import atomic


def list_items(*, limit: int = 200, status: str | None = None) -> list[dict[str, Any]]:
    query = TaskMasterlist.objects.order_by("-task_date", "title")
    if status:
        query = query.filter(status=status)
    return [dump(row) for row in query[:limit]]


def get(task_id: str) -> dict[str, Any] | None:
    row = TaskMasterlist.objects.filter(id=task_id).first()
    return dump(row) if row else None


def update(task_id: str, patch: dict[str, Any], *, changed_by: str | None = None) -> dict[str, Any] | None:
    row = TaskMasterlist.objects.filter(id=task_id).first()
    if not row:
        return None
    with atomic():
        _apply_patch(row, patch, changed_by=changed_by)
        row.save()
        _replace_assignees(row, patch.get("assignees"), source="manual_save") if "assignees" in patch else None
        _record_version(row, "submitted" if patch.get("status") == "submitted" else "saved", changed_by, patch)
    return dump(row)


def create(*, task_date: date, title: str, action: str = "", context: str = "", priority: str = "medium", status: str = "draft", changed_by: str | None = None, assignees: list[dict[str, Any]] | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    with atomic():
        origin = TaskOrigin.objects.create(id=new_origin_id(), origin_type="manual", title=title, action=action or title, context=context, priority=priority, payload={"created_by": changed_by, **(metadata or {})})
        row = TaskMasterlist.objects.create(id=new_task_id(), task_date=task_date, title=title, action=action or title, context=context, priority=priority, status=status, origin=origin, origin_type="manual", version=1, saved_by=changed_by, saved_at=timezone.now(), metadata_payload=metadata or {})
        _replace_assignees(row, assignees or [], source="manual_save")
        _record_version(row, "created", changed_by, {"title": title, "action": action, "context": context, "priority": priority, "status": status, "assignees": assignees or []})
        return dump(row)


def archive(task_ids: list[str], *, changed_by: str | None = None) -> list[dict[str, Any]]:
    return _set_status(task_ids, "archived", changed_by=changed_by, change_type="archived")


def restore(task_ids: list[str], *, changed_by: str | None = None, status: str = "saved") -> list[dict[str, Any]]:
    return _set_status(task_ids, status, changed_by=changed_by, change_type="restored")


def submit(task_ids: list[str], *, changed_by: str | None = None) -> list[dict[str, Any]]:
    return _set_status(task_ids, "submitted", changed_by=changed_by, change_type="submitted")


def set_monday_fields(task_ids: list[str], *, monday_board_id: str | None = None, monday_board_name: str | None = None, monday_group_id: str | None = None, monday_group_title: str | None = None, monday_field_values: dict[str, Any] | None = None, changed_by: str | None = None) -> list[dict[str, Any]]:
    updated: list[dict[str, Any]] = []
    now = timezone.now()
    with atomic():
        for row in TaskMasterlist.objects.filter(id__in=task_ids):
            patch: dict[str, Any] = {}
            for key, value in {"monday_board_id": monday_board_id, "monday_board_name": monday_board_name, "monday_group_id": monday_group_id, "monday_group_title": monday_group_title}.items():
                if value is not None:
                    setattr(row, key, value)
                    patch[key] = value
            if monday_field_values is not None:
                row.monday_field_values = {**(row.monday_field_values or {}), **monday_field_values}
                patch["monday_field_values"] = row.monday_field_values
            row.monday_target_set_by = changed_by
            row.monday_target_set_at = now
            row.monday_target_status = "unchecked"
            row.monday_target_checked_at = None
            row.monday_target_error = None
            row.saved_by = changed_by
            row.saved_at = now
            row.version += 1
            row.save()
            _record_version(row, "monday_fields_updated", changed_by, patch)
            updated.append(dump(row))
    return updated


def dump(row: TaskMasterlist) -> dict[str, Any]:
    return {"id": row.id, "task_date": row.task_date.isoformat() if row.task_date else None, "title": row.title, "action": row.action, "context": row.context, "priority": row.priority, "status": row.status, "origin_id": row.origin_id, "origin_type": row.origin_type, "version": row.version, "due_date": row.due_date.isoformat() if row.due_date else None, "due_note": row.due_note, "monday_board_id": row.monday_board_id, "monday_board_name": row.monday_board_name, "monday_group_id": row.monday_group_id, "monday_group_title": row.monday_group_title, "monday_schema_version": row.monday_schema_version, "monday_field_values": row.monday_field_values or {}, "metadata_payload": row.metadata_payload or {}}


def _apply_patch(row: TaskMasterlist, patch: dict[str, Any], *, changed_by: str | None) -> None:
    allowed = {"title", "action", "context", "priority", "status", "due_date", "due_note", "monday_board_id", "monday_board_name", "monday_group_id", "monday_group_title", "monday_schema_version"}
    for key in allowed:
        if key in patch:
            setattr(row, key, patch[key])
    if isinstance(patch.get("monday_field_values"), dict):
        row.monday_field_values = {**(row.monday_field_values or {}), **patch["monday_field_values"]}
    row.saved_by = changed_by or row.saved_by
    row.saved_at = timezone.now()
    if patch.get("status") == "submitted":
        row.submitted_by = changed_by
        row.submitted_at = timezone.now()
    row.version += 1


def _set_status(task_ids: list[str], status: str, *, changed_by: str | None, change_type: str) -> list[dict[str, Any]]:
    updated: list[dict[str, Any]] = []
    with atomic():
        for row in TaskMasterlist.objects.filter(id__in=task_ids):
            row.status = status
            row.version += 1
            row.saved_by = changed_by
            row.saved_at = timezone.now()
            if status == "submitted":
                row.submitted_by = changed_by
                row.submitted_at = timezone.now()
            row.save()
            _record_version(row, change_type, changed_by, {"status": status})
            updated.append(dump(row))
    return updated


def _replace_assignees(row: TaskMasterlist, assignees: list[dict[str, Any]] | None, *, source: str) -> None:
    if assignees is None:
        return
    TaskAssigneeLink.objects.filter(masterlist_task=row).delete()
    for item in assignees:
        email = str(item.get("email") or "").strip().lower() or None
        alias_value = str(item.get("alias") or item.get("name") or "").strip()
        alias_id = item.get("alias_id")
        if email:
            Person.objects.get_or_create(email=email, defaults={"identity_type": "alias", "source": source, "metadata_payload": {}})
        if not alias_id and alias_value:
            normalized = " ".join(alias_value.lower().split())
            alias, _ = PersonAlias.objects.get_or_create(normalized_alias=normalized, defaults={"id": new_assignee_id(), "alias": alias_value, "email_id": email, "source": source, "confidence": float(item.get("confidence") or 1), "metadata_payload": {}})
            if email and not alias.email_id:
                alias.email_id = email
                alias.save(update_fields=["email"])
            alias_id = alias.id
        TaskAssigneeLink.objects.create(id=new_assignee_id(), masterlist_task=row, email_id=email, alias_id=alias_id, relation=item.get("relation") or "assignee", source=source, confidence=float(item.get("confidence") or 1), metadata_payload=item.get("metadata") or {})


def _record_version(row: TaskMasterlist, change_type: str, changed_by: str | None, patch: dict[str, Any]) -> None:
    TaskVersion.objects.create(id=new_version_id(), masterlist_task=row, version=row.version, change_type=change_type, changed_by=changed_by, changed_at=timezone.now(), snapshot=dump(row), patch=patch)
