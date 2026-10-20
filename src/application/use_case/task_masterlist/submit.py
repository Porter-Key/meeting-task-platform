from __future__ import annotations

from typing import Any

from django.utils import timezone

from domain.models.monday import MondayColumn, MondayPushRun, MondayPushRunItem, MondayTaskLink, MondayUserMapping
from domain.models.task_masterlist import TaskAssigneeLink, TaskMasterlist
from django_client.ids import new_id
from django_client.uow import atomic
from external_client.config import get_config
from external_client.monday.client import create_client


def submit_task_masterlist_items(payload: dict[str, Any], *, job_id: str | None = None) -> dict[str, Any]:
    task_ids = [str(item) for item in payload.get("task_ids") or payload.get("taskIds") or [] if item]
    changed_by = payload.get("changed_by") or payload.get("changedBy") or payload.get("requested_by") or payload.get("requestedBy")
    dry_run = bool(payload.get("dry_run") or payload.get("dryRun") or False)
    force_create = bool(payload.get("force_create") or payload.get("forceCreate") or False)
    tasks = list(TaskMasterlist.objects.filter(id__in=task_ids).order_by("task_date", "title")) if task_ids else []
    run = _create_run(task_ids=task_ids, changed_by=changed_by, dry_run=dry_run, force_create=force_create, job_id=job_id)
    client = None if dry_run else create_client(get_config().monday)
    try:
        for task in tasks:
            _publish_one(run, task, client=client, dry_run=dry_run, force_create=force_create)
    finally:
        if client is not None:
            client.close()
    _finish_run(run)
    _mark_submitted(tasks, changed_by=changed_by)
    return {
        "run_id": run.id,
        "status": run.status,
        "task_ids": task_ids,
        "total": run.total_count,
        "success": run.success_count,
        "skipped": run.skipped_count,
        "failed": run.failed_count,
        "dry_run": dry_run,
        "items": [_item_payload(item) for item in MondayPushRunItem.objects.filter(run=run).order_by("created_at")],
    }


def _create_run(*, task_ids: list[str], changed_by: str | None, dry_run: bool, force_create: bool, job_id: str | None) -> MondayPushRun:
    return MondayPushRun.objects.create(id=new_id("monday_run"), requested_by=changed_by, status="running", total_count=len(task_ids), started_at=timezone.now(), metadata_payload={"dry_run": dry_run, "task_ids": task_ids, "force_create": force_create, "job_id": job_id})


def _publish_one(run: MondayPushRun, task: TaskMasterlist, *, client: Any | None, dry_run: bool, force_create: bool) -> None:
    if not task.monday_board_id or not task.monday_group_id:
        _record_item(run, task, action="skip", status="skipped", error="monday_target_missing")
        return
    existing = MondayTaskLink.objects.filter(masterlist_task=task, monday_board_id=task.monday_board_id, status="active").order_by("-last_pushed_at", "-created_at").first()
    action = "create" if force_create or existing is None else "update"
    column_values, warnings = _column_values(task)
    request_payload = {"dry_run": dry_run, "board_id": task.monday_board_id, "group_id": task.monday_group_id, "item_name": _item_name(task), "column_value_keys": sorted(column_values.keys())}
    try:
        if dry_run:
            response = {"id": existing.monday_item_id if existing and not force_create else None, "url": existing.monday_item_url if existing and not force_create else None, "dry_run": True}
        elif action == "create":
            response = client.create_item(board_id=task.monday_board_id, group_id=task.monday_group_id, item_name=_item_name(task), column_values=column_values or None)
        else:
            response = client.change_multiple_column_values(board_id=task.monday_board_id, item_id=existing.monday_item_id, column_values=column_values)
        monday_item_id = str(response.get("id") or (existing.monday_item_id if existing else "") or "") or None
        monday_item_url = response.get("url") or (existing.monday_item_url if existing else None)
        _record_item(run, task, action=action, status="success", monday_item_id=monday_item_id, warnings=warnings, request_payload=request_payload, response_payload=response)
        if monday_item_id and not dry_run:
            _upsert_link(task, run=run, monday_item_id=monday_item_id, monday_item_url=monday_item_url, warnings=warnings)
    except Exception as exc:
        _record_item(run, task, action=action, status="failed", error=str(exc), warnings=warnings, request_payload=request_payload)


def _column_values(task: TaskMasterlist) -> tuple[dict[str, Any], list[str]]:
    values = dict(task.monday_field_values or {})
    warnings: list[str] = []
    columns = {c.monday_column_id: c for c in MondayColumn.objects.filter(monday_board_id=str(task.monday_board_id))}
    result: dict[str, Any] = {}
    for key, value in values.items():
        column_id = _resolve_column_id(str(key), columns)
        if not column_id:
            warnings.append(f"monday_column_unknown:{key}")
            continue
        result[column_id] = _format_column_value(columns.get(column_id), value)
    owner_column = _owner_column(columns)
    if owner_column and owner_column.monday_column_id not in result:
        owner_value = _owner_column_value(task)
        if owner_value:
            result[owner_column.monday_column_id] = owner_value
        else:
            warnings.append("monday_owner_mapping_missing")
    return result, warnings


def _resolve_column_id(key: str, columns: dict[str, MondayColumn]) -> str | None:
    if key in columns:
        return key
    normalized = key.strip().lower().replace(" ", "_").replace("-", "_")
    for column in columns.values():
        candidates = {str(column.field_key or "").lower(), str(column.title or "").strip().lower().replace(" ", "_").replace("-", "_")}
        if normalized in candidates:
            return column.monday_column_id
    return None


def _format_column_value(column: MondayColumn | None, value: Any) -> Any:
    if column is None:
        return value
    column_type = column.type or ""
    if column_type == "date" and isinstance(value, dict) and set(value.keys()) <= {"date", "time"}:
        return value
    if column_type == "date" and isinstance(value, str):
        return {"date": value}
    if column_type == "status" and isinstance(value, dict) and "label" in value:
        return value
    if column_type == "status":
        return {"label": value} if isinstance(value, str) else value
    if column_type == "dropdown":
        if isinstance(value, dict) and ("labels" in value or "ids" in value):
            return value
        if isinstance(value, list):
            return {"labels": value}
        if isinstance(value, str):
            return {"labels": [value]}
    if column_type == "people" and isinstance(value, list):
        return {"personsAndTeams": [{"id": str(item), "kind": "person"} if not isinstance(item, dict) else item for item in value]}
    if column_type == "numbers" and isinstance(value, (int, float, str)):
        return str(value)
    return value


def _owner_column(columns: dict[str, MondayColumn]) -> MondayColumn | None:
    people = [c for c in columns.values() if (c.type or "") == "people"]
    if not people:
        return None
    return next((c for c in people if (c.title or "").strip().lower() in {"owner", "person"}), people[0])


def _owner_column_value(task: TaskMasterlist) -> dict[str, Any] | None:
    links = list(TaskAssigneeLink.objects.filter(masterlist_task=task).order_by("relation", "id"))
    owner = next((link for link in links if (link.relation or "").lower() == "owner"), links[0] if links else None)
    if not owner or not owner.email_id:
        return None
    mapping = MondayUserMapping.objects.filter(person_email_id=owner.email_id, verified=True).first() or MondayUserMapping.objects.filter(person_email_id=owner.email_id).order_by("-confidence").first()
    if not mapping:
        return None
    return {"personsAndTeams": [{"id": int(mapping.monday_user_id) if str(mapping.monday_user_id).isdigit() else mapping.monday_user_id, "kind": "person"}]}


def _record_item(run: MondayPushRun, task: TaskMasterlist | None, *, action: str, status: str, monday_item_id: str | None = None, warnings: list[str] | None = None, error: str | None = None, request_payload: dict[str, Any] | None = None, response_payload: dict[str, Any] | None = None) -> None:
    MondayPushRunItem.objects.create(id=new_id("monday_item"), run=run, masterlist_task=task, action=action, status=status, monday_item_id=monday_item_id, warnings=warnings or [], error=error, request_payload=request_payload or {}, response_payload=response_payload or {}, metadata_payload={})


def _upsert_link(task: TaskMasterlist, *, run: MondayPushRun, monday_item_id: str, monday_item_url: str | None, warnings: list[str]) -> None:
    link = MondayTaskLink.objects.filter(masterlist_task=task, monday_item_id=monday_item_id).first() or MondayTaskLink(id=new_id("monday_link"), masterlist_task=task, monday_item_id=monday_item_id, monday_board_id=str(task.monday_board_id))
    link.monday_board_id = str(task.monday_board_id)
    link.monday_group_id = task.monday_group_id
    link.monday_item_url = monday_item_url
    link.status = "active"
    link.last_pushed_at = timezone.now()
    link.last_push_run_id = run.id
    link.last_error = None
    link.metadata_payload = {"warnings": warnings}
    link.save()


def _finish_run(run: MondayPushRun) -> None:
    items = list(MondayPushRunItem.objects.filter(run=run))
    run.success_count = sum(1 for item in items if item.status == "success")
    run.skipped_count = sum(1 for item in items if item.status == "skipped")
    run.failed_count = sum(1 for item in items if item.status == "failed")
    run.status = "failed" if run.failed_count and not run.success_count and not run.skipped_count else "completed_with_errors" if run.failed_count else "completed"
    run.completed_at = timezone.now()
    run.save(update_fields=["success_count", "skipped_count", "failed_count", "status", "completed_at"])


def _mark_submitted(tasks: list[TaskMasterlist], *, changed_by: str | None) -> None:
    with atomic():
        for task in tasks:
            task.status = "submitted"
            task.submitted_by = changed_by
            task.submitted_at = timezone.now()
            task.save(update_fields=["status", "submitted_by", "submitted_at", "updated_at"])


def _item_name(task: TaskMasterlist) -> str:
    return (task.title or task.action or task.id)[:255]


def _item_payload(item: MondayPushRunItem) -> dict[str, Any]:
    return {"task_id": item.masterlist_task_id, "action": item.action, "status": item.status, "monday_item_id": item.monday_item_id, "warnings": item.warnings or [], "error": item.error, "response": item.response_payload or {}}
