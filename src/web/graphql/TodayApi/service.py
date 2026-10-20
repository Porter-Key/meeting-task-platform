from __future__ import annotations

import hashlib
from collections import OrderedDict
from datetime import date
from typing import Any

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from application.tasks.task_masterlist import submit_task_masterlist_items_task
from django_client import task_masterlist as task_client
from domain.models.job import ApplicationJob
from domain.models.meeting import Meeting
from domain.models.monday import MondayBoard, MondayColumn, MondayGroup
from domain.models.people import Person
from domain.models.task_masterlist import TaskAssigneeLink, TaskMasterlist
from web.graphql.dto.monday import serialize_board_schema
from web.graphql.dto.people import PersonDTO
from web.graphql.jobs import enqueue_task


def today_review_bundle(*, from_date: str, to_date: str, include_archived: bool = False) -> dict[str, Any]:
    start = date.fromisoformat(from_date)
    end = date.fromisoformat(to_date)
    if end < start:
        start, end = end, start

    rows = _range_rows(start=start, end=end, include_archived=include_archived)
    task_items = _effective_task_items(rows, start=start, end=end)
    board_schemas = board_schemas_for_rows([row for row, _, _ in task_items])
    pending_jobs = pending_jobs_by_task_id([row.id for row, _, _ in task_items])
    links_by_task = assignees_by_task([row.id for row, _, _ in task_items])

    readiness_by_task_id = {row.id: task_readiness(row, board_schemas.get(str(row.monday_board_id))) for row, _, _ in task_items}
    task_dtos = {
        row.id: today_task_dto(row, meeting=meeting, readiness=readiness_by_task_id[row.id], assignees=links_by_task.get(row.id) or [], pending_job=pending_jobs.get(row.id))
        for row, _, meeting in task_items
    }

    grouped: OrderedDict[str, OrderedDict[tuple[str | None, str | None, bool], OrderedDict[str, dict[str, Any]]]] = OrderedDict()
    person_emails: set[str] = set()
    for row, effective_date, meeting in task_items:
        owner = task_owner(row.id, links_by_task)
        if owner.get("email"):
            person_emails.add(str(owner["email"]))
        date_bucket = grouped.setdefault(effective_date.isoformat(), OrderedDict())
        owner_bucket = date_bucket.setdefault((owner.get("email"), owner.get("alias_id"), bool(owner.get("resolved"))), OrderedDict())
        meeting_id = str(meeting.id) if meeting else ""
        meeting_title = meeting.title if meeting else "No linked meeting"
        meeting_bucket = owner_bucket.setdefault(meeting_id, {"meeting_id": meeting_id, "meeting_title": meeting_title, "tasks": []})
        meeting_bucket["tasks"].append(task_dtos[row.id])

    people = Person.objects.filter(email__in=person_emails).order_by("email") if person_emails else Person.objects.none()
    generated_at = timezone.now()
    return {
        "from_date": start.isoformat(),
        "to_date": end.isoformat(),
        "bundle_version": bundle_version([row for row, _, _ in task_items], generated_at=generated_at),
        "generated_at": generated_at.isoformat(),
        "dates": [{"date": date_key, "groups": [{"email": email, "alias_id": alias_id, "resolved": resolved, "meetings": list(meetings.values())} for (email, alias_id, resolved), meetings in owners.items()]} for date_key, owners in grouped.items()],
        "people": list(PersonDTO(people, many=True).data),
        "monday_boards": list(board_schemas.values()),
        "readiness_by_task_id": readiness_by_task_id,
        "pending_jobs_by_task_id": pending_jobs,
    }


def set_due_date(task_id: str, *, due_date: str | None, due_note: str | None = None, changed_by: str | None = None) -> dict[str, Any]:
    row = _get_task(task_id)
    patch: dict[str, Any] = {"due_date": date.fromisoformat(due_date) if due_date else None}
    if due_note is not None:
        patch["due_note"] = due_note
    fields = _normalize_monday_values(row, row.monday_field_values or {})
    for column_id in _due_column_ids(str(row.monday_board_id) if row.monday_board_id else None):
        if due_date:
            fields[column_id] = {"date": due_date}
        else:
            fields.pop(column_id, None)
    if fields != (row.monday_field_values or {}):
        patch["monday_field_values"] = fields
    return _mutation_result(_update_task(task_id, patch, changed_by=changed_by))


def set_monday_target(task_id: str, *, board_id: str, group_id: str, changed_by: str | None = None) -> dict[str, Any]:
    board = MondayBoard.objects.filter(monday_board_id=str(board_id)).first()
    group = MondayGroup.objects.filter(monday_board_id=str(board_id), monday_group_id=str(group_id)).first()
    patch = {
        "monday_board_id": str(board_id),
        "monday_board_name": board.name if board else None,
        "monday_group_id": str(group_id),
        "monday_group_title": group.title if group else None,
        "monday_schema_version": _board_schema_version(str(board_id)),
    }
    return _mutation_result(_update_task(task_id, patch, changed_by=changed_by))


def save_schema(task_id: str, *, values: dict[str, Any], changed_by: str | None = None) -> dict[str, Any]:
    row = _get_task(task_id)
    merged = _normalize_monday_values(row, {**(row.monday_field_values or {}), **(values or {})})
    return _mutation_result(_update_task(task_id, {"monday_field_values": merged, "monday_schema_version": _board_schema_version(row.monday_board_id)}, changed_by=changed_by))


def update_fields(task_id: str, *, patch: dict[str, Any], changed_by: str | None = None) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in (patch or {}).items():
        if key == "monday_fields":
            row = _get_task(task_id)
            merged = _normalize_monday_values(row, {**(row.monday_field_values or {}), **(value or {})})
            normalized["monday_field_values"] = merged
        elif key in {"title", "action", "status", "priority", "due_note"}:
            normalized[key] = value
        elif key == "due_date":
            normalized[key] = date.fromisoformat(value) if value else None
    return _mutation_result(_update_task(task_id, normalized, changed_by=changed_by))


def archive_tasks(task_ids: list[str], *, changed_by: str | None = None) -> list[dict[str, Any]]:
    task_client.archive(task_ids, changed_by=changed_by)
    return [_mutation_result(TaskMasterlist.objects.get(id=task_id)) for task_id in task_ids if TaskMasterlist.objects.filter(id=task_id).exists()]


def reject_tasks(task_ids: list[str], *, changed_by: str | None = None) -> list[dict[str, Any]]:
    for task_id in task_ids:
        _update_task(task_id, {"status": "rejected"}, changed_by=changed_by)
    return [_mutation_result(TaskMasterlist.objects.get(id=task_id)) for task_id in task_ids if TaskMasterlist.objects.filter(id=task_id).exists()]


def submit_today_tasks(task_ids: list[str], *, changed_by: str | None = None) -> dict[str, Any]:
    rows = list(TaskMasterlist.objects.filter(id__in=task_ids).select_related("origin", "origin__meeting"))
    row_by_id = {row.id: row for row in rows}
    schemas = board_schemas_for_rows(rows)
    accepted: list[str] = []
    blocked: list[dict[str, Any]] = []
    for task_id in task_ids:
        row = row_by_id.get(task_id)
        if row is None:
            blocked.append({"task_id": task_id, "readiness": _blocked("blocked", "Task not found", ["task_not_found"]), "reason": "task_not_found"})
            continue
        readiness = task_readiness(row, schemas.get(str(row.monday_board_id)))
        if readiness["canSubmit"]:
            accepted.append(task_id)
        else:
            blocked.append({"task_id": task_id, "readiness": readiness, "reason": readiness["label"]})
    job = None
    if accepted:
        job = enqueue_task(command="submit-today-tasks", task_func=submit_task_masterlist_items_task, payload={"task_ids": accepted, "changed_by": changed_by, "dry_run": False}, meeting_ids=[])
    return {"job": job, "accepted_task_ids": accepted, "blocked_tasks": blocked, "bundle_version": bundle_version(rows)}


def task_readiness(row: TaskMasterlist, board_schema: dict[str, Any] | None) -> dict[str, Any]:
    if (row.status or "").lower() == "archived":
        return _blocked("blocked", "Task is archived", ["task_archived"])
    if not row.monday_board_id or board_schema is None:
        return _blocked("blocked", "No Monday board selected", ["missing_board"])
    if not row.monday_group_id:
        return _blocked("no_group", "Choose a Monday group", ["missing_group"])
    values = _normalize_monday_values(row, row.monday_field_values or {})
    missing = []
    for column in board_schema.get("columns") or []:
        if not column.get("required"):
            continue
        column_id = str(column.get("monday_column_id") or "")
        if values.get(column_id) in (None, "", [], {}):
            missing.append({"columnId": column_id, "fieldKey": column.get("field_key"), "title": column.get("title") or "", "type": column.get("type"), "valueKind": column.get("value_kind") or "json"})
    if missing:
        return {"state": "missing", "canSubmit": False, "label": f"Missing {len(missing)} required field(s)", "missingFields": missing, "blockingReasons": ["missing_required_fields"]}
    return {"state": "ready", "canSubmit": True, "label": "Ready to submit", "missingFields": [], "blockingReasons": []}


def today_task_dto(row: TaskMasterlist, *, meeting: Meeting | None = None, readiness: dict[str, Any] | None = None, assignees: list[TaskAssigneeLink] | None = None, pending_job: dict[str, Any] | None = None) -> dict[str, Any]:
    if meeting is None and row.origin_id and row.origin and row.origin.meeting_id:
        meeting = row.origin.meeting
    readiness = readiness or task_readiness(row, board_schemas_for_rows([row]).get(str(row.monday_board_id)))
    return {
        "id": row.id,
        "title": row.title or "",
        "action": row.action or "",
        "status": row.status or "",
        "priority": row.priority or "",
        "due_date": row.due_date.isoformat() if row.due_date else None,
        "due_note": row.due_note,
        "monday_target": {"board_id": row.monday_board_id, "board_name": row.monday_board_name, "group_id": row.monday_group_id, "group_title": row.monday_group_title},
        "monday_fields": _normalize_monday_values(row, row.monday_field_values or {}),
        "readiness": readiness,
        "available_actions": _available_actions(row, readiness),
        "action_state": _action_state(row, pending_job),
        "meeting_id": str(meeting.id) if meeting else None,
        "meeting_title": meeting.title if meeting else None,
        "owner": task_owner(row.id, {row.id: assignees or []}),
        "changed_at": _changed_at(row).isoformat() if _changed_at(row) else None,
    }


def board_schemas_for_rows(rows: list[TaskMasterlist]) -> OrderedDict[str, dict[str, Any]]:
    board_ids = {str(row.monday_board_id) for row in rows if row.monday_board_id}
    result: OrderedDict[str, dict[str, Any]] = OrderedDict()
    if not board_ids:
        return result
    boards = {str(board.monday_board_id): board for board in MondayBoard.objects.filter(monday_board_id__in=board_ids).order_by("name")}
    groups_by_board: dict[str, list[MondayGroup]] = {board_id: [] for board_id in board_ids}
    for group in MondayGroup.objects.filter(monday_board_id__in=board_ids, archived=False, deleted=False).order_by("title"):
        groups_by_board.setdefault(str(group.monday_board_id), []).append(group)
    columns_by_board: dict[str, list[MondayColumn]] = {board_id: [] for board_id in board_ids}
    for column in MondayColumn.objects.filter(monday_board_id__in=board_ids).order_by("title"):
        columns_by_board.setdefault(str(column.monday_board_id), []).append(column)
    for board_id, board in boards.items():
        schema = serialize_board_schema(board=board, groups=groups_by_board.get(board_id) or [], columns=columns_by_board.get(board_id) or [])
        result[board_id] = {"board_id": board_id, "name": board.name or "", "workspace_name": board.workspace_name, "groups": schema["groups"], "columns": schema["columns"]}
    return result


def assignees_by_task(task_ids: list[str]) -> dict[str, list[TaskAssigneeLink]]:
    result = {task_id: [] for task_id in task_ids}
    if not task_ids:
        return result
    for link in TaskAssigneeLink.objects.filter(masterlist_task_id__in=task_ids).select_related("email", "alias").order_by("relation", "id"):
        result.setdefault(str(link.masterlist_task_id), []).append(link)
    return result


def task_owner(task_id: str, links_by_task: dict[str, list[TaskAssigneeLink]]) -> dict[str, Any]:
    links = links_by_task.get(task_id) or []
    primary = next((link for link in links if (link.relation or "").lower() == "owner"), links[0] if links else None)
    if primary is None:
        return {"email": None, "aliasId": None, "resolved": False, "label": "Unassigned"}
    return {"email": primary.email_id, "aliasId": str(primary.alias_id) if primary.alias_id else None, "resolved": bool(primary.email_id), "label": primary.email_id or (primary.alias.alias if primary.alias_id and primary.alias else "Unresolved")}


def _normalize_monday_values(row: TaskMasterlist, values: dict[str, Any]) -> dict[str, Any]:
    if not values:
        return {}
    columns = list(MondayColumn.objects.filter(monday_board_id=str(row.monday_board_id))) if row.monday_board_id else []
    if not columns:
        return dict(values)
    by_column_id = {str(column.monday_column_id): column for column in columns}
    by_field_key = {str(column.field_key).strip().lower(): column for column in columns if column.field_key}
    by_title = {_normalize_key(column.title): column for column in columns if column.title}
    normalized: dict[str, Any] = {}
    for key, value in values.items():
        raw_key = str(key)
        column = by_column_id.get(raw_key) or by_field_key.get(raw_key.strip().lower()) or by_title.get(_normalize_key(raw_key))
        normalized[column.monday_column_id if column else raw_key] = _normalize_monday_value(column, value)
    return normalized


def _normalize_key(value: str | None) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def _normalize_monday_value(column: MondayColumn | None, value: Any) -> Any:
    if column is None:
        return value
    column_type = column.type or ""
    if column_type == "date" and isinstance(value, str):
        return {"date": value}
    if column_type == "status" and isinstance(value, str):
        return {"label": value}
    if column_type == "dropdown" and isinstance(value, str):
        return {"labels": [value]}
    if column_type == "dropdown" and isinstance(value, list):
        return {"labels": value}
    return value


def pending_jobs_by_task_id(task_ids: list[str]) -> dict[str, Any]:
    pending = {"queued", "running", "accepted", "started"}
    result: dict[str, Any] = {}
    if not task_ids:
        return result
    for job in ApplicationJob.objects.filter(command__in=["submit-task-masterlist-items", "submit-today-tasks"], status__in=pending).order_by("-created_at")[:100]:
        payload = job.payload or {}
        for task_id in payload.get("task_ids") or []:
            if task_id in task_ids and task_id not in result:
                result[task_id] = {"jobId": job.id, "queueTaskId": job.queue_task_id, "status": job.status, "command": job.command}
    return result


def bundle_version(rows: list[TaskMasterlist], *, generated_at: Any | None = None) -> str:
    parts = [str(generated_at or timezone.now())]
    for row in rows:
        parts.append(f"{row.id}:{row.version}:{_changed_at(row)}")
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]


def _mutation_result(row: TaskMasterlist) -> dict[str, Any]:
    row = TaskMasterlist.objects.select_related("origin", "origin__meeting").get(id=row.id)
    schemas = board_schemas_for_rows([row])
    readiness = task_readiness(row, schemas.get(str(row.monday_board_id)))
    assignees = assignees_by_task([row.id]).get(row.id) or []
    task = today_task_dto(row, meeting=row.origin.meeting if row.origin_id and row.origin and row.origin.meeting_id else None, readiness=readiness, assignees=assignees)
    return {"task": task, "readiness": readiness, "bundle_version": bundle_version([row])}


def _range_rows(*, start: date, end: date, include_archived: bool) -> list[TaskMasterlist]:
    rows = list(TaskMasterlist.objects.select_related("origin", "origin__meeting").filter(Q(task_date__range=(start, end)) | Q(task_date__isnull=True, origin__meeting__started_at__date__range=(start, end))).order_by("task_date", "origin__meeting__started_at", "title"))
    return rows if include_archived else [row for row in rows if (row.status or "").lower() != "archived"]


def _effective_task_items(rows: list[TaskMasterlist], *, start: date, end: date) -> list[tuple[TaskMasterlist, date, Meeting | None]]:
    result = []
    for row in rows:
        meeting = row.origin.meeting if row.origin_id and row.origin and row.origin.meeting_id else None
        effective_date = row.task_date or (meeting.started_at.date() if meeting and meeting.started_at else None)
        if effective_date is not None and start <= effective_date <= end:
            result.append((row, effective_date, meeting))
    return result


def _update_task(task_id: str, patch: dict[str, Any], *, changed_by: str | None) -> TaskMasterlist:
    with transaction.atomic():
        data = task_client.update(task_id, patch, changed_by=changed_by)
        if data is None:
            raise ValueError("task_not_found")
        return TaskMasterlist.objects.get(id=task_id)


def _get_task(task_id: str) -> TaskMasterlist:
    row = TaskMasterlist.objects.filter(id=task_id).first()
    if row is None:
        raise ValueError("task_not_found")
    return row


def _blocked(state: str, label: str, reasons: list[str]) -> dict[str, Any]:
    return {"state": state, "canSubmit": False, "label": label, "missingFields": [], "blockingReasons": reasons}


def _available_actions(row: TaskMasterlist, readiness: dict[str, Any]) -> list[str]:
    actions = ["setDueDate", "clearDueDate", "chooseMondayGroup", "saveRequiredFields", "archiveTasks", "rejectTasks"]
    if readiness.get("canSubmit"):
        actions.append("submitTasks")
    if (row.status or "").lower() == "archived":
        return ["restoreTasks"]
    return actions


def _action_state(row: TaskMasterlist, pending_job: dict[str, Any] | None) -> str:
    if pending_job:
        return "queued" if pending_job.get("status") == "queued" else "submitting"
    if (row.status or "").lower() == "submitted":
        return "submitted"
    return "idle"


def _changed_at(row: TaskMasterlist):
    return row.submitted_at or row.saved_at or row.monday_target_set_at


def _board_schema_version(board_id: str | None) -> str | None:
    if not board_id:
        return None
    latest = MondayColumn.objects.filter(monday_board_id=str(board_id)).order_by("-synced_at").first()
    return latest.synced_at.isoformat() if latest and latest.synced_at else None


def _due_column_ids(board_id: str | None) -> list[str]:
    if not board_id:
        return []
    rows = MondayColumn.objects.filter(monday_board_id=str(board_id), type="date")
    result = []
    for column in rows:
        text = f"{column.title or ''} {column.field_key or ''}".lower()
        if "due" in text:
            result.append(str(column.monday_column_id))
    return result
