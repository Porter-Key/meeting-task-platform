from __future__ import annotations

from collections import OrderedDict
from datetime import date
from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from domain.models.job import ApplicationJob
from domain.models.logs import ApplicationLog
from domain.models.meeting import Meeting, MeetingConclusion, MeetingPeopleCandidate, MeetingPipelineRun, MeetingTopic
from domain.models.monday import MondayBoard, MondayColumn, MondayGroup
from domain.models.people import Person
from django_client import job as job_client
from domain.models.task_masterlist import TaskAssigneeLink, TaskExternalLink, TaskMasterlist
from web.graphql.dto.job import ApplicationJobDTO, ApplicationLogDTO
from web.graphql.dto.meeting import MeetingDTO, MeetingPipelineRunDTO
from web.graphql.dto.monday import MondayBoardDTO, serialize_board_schema
from web.graphql.dto.people import PersonDTO
from web.graphql.dto.task_masterlist import TaskAssigneeLinkDTO, TaskExternalLinkDTO, TaskMasterlistDTO


def limited(value: int, *, default: int = 50, maximum: int = 500) -> int:
    return max(1, min(maximum, int(value or default)))


def list_meetings(*, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
    rows = Meeting.objects.order_by("-started_at", "-created_at")[max(0, offset): max(0, offset) + limited(limit)]
    return list(MeetingDTO(rows, many=True).data)


def get_meeting(meeting_id: str) -> dict[str, Any] | None:
    row = Meeting.objects.filter(id=meeting_id).first()
    return MeetingDTO(row).data if row else None


def meeting_detail_bundle(meeting_id: str) -> dict[str, Any]:
    meeting = Meeting.objects.filter(id=meeting_id).first()
    conclusion = MeetingConclusion.objects.filter(meeting_id=meeting_id).order_by("-created_at").first()
    payload = conclusion.payload if conclusion and isinstance(conclusion.payload, dict) else {}
    tasks = TaskMasterlist.objects.filter(origin__meeting_id=meeting_id).order_by("task_date", "title")
    topics = MeetingTopic.objects.filter(meeting_id=meeting_id).order_by("topic_index")
    facts = MeetingPeopleCandidate.objects.filter(meeting_id=meeting_id).order_by("ref")
    return {
        "meeting": MeetingDTO(meeting).data if meeting else None,
        "summary": (conclusion.summary if conclusion else None) or payload.get("summary"),
        "one_sentence_summary": (conclusion.one_sentence_summary if conclusion else None) or payload.get("one_sentence_summary"),
        "tl_dr": (conclusion.tl_dr if conclusion else None) or payload.get("tl_dr") or [],
        "action_items": payload.get("action_items") or payload.get("people_tasks") or [],
        "decisions": payload.get("decisions") or payload.get("key_decisions") or payload.get("decision_log") or [],
        "open_issues": payload.get("open_issues") or payload.get("issues") or [],
        "topics": [_topic_dto(row) for row in topics],
        "facts": [_fact_dto(row) for row in facts],
        "tasks": list(TaskMasterlistDTO(tasks, many=True).data),
        "conclusion": _conclusion_dto(conclusion) if conclusion else None,
        "raw_conclusion": payload,
    }


def meeting_progress(meeting_id: str, *, limit: int = 100) -> list[dict[str, Any]]:
    rows = MeetingPipelineRun.objects.filter(meeting_id=meeting_id).order_by("-created_at")[:limited(limit)]
    return list(MeetingPipelineRunDTO(rows, many=True).data)


def _topic_dto(row: MeetingTopic) -> dict[str, Any]:
    return {"id": row.id, "meeting_id": row.meeting_id, "topic_index": row.topic_index, "title": row.title, "summary": row.summary, "source_chunk_indexes": row.source_chunk_indexes or [], "confidence": row.confidence, "payload": row.payload or {}}


def _conclusion_dto(row: MeetingConclusion) -> dict[str, Any]:
    return {"id": row.id, "meeting_id": row.meeting_id, "title": row.title, "summary": row.summary, "one_sentence_summary": row.one_sentence_summary, "tl_dr": row.tl_dr or [], "source_topic_indexes": row.source_topic_indexes or [], "source_chunk_indexes": row.source_chunk_indexes or [], "confidence": row.confidence, "payload": row.payload or {}}


def _fact_dto(row: MeetingPeopleCandidate) -> dict[str, Any]:
    return {"ref": row.ref, "email": row.email_id, "alias_id": row.alias_id, "identity_type": row.identity_type, "display_label": row.display_label, "sources": row.sources or [], "confidence": row.confidence, "metadata_payload": row.metadata_payload or {}}


def list_jobs(*, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
    rows = ApplicationJob.objects.order_by("-created_at")[max(0, offset): max(0, offset) + limited(limit)]
    return list(ApplicationJobDTO(rows, many=True).data)


def get_job(job_id: str) -> dict[str, Any] | None:
    row = ApplicationJob.objects.filter(id=job_id).first()
    return ApplicationJobDTO(row).data if row else None


def job_logs(job_id: str, *, limit: int = 100) -> list[dict[str, Any]]:
    rows = ApplicationLog.objects.filter(correlation_id=job_id).order_by("created_at")[:limited(limit)]
    return list(ApplicationLogDTO(rows, many=True).data)


def job_progress(job_id: str, *, limit: int = 100) -> dict[str, Any]:
    row = ApplicationJob.objects.filter(id=job_id).first()
    if row is None:
        return {}
    logs = list(ApplicationLog.objects.filter(correlation_id=job_id).order_by("created_at")[:limited(limit)])
    return job_client.progress(row, logs)


def list_logs(*, limit: int = 100, meeting_id: str | None = None, correlation_id: str | None = None) -> list[dict[str, Any]]:
    rows = ApplicationLog.objects.order_by("-created_at")
    if meeting_id:
        rows = rows.filter(meeting_id=meeting_id)
    if correlation_id:
        rows = rows.filter(correlation_id=correlation_id)
    return list(ApplicationLogDTO(rows[:limited(limit)], many=True).data)


def list_task_masterlist(*, limit: int = 200, status: str | None = None) -> list[dict[str, Any]]:
    rows = TaskMasterlist.objects.order_by("-task_date", "title")
    if status:
        rows = rows.filter(status=status)
    return list(TaskMasterlistDTO(rows[:limited(limit)], many=True).data)


def task_assignees(task_id: str) -> list[dict[str, Any]]:
    rows = TaskAssigneeLink.objects.filter(masterlist_task_id=task_id).order_by("relation", "id")
    return list(TaskAssigneeLinkDTO(rows, many=True).data)


def task_external_links(task_id: str) -> list[dict[str, Any]]:
    rows = TaskExternalLink.objects.filter(masterlist_task_id=task_id).order_by("external_system", "id")
    return list(TaskExternalLinkDTO(rows, many=True).data)


def monday_boards(*, active_only: bool = True, limit: int = 200) -> list[dict[str, Any]]:
    rows = MondayBoard.objects.order_by("name")
    if active_only:
        rows = rows.filter(state="active")
    return list(MondayBoardDTO(rows[:limited(limit, maximum=1000)], many=True).data)


def monday_board_schema(board_id: str, *, include_archived_groups: bool = False) -> dict[str, Any]:
    board = MondayBoard.objects.filter(monday_board_id=str(board_id)).first()
    if board is None:
        raise ObjectDoesNotExist(f"Monday board not found: {board_id}")
    groups = list(MondayGroup.objects.filter(monday_board_id=str(board_id)).order_by("title"))
    if not include_archived_groups:
        groups = [group for group in groups if not group.archived and not group.deleted]
    columns = list(MondayColumn.objects.filter(monday_board_id=str(board_id)).order_by("title"))
    return serialize_board_schema(board=board, groups=groups, columns=columns)


def today_review_bundle(*, from_date: str, to_date: str, include_archived: bool = False) -> dict[str, Any]:
    start = date.fromisoformat(from_date)
    end = date.fromisoformat(to_date)
    if end < start:
        start, end = end, start

    rows = list(
        TaskMasterlist.objects.select_related("origin", "origin__meeting")
        .filter(Q(task_date__range=(start, end)) | Q(task_date__isnull=True, origin__meeting__started_at__date__range=(start, end)))
        .order_by("task_date", "origin__meeting__started_at", "title")
    )
    if not include_archived:
        rows = [row for row in rows if (row.status or "").lower() != "archived"]

    task_items: list[tuple[TaskMasterlist, date, Any]] = []
    board_ids: set[str] = set()
    person_emails: set[str] = set()
    for row in rows:
        meeting = row.origin.meeting if row.origin_id and row.origin and row.origin.meeting_id else None
        effective_date = row.task_date or (meeting.started_at.date() if meeting and meeting.started_at else None)
        if effective_date is None or effective_date < start or effective_date > end:
            continue
        task_items.append((row, effective_date, meeting))
        if row.monday_board_id:
            board_ids.add(str(row.monday_board_id))
        for link in TaskAssigneeLink.objects.filter(masterlist_task_id=row.id).select_related("email", "alias"):
            if link.email_id:
                person_emails.add(str(link.email_id))

    board_schemas = _today_review_board_schemas(board_ids=board_ids)
    readiness_by_task_id = {row.id: _task_readiness(row, board_schemas.get(str(row.monday_board_id))) for row, _, _ in task_items}

    grouped: OrderedDict[str, OrderedDict[tuple[str | None, str | None, bool], OrderedDict[str, dict[str, Any]]]] = OrderedDict()
    task_dtos = {item["id"]: item for item in TaskMasterlistDTO([row for row, _, _ in task_items], many=True).data}
    assignees_by_task = _assignees_by_task([row.id for row, _, _ in task_items])
    for row, effective_date, meeting in task_items:
        date_key = effective_date.isoformat()
        owner = _task_owner(row.id, assignees_by_task)
        meeting_id = str(meeting.id) if meeting else ""
        meeting_title = meeting.title if meeting else "No linked meeting"
        date_bucket = grouped.setdefault(date_key, OrderedDict())
        owner_bucket = date_bucket.setdefault((owner["email"], owner["alias_id"], owner["resolved"]), OrderedDict())
        meeting_bucket = owner_bucket.setdefault(meeting_id, {"meeting_id": meeting_id, "meeting_title": meeting_title, "tasks": []})
        meeting_bucket["tasks"].append(dict(task_dtos[row.id]))

    dates = [
        {
            "date": date_key,
            "groups": [
                {"email": email, "alias_id": alias_id, "resolved": resolved, "meetings": list(meetings.values())}
                for (email, alias_id, resolved), meetings in owners.items()
            ],
        }
        for date_key, owners in grouped.items()
    ]
    people = Person.objects.filter(email__in=person_emails).order_by("email") if person_emails else Person.objects.none()
    return {
        "from_date": start.isoformat(),
        "to_date": end.isoformat(),
        "dates": dates,
        "people": list(PersonDTO(people, many=True).data),
        "monday_boards": list(board_schemas.values()),
        "readiness_by_task_id": readiness_by_task_id,
    }


def _assignees_by_task(task_ids: list[str]) -> dict[str, list[TaskAssigneeLink]]:
    result: dict[str, list[TaskAssigneeLink]] = {task_id: [] for task_id in task_ids}
    for link in TaskAssigneeLink.objects.filter(masterlist_task_id__in=task_ids).select_related("email", "alias").order_by("relation", "id"):
        result.setdefault(str(link.masterlist_task_id), []).append(link)
    return result


def _task_owner(task_id: str, assignees_by_task: dict[str, list[TaskAssigneeLink]]) -> dict[str, Any]:
    links = assignees_by_task.get(task_id) or []
    primary = next((link for link in links if (link.relation or "").lower() == "owner"), links[0] if links else None)
    if primary is None:
        return {"email": None, "alias_id": None, "resolved": False}
    return {"email": primary.email_id, "alias_id": str(primary.alias_id) if primary.alias_id else None, "resolved": bool(primary.email_id)}


def _today_review_board_schemas(*, board_ids: set[str]) -> OrderedDict[str, dict[str, Any]]:
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


def _task_readiness(row: TaskMasterlist, board_schema: dict[str, Any] | None) -> dict[str, Any]:
    if not row.monday_board_id or board_schema is None:
        return {"state": "unknown", "label": "No Monday board selected", "missing_column_ids": [], "missing_column_titles": []}
    if not row.monday_group_id:
        return {"state": "no-group", "label": "Monday group is not selected", "missing_column_ids": [], "missing_column_titles": []}
    values = row.monday_field_values or {}
    missing = []
    for column in board_schema.get("columns") or []:
        if not column.get("required"):
            continue
        column_id = str(column.get("monday_column_id") or "")
        value = values.get(column_id)
        if value in (None, "", [], {}):
            missing.append(column)
    if missing:
        return {"state": "missing", "label": f"Missing {len(missing)} required Monday field(s)", "missing_column_ids": [str(item.get("monday_column_id") or "") for item in missing], "missing_column_titles": [str(item.get("title") or "") for item in missing]}
    return {"state": "ready", "label": "Ready to submit", "missing_column_ids": [], "missing_column_titles": []}
