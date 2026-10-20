from __future__ import annotations

from datetime import date, datetime
from typing import Any

import strawberry
from strawberry.scalars import JSON

from web.graphql.types import JobAcceptedType, MondayColumnSchemaType, MondayGroupType, PersonType, TodayReviewBoardType


def _date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _dt(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


@strawberry.type
class TodayTaskReadiness:
    state: str
    can_submit: bool
    label: str
    missing_fields: JSON
    blocking_reasons: list[str]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayTaskReadiness:
        return cls(
            state=data.get("state") or "blocked",
            can_submit=bool(data.get("canSubmit", data.get("can_submit"))),
            label=data.get("label") or "Blocked",
            missing_fields=data.get("missingFields", data.get("missing_fields")) or [],
            blocking_reasons=[str(item) for item in data.get("blockingReasons", data.get("blocking_reasons")) or []],
        )


@strawberry.type
class TodayMondayTarget:
    board_id: str | None
    board_name: str | None
    group_id: str | None
    group_title: str | None

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayMondayTarget:
        return cls(board_id=data.get("board_id"), board_name=data.get("board_name"), group_id=data.get("group_id"), group_title=data.get("group_title"))


@strawberry.type
class TodayTask:
    id: str
    title: str
    action: str
    status: str
    priority: str
    due_date: date | None
    due_note: str | None
    monday_target: TodayMondayTarget
    monday_fields: JSON
    readiness: TodayTaskReadiness
    available_actions: list[str]
    action_state: str
    meeting_id: str | None
    meeting_title: str | None
    owner: JSON
    changed_at: datetime | None

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayTask:
        return cls(
            id=str(data.get("id") or ""),
            title=data.get("title") or "",
            action=data.get("action") or "",
            status=data.get("status") or "",
            priority=data.get("priority") or "",
            due_date=_date(data.get("due_date")),
            due_note=data.get("due_note"),
            monday_target=TodayMondayTarget.from_dto(data.get("monday_target") or {}),
            monday_fields=data.get("monday_fields") or {},
            readiness=TodayTaskReadiness.from_dto(data.get("readiness") or {}),
            available_actions=[str(item) for item in data.get("available_actions") or []],
            action_state=data.get("action_state") or "idle",
            meeting_id=data.get("meeting_id"),
            meeting_title=data.get("meeting_title"),
            owner=data.get("owner") or {},
            changed_at=_dt(data.get("changed_at")),
        )


@strawberry.type
class TodayReviewMeeting:
    meeting_id: str
    meeting_title: str
    tasks: list[TodayTask]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewMeeting:
        return cls(meeting_id=str(data.get("meeting_id") or ""), meeting_title=data.get("meeting_title") or "", tasks=[TodayTask.from_dto(item) for item in data.get("tasks") or []])


@strawberry.type
class TodayReviewOwnerGroup:
    email: str | None
    alias_id: str | None
    resolved: bool
    meetings: list[TodayReviewMeeting]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewOwnerGroup:
        return cls(email=data.get("email"), alias_id=data.get("alias_id"), resolved=bool(data.get("resolved")), meetings=[TodayReviewMeeting.from_dto(item) for item in data.get("meetings") or []])


@strawberry.type
class TodayReviewDate:
    date: str
    groups: list[TodayReviewOwnerGroup]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewDate:
        return cls(date=str(data.get("date") or ""), groups=[TodayReviewOwnerGroup.from_dto(item) for item in data.get("groups") or []])


@strawberry.type
class TodayReviewBundle:
    from_date: str
    to_date: str
    bundle_version: str
    generated_at: datetime
    dates: list[TodayReviewDate]
    people: list[PersonType]
    monday_boards: list[TodayReviewBoardType]
    readiness_by_task_id: JSON
    pending_jobs_by_task_id: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewBundle:
        return cls(
            from_date=str(data.get("from_date") or ""),
            to_date=str(data.get("to_date") or ""),
            bundle_version=str(data.get("bundle_version") or ""),
            generated_at=_dt(data.get("generated_at")) or datetime.now(),
            dates=[TodayReviewDate.from_dto(item) for item in data.get("dates") or []],
            people=[PersonType.from_dto(item) for item in data.get("people") or []],
            monday_boards=[TodayReviewBoardType.from_dto(item) for item in data.get("monday_boards") or []],
            readiness_by_task_id=data.get("readiness_by_task_id") or {},
            pending_jobs_by_task_id=data.get("pending_jobs_by_task_id") or {},
        )


@strawberry.type
class TodayTaskMutationResult:
    task: TodayTask
    readiness: TodayTaskReadiness
    bundle_version: str

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayTaskMutationResult:
        task = TodayTask.from_dto(data.get("task") or {})
        return cls(task=task, readiness=TodayTaskReadiness.from_dto(data.get("readiness") or {}), bundle_version=str(data.get("bundle_version") or ""))


@strawberry.type
class TodayBlockedTask:
    task_id: str
    readiness: TodayTaskReadiness
    reason: str

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayBlockedTask:
        return cls(task_id=str(data.get("task_id") or ""), readiness=TodayTaskReadiness.from_dto(data.get("readiness") or {}), reason=data.get("reason") or "blocked")


@strawberry.type
class TodaySubmitResult:
    job: JobAcceptedType | None
    accepted_task_ids: list[str]
    blocked_tasks: list[TodayBlockedTask]
    bundle_version: str

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodaySubmitResult:
        job = JobAcceptedType(**data["job"]) if data.get("job") else None
        return cls(job=job, accepted_task_ids=[str(item) for item in data.get("accepted_task_ids") or []], blocked_tasks=[TodayBlockedTask.from_dto(item) for item in data.get("blocked_tasks") or []], bundle_version=str(data.get("bundle_version") or ""))


@strawberry.input
class TodayTaskPatchInput:
    title: str | None = None
    action: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: str | None = None
    due_note: str | None = None
    monday_fields: JSON | None = None
