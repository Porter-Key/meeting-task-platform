from __future__ import annotations

from datetime import date, datetime
from typing import Any

import strawberry
from strawberry.scalars import JSON


def _dt(value: Any) -> datetime | None:
    return value if isinstance(value, datetime) else None


def _date(value: Any) -> date | None:
    return value if isinstance(value, date) else None


@strawberry.type
class JobAcceptedType:
    job_id: str
    queue_task_id: str | None
    command: str
    status: str
    meeting_ids: list[str]


@strawberry.type
class ApplicationJobType:
    id: str
    queue_task_id: str | None
    command: str
    status: str
    meeting_ids: list[str]
    payload: JSON
    result: JSON
    error: str | None
    created_at: datetime | None
    updated_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> ApplicationJobType:
        return cls(id=str(data["id"]), queue_task_id=data.get("queue_task_id"), command=data.get("command") or "", status=data.get("status") or "", meeting_ids=list(data.get("meeting_ids") or []), payload=data.get("payload") or {}, result=data.get("result") or {}, error=data.get("error"), created_at=_dt(data.get("created_at")), updated_at=_dt(data.get("updated_at")), started_at=_dt(data.get("started_at")), finished_at=_dt(data.get("finished_at")))

    @strawberry.field
    def logs(self, limit: int = 100) -> list[ApplicationLogType]:
        from web.graphql import selectors

        return [ApplicationLogType.from_dto(item) for item in selectors.job_logs(self.id, limit=limit)]

    @strawberry.field
    def progress(self, limit: int = 100) -> JobProgressType:
        from web.graphql import selectors

        return JobProgressType.from_dto(selectors.job_progress(self.id, limit=limit))


@strawberry.type
class ApplicationLogType:
    id: str
    created_at: datetime | None
    level: str
    logger_name: str
    stage: str
    event: str
    message: str
    correlation_id: str | None
    meeting_id: str | None
    payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> ApplicationLogType:
        return cls(id=str(data["id"]), created_at=_dt(data.get("created_at")), level=data.get("level") or "", logger_name=data.get("logger_name") or "", stage=data.get("stage") or "", event=data.get("event") or "", message=data.get("message") or "", correlation_id=data.get("correlation_id"), meeting_id=data.get("meeting_id"), payload=data.get("payload") or {})


@strawberry.type
class JobProgressEventType:
    id: str
    created_at: datetime | None
    level: str
    stage: str
    event: str
    message: str
    meeting_id: str | None
    payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> JobProgressEventType:
        return cls(id=str(data.get("id") or ""), created_at=_dt(data.get("created_at")), level=data.get("level") or "", stage=data.get("stage") or "", event=data.get("event") or "", message=data.get("message") or "", meeting_id=data.get("meeting_id"), payload=data.get("payload") or {})


@strawberry.type
class JobProgressType:
    status: str
    current_stage: str | None
    current_event: str | None
    current_message: str | None
    current_meeting_id: str | None
    total_meetings: int | None
    completed_meetings: int
    percent: int | None
    started_at: datetime | None
    finished_at: datetime | None
    error: str | None
    events: list[JobProgressEventType]
    event_count: int
    has_events: bool
    is_stale: bool

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> JobProgressType:
        return cls(status=data.get("status") or "", current_stage=data.get("current_stage"), current_event=data.get("current_event"), current_message=data.get("current_message"), current_meeting_id=data.get("current_meeting_id"), total_meetings=data.get("total_meetings"), completed_meetings=int(data.get("completed_meetings") or 0), percent=data.get("percent"), started_at=_dt(data.get("started_at")), finished_at=_dt(data.get("finished_at")), error=data.get("error"), events=[JobProgressEventType.from_dto(item) for item in data.get("events") or []], event_count=int(data.get("event_count") or 0), has_events=bool(data.get("has_events")), is_stale=bool(data.get("is_stale")))


@strawberry.type
class MeetingType:
    id: str
    title: str
    started_at: datetime | None
    ended_at: datetime | None
    duration_seconds: int | None
    timezone: str | None
    metadata_payload: JSON
    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MeetingType:
        return cls(id=str(data["id"]), title=data.get("title") or "", started_at=_dt(data.get("started_at")), ended_at=_dt(data.get("ended_at")), duration_seconds=data.get("duration_seconds"), timezone=data.get("timezone"), metadata_payload=data.get("metadata_payload") or {}, created_at=_dt(data.get("created_at")), updated_at=_dt(data.get("updated_at")))


@strawberry.type
class MeetingPipelineRunType:
    id: str
    meeting_id: str
    pipeline_name: str
    stage: str
    status: str
    job_id: str | None
    started_at: datetime | None
    finished_at: datetime | None
    error: str | None
    metadata_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MeetingPipelineRunType:
        return cls(id=str(data["id"]), meeting_id=str(data.get("meeting") or data.get("meeting_id") or ""), pipeline_name=data.get("pipeline_name") or "", stage=data.get("stage") or "", status=data.get("status") or "", job_id=data.get("job") or data.get("job_id"), started_at=_dt(data.get("started_at")), finished_at=_dt(data.get("finished_at")), error=data.get("error"), metadata_payload=data.get("metadata_payload") or {})


@strawberry.type
class MeetingTopicType:
    id: str
    meeting_id: str
    topic_index: int
    title: str
    summary: str
    source_chunk_indexes: JSON
    confidence: float
    payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MeetingTopicType:
        return cls(id=str(data.get("id") or ""), meeting_id=str(data.get("meeting_id") or data.get("meeting") or ""), topic_index=int(data.get("topic_index") or 0), title=data.get("title") or "", summary=data.get("summary") or "", source_chunk_indexes=data.get("source_chunk_indexes") or [], confidence=float(data.get("confidence") or 0), payload=data.get("payload") or {})


@strawberry.type
class MeetingConclusionType:
    id: str
    meeting_id: str
    title: str
    summary: str
    one_sentence_summary: str | None
    tl_dr: JSON
    source_topic_indexes: JSON
    source_chunk_indexes: JSON
    confidence: float
    payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MeetingConclusionType:
        return cls(id=str(data.get("id") or ""), meeting_id=str(data.get("meeting_id") or data.get("meeting") or ""), title=data.get("title") or "", summary=data.get("summary") or "", one_sentence_summary=data.get("one_sentence_summary"), tl_dr=data.get("tl_dr") or [], source_topic_indexes=data.get("source_topic_indexes") or [], source_chunk_indexes=data.get("source_chunk_indexes") or [], confidence=float(data.get("confidence") or 0), payload=data.get("payload") or {})


@strawberry.type
class MeetingFactType:
    ref: str
    email: str | None
    alias_id: str | None
    identity_type: str
    display_label: str
    sources: JSON
    confidence: float
    metadata_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MeetingFactType:
        return cls(ref=str(data.get("ref") or ""), email=data.get("email"), alias_id=data.get("alias_id") or data.get("alias"), identity_type=data.get("identity_type") or "", display_label=data.get("display_label") or "", sources=data.get("sources") or [], confidence=float(data.get("confidence") or 0), metadata_payload=data.get("metadata_payload") or {})


@strawberry.type
class TaskMasterlistType:
    id: str
    task_date: date | None
    title: str
    action: str
    context: str
    priority: str
    status: str
    origin_id: str | None
    origin_type: str
    version: int
    due_date: date | None
    due_note: str | None
    monday_board_id: str | None
    monday_board_name: str | None
    monday_group_id: str | None
    monday_group_title: str | None
    monday_schema_version: str | None
    monday_field_values: JSON
    metadata_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TaskMasterlistType:
        return cls(id=str(data["id"]), task_date=_date(data.get("task_date")), title=data.get("title") or "", action=data.get("action") or "", context=data.get("context") or "", priority=data.get("priority") or "", status=data.get("status") or "", origin_id=data.get("origin_id") or data.get("origin"), origin_type=data.get("origin_type") or "", version=int(data.get("version") or 0), due_date=_date(data.get("due_date")), due_note=data.get("due_note"), monday_board_id=data.get("monday_board_id"), monday_board_name=data.get("monday_board_name"), monday_group_id=data.get("monday_group_id"), monday_group_title=data.get("monday_group_title"), monday_schema_version=data.get("monday_schema_version"), monday_field_values=data.get("monday_field_values") or {}, metadata_payload=data.get("metadata_payload") or {})

    @strawberry.field
    def assignees(self) -> list[TaskAssigneeLinkType]:
        from web.graphql import selectors

        return [TaskAssigneeLinkType.from_dto(item) for item in selectors.task_assignees(self.id)]

    @strawberry.field
    def external_links(self) -> list[TaskExternalLinkType]:
        from web.graphql import selectors

        return [TaskExternalLinkType.from_dto(item) for item in selectors.task_external_links(self.id)]


@strawberry.type
class MeetingDetailBundleType:
    meeting: MeetingType | None
    summary: str | None
    one_sentence_summary: str | None
    tl_dr: JSON
    action_items: JSON
    decisions: JSON
    open_issues: JSON
    topics: list[MeetingTopicType]
    facts: list[MeetingFactType]
    tasks: list[TaskMasterlistType]
    conclusion: MeetingConclusionType | None
    raw_conclusion: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MeetingDetailBundleType:
        conclusion = data.get("conclusion")
        return cls(meeting=MeetingType.from_dto(data["meeting"]) if data.get("meeting") else None, summary=data.get("summary"), one_sentence_summary=data.get("one_sentence_summary"), tl_dr=data.get("tl_dr") or [], action_items=data.get("action_items") or [], decisions=data.get("decisions") or [], open_issues=data.get("open_issues") or [], topics=[MeetingTopicType.from_dto(item) for item in data.get("topics") or []], facts=[MeetingFactType.from_dto(item) for item in data.get("facts") or []], tasks=[TaskMasterlistType.from_dto(item) for item in data.get("tasks") or []], conclusion=MeetingConclusionType.from_dto(conclusion) if conclusion else None, raw_conclusion=data.get("raw_conclusion") or {})


@strawberry.type
class TaskAssigneeLinkType:
    id: str
    masterlist_task_id: str
    email: str | None
    alias: str | None
    relation: str
    source: str
    confidence: float
    metadata_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TaskAssigneeLinkType:
        return cls(id=str(data["id"]), masterlist_task_id=str(data.get("masterlist_task") or ""), email=data.get("email"), alias=data.get("alias"), relation=data.get("relation") or "", source=data.get("source") or "", confidence=float(data.get("confidence") or 0), metadata_payload=data.get("metadata_payload") or {})


@strawberry.type
class TaskExternalLinkType:
    id: str
    masterlist_task_id: str
    external_system: str
    external_item_id: str | None
    external_board_id: str | None
    external_url: str | None
    sync_status: str
    last_synced_at: datetime | None
    error: str | None
    metadata_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TaskExternalLinkType:
        return cls(id=str(data["id"]), masterlist_task_id=str(data.get("masterlist_task") or ""), external_system=data.get("external_system") or "", external_item_id=data.get("external_item_id"), external_board_id=data.get("external_board_id"), external_url=data.get("external_url"), sync_status=data.get("sync_status") or "", last_synced_at=_dt(data.get("last_synced_at")), error=data.get("error"), metadata_payload=data.get("metadata_payload") or {})


@strawberry.type
class PersonType:
    email: str
    identity_type: str
    role: str | None
    is_active: bool
    source: str
    metadata_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> PersonType:
        return cls(email=data.get("email") or "", identity_type=data.get("identity_type") or "", role=data.get("role"), is_active=bool(data.get("is_active", True)), source=data.get("source") or "", metadata_payload=data.get("metadata_payload") or {})


@strawberry.type
class PersonAliasType:
    id: str
    alias: str
    normalized_alias: str
    email: str | None
    source: str
    confidence: float
    metadata_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> PersonAliasType:
        return cls(id=str(data.get("id") or ""), alias=data.get("alias") or "", normalized_alias=data.get("normalized_alias") or "", email=data.get("email"), source=data.get("source") or "", confidence=float(data.get("confidence") or 0), metadata_payload=data.get("metadata_payload") or {})


@strawberry.type
class MondayBoardType:
    id: str
    monday_board_id: str
    name: str
    workspace_id: str | None
    workspace_name: str | None
    state: str | None
    board_kind: str | None
    raw_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MondayBoardType:
        return cls(id=str(data["id"]), monday_board_id=str(data.get("monday_board_id") or ""), name=data.get("name") or "", workspace_id=data.get("workspace_id"), workspace_name=data.get("workspace_name"), state=data.get("state"), board_kind=data.get("board_kind"), raw_payload=data.get("raw_payload") or {})


@strawberry.type
class MondayGroupType:
    id: str
    monday_board_id: str
    monday_group_id: str
    title: str
    archived: bool
    deleted: bool
    raw_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MondayGroupType:
        return cls(id=str(data["id"]), monday_board_id=str(data.get("monday_board_id") or ""), monday_group_id=str(data.get("monday_group_id") or ""), title=data.get("title") or "", archived=bool(data.get("archived")), deleted=bool(data.get("deleted")), raw_payload=data.get("raw_payload") or {})


@strawberry.type
class MondayColumnSchemaType:
    id: str
    monday_board_id: str
    monday_column_id: str
    title: str
    type: str | None
    settings_str: str | None
    field_key: str | None
    required: bool
    writable: bool
    value_kind: str
    options: JSON
    schema_payload: JSON
    settings: JSON
    raw_payload: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MondayColumnSchemaType:
        return cls(id=str(data["id"]), monday_board_id=str(data.get("monday_board_id") or ""), monday_column_id=str(data.get("monday_column_id") or ""), title=data.get("title") or "", type=data.get("type"), settings_str=data.get("settings_str"), field_key=data.get("field_key"), required=bool(data.get("required")), writable=bool(data.get("writable")), value_kind=data.get("value_kind") or "json", options=data.get("options") or [], schema_payload=data.get("schema_payload") or {}, settings=data.get("settings") or {}, raw_payload=data.get("raw_payload") or {})


@strawberry.type
class MondayBoardSchemaType:
    board: MondayBoardType
    groups: list[MondayGroupType]
    columns: list[MondayColumnSchemaType]
    required_columns: list[MondayColumnSchemaType]
    writable_columns: list[MondayColumnSchemaType]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> MondayBoardSchemaType:
        return cls(board=MondayBoardType.from_dto(data["board"]), groups=[MondayGroupType.from_dto(item) for item in data.get("groups") or []], columns=[MondayColumnSchemaType.from_dto(item) for item in data.get("columns") or []], required_columns=[MondayColumnSchemaType.from_dto(item) for item in data.get("required_columns") or []], writable_columns=[MondayColumnSchemaType.from_dto(item) for item in data.get("writable_columns") or []])


@strawberry.type
class TodayReviewMeetingType:
    meeting_id: str
    meeting_title: str
    tasks: list[TaskMasterlistType]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewMeetingType:
        return cls(meeting_id=str(data.get("meeting_id") or ""), meeting_title=data.get("meeting_title") or "", tasks=[TaskMasterlistType.from_dto(item) for item in data.get("tasks") or []])


@strawberry.type
class TodayReviewOwnerGroupType:
    email: str | None
    alias_id: str | None
    resolved: bool
    meetings: list[TodayReviewMeetingType]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewOwnerGroupType:
        return cls(email=data.get("email"), alias_id=data.get("alias_id"), resolved=bool(data.get("resolved")), meetings=[TodayReviewMeetingType.from_dto(item) for item in data.get("meetings") or []])


@strawberry.type
class TodayReviewDateType:
    date: str
    groups: list[TodayReviewOwnerGroupType]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewDateType:
        return cls(date=str(data.get("date") or ""), groups=[TodayReviewOwnerGroupType.from_dto(item) for item in data.get("groups") or []])


@strawberry.type
class TodayReviewBoardType:
    board_id: str
    name: str
    workspace_name: str | None
    groups: list[MondayGroupType]
    columns: list[MondayColumnSchemaType]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewBoardType:
        return cls(board_id=str(data.get("board_id") or ""), name=data.get("name") or "", workspace_name=data.get("workspace_name"), groups=[MondayGroupType.from_dto(item) for item in data.get("groups") or []], columns=[MondayColumnSchemaType.from_dto(item) for item in data.get("columns") or []])


@strawberry.type
class TaskReadinessType:
    state: str
    label: str
    missing_column_ids: list[str]
    missing_column_titles: list[str]

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TaskReadinessType:
        return cls(state=data.get("state") or "unknown", label=data.get("label") or "Unknown", missing_column_ids=[str(item) for item in data.get("missing_column_ids") or []], missing_column_titles=[str(item) for item in data.get("missing_column_titles") or []])


@strawberry.type
class TaskReadinessEntryType:
    task_id: str
    readiness: TaskReadinessType

    @classmethod
    def from_dto(cls, task_id: str, data: dict[str, Any]) -> TaskReadinessEntryType:
        return cls(task_id=str(task_id), readiness=TaskReadinessType.from_dto(data))


@strawberry.type
class TodayReviewBundleType:
    from_date: str
    to_date: str
    dates: list[TodayReviewDateType]
    people: list[PersonType]
    monday_boards: list[TodayReviewBoardType]
    readiness_by_task_id: JSON

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> TodayReviewBundleType:
        return cls(from_date=str(data.get("from_date") or ""), to_date=str(data.get("to_date") or ""), dates=[TodayReviewDateType.from_dto(item) for item in data.get("dates") or []], people=[PersonType.from_dto(item) for item in data.get("people") or []], monday_boards=[TodayReviewBoardType.from_dto(item) for item in data.get("monday_boards") or []], readiness_by_task_id=data.get("readiness_by_task_id") or {})
