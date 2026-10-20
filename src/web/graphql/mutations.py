from __future__ import annotations

import strawberry
from strawberry.scalars import JSON

from application.tasks.meeting import delete_meeting_task, generate_events_task, meeting_pipeline_task, wash_meeting_task
from application.tasks.task_masterlist import submit_task_masterlist_items_task
from django_client import people as people_client
from django_client import task_masterlist as task_client
from web.graphql.TodayApi import service as today_service
from web.graphql.TodayApi.types import TodaySubmitResult, TodayTaskMutationResult, TodayTaskPatchInput
from web.graphql.jobs import enqueue_task
from web.graphql.types import JobAcceptedType, PersonAliasType, PersonType, TaskMasterlistType


@strawberry.input
class TaskAssigneeInput:
    email: str | None = None
    alias: str | None = None
    alias_id: str | None = None
    relation: str = "assignee"
    confidence: float = 1.0
    metadata: JSON | None = None


@strawberry.input
class TaskCreateInput:
    task_date: str
    title: str
    action: str = ""
    context: str = ""
    priority: str = "medium"
    status: str = "draft"
    changed_by: str | None = None
    assignees: list[TaskAssigneeInput] | None = None
    metadata: JSON | None = None


@strawberry.input
class TaskUpdateInput:
    task_id: str | None = None
    id: str | None = None
    title: str | None = None
    action: str | None = None
    context: str | None = None
    priority: str | None = None
    status: str | None = None
    due_date: str | None = None
    due_note: str | None = None
    monday_board_id: str | None = None
    monday_board_name: str | None = None
    monday_group_id: str | None = None
    monday_group_title: str | None = None
    monday_schema_version: str | None = None
    monday_field_values: JSON | None = None
    assignees: list[TaskAssigneeInput] | None = None
    changed_by: str | None = None


@strawberry.input
class MondayTaskFieldsInput:
    task_ids: list[str]
    monday_board_id: str | None = None
    monday_board_name: str | None = None
    monday_group_id: str | None = None
    monday_group_title: str | None = None
    monday_field_values: JSON | None = None
    changed_by: str | None = None


@strawberry.input
class PersonInput:
    email: str
    identity_type: str = "alias"
    role: str | None = None
    is_active: bool = True
    source: str = "manual"
    metadata: JSON | None = None


@strawberry.input
class PersonAliasInput:
    alias: str
    email: str | None = None
    source: str = "manual"
    confidence: float = 1.0
    metadata: JSON | None = None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def trigger_meeting_pipeline(self, meeting_id: str) -> JobAcceptedType:
        return JobAcceptedType(**enqueue_task(command="meeting-pipeline", task_func=meeting_pipeline_task, payload={"meeting_id": meeting_id}, meeting_ids=[meeting_id]))

    @strawberry.mutation
    def delete_meeting(self, meeting_id: str) -> JobAcceptedType:
        return JobAcceptedType(**enqueue_task(command="delete-meeting", task_func=delete_meeting_task, payload={"meeting_id": meeting_id}, meeting_ids=[meeting_id]))

    @strawberry.mutation
    def trigger_generate_events(self, meeting_id: str) -> JobAcceptedType:
        return JobAcceptedType(**enqueue_task(command="generate-events", task_func=generate_events_task, payload={"meeting_id": meeting_id}, meeting_ids=[meeting_id]))

    @strawberry.mutation
    def trigger_wash_meeting(self, meeting_id: str) -> JobAcceptedType:
        return JobAcceptedType(**enqueue_task(command="wash-meeting", task_func=wash_meeting_task, payload={"meeting_id": meeting_id}, meeting_ids=[meeting_id]))

    @strawberry.mutation
    def set_today_task_due_date(self, task_id: str, due_date: str | None, due_note: str | None = None, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(today_service.set_due_date(task_id, due_date=due_date, due_note=due_note, changed_by=changed_by))

    @strawberry.mutation
    def clear_today_task_due_date(self, task_id: str, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(today_service.set_due_date(task_id, due_date=None, due_note="", changed_by=changed_by))

    @strawberry.mutation
    def set_due_date(self, task_id: str, due_date: str | None, due_note: str | None = None, changed_by: str | None = None) -> TodayTaskMutationResult:
        return self.set_today_task_due_date(task_id=task_id, due_date=due_date, due_note=due_note, changed_by=changed_by)

    @strawberry.mutation
    def clear_due_date(self, task_id: str, changed_by: str | None = None) -> TodayTaskMutationResult:
        return self.clear_today_task_due_date(task_id=task_id, changed_by=changed_by)

    @strawberry.mutation
    def set_today_task_monday_target(self, task_id: str, board_id: str, group_id: str, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(today_service.set_monday_target(task_id, board_id=board_id, group_id=group_id, changed_by=changed_by))

    @strawberry.mutation
    def choose_monday_group(self, task_id: str, board_id: str, group_id: str, changed_by: str | None = None) -> TodayTaskMutationResult:
        return self.set_today_task_monday_target(task_id=task_id, board_id=board_id, group_id=group_id, changed_by=changed_by)

    @strawberry.mutation
    def save_today_task_schema(self, task_id: str, values: JSON, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(today_service.save_schema(task_id, values=values or {}, changed_by=changed_by))

    @strawberry.mutation
    def save_required_fields(self, task_id: str, values: JSON, changed_by: str | None = None) -> TodayTaskMutationResult:
        return self.save_today_task_schema(task_id=task_id, values=values, changed_by=changed_by)

    @strawberry.mutation
    def update_today_task_fields(self, task_id: str, patch: TodayTaskPatchInput, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(today_service.update_fields(task_id, patch={key: value for key, value in patch.__dict__.items() if value is not None}, changed_by=changed_by))

    @strawberry.mutation
    def submit_today_tasks(self, task_ids: list[str], changed_by: str | None = None) -> TodaySubmitResult:
        return TodaySubmitResult.from_dto(today_service.submit_today_tasks(task_ids, changed_by=changed_by))

    @strawberry.mutation
    def submit_tasks(self, task_ids: list[str], changed_by: str | None = None) -> TodaySubmitResult:
        return self.submit_today_tasks(task_ids=task_ids, changed_by=changed_by)

    @strawberry.mutation
    def archive_today_tasks(self, task_ids: list[str], changed_by: str | None = None) -> list[TodayTaskMutationResult]:
        return [TodayTaskMutationResult.from_dto(item) for item in today_service.archive_tasks(task_ids, changed_by=changed_by)]

    @strawberry.mutation
    def archive_tasks(self, task_ids: list[str], changed_by: str | None = None) -> list[TodayTaskMutationResult]:
        return self.archive_today_tasks(task_ids=task_ids, changed_by=changed_by)

    @strawberry.mutation
    def reject_today_tasks(self, task_ids: list[str], changed_by: str | None = None) -> list[TodayTaskMutationResult]:
        return [TodayTaskMutationResult.from_dto(item) for item in today_service.reject_tasks(task_ids, changed_by=changed_by)]

    @strawberry.mutation
    def reject_tasks(self, task_ids: list[str], changed_by: str | None = None) -> list[TodayTaskMutationResult]:
        return self.reject_today_tasks(task_ids=task_ids, changed_by=changed_by)

    @strawberry.mutation
    def create_task_masterlist_item(self, input: TaskCreateInput) -> TaskMasterlistType:
        from datetime import date

        data = task_client.create(task_date=date.fromisoformat(input.task_date), title=input.title, action=input.action, context=input.context, priority=input.priority, status=input.status, changed_by=input.changed_by, assignees=[item.__dict__ for item in input.assignees or []], metadata=input.metadata or {})
        return TaskMasterlistType.from_dto(data)

    @strawberry.mutation
    def update_task_masterlist_item(self, input: TaskUpdateInput) -> TaskMasterlistType:
        task_id = input.task_id or input.id
        if not task_id:
            raise ValueError("task_id_required")
        patch = {key: value for key, value in input.__dict__.items() if key not in {"task_id", "id", "changed_by"} and value is not None}
        if input.assignees is not None:
            patch["assignees"] = [item.__dict__ for item in input.assignees]
        data = task_client.update(task_id, patch, changed_by=input.changed_by)
        if data is None:
            raise ValueError("task_not_found")
        return TaskMasterlistType.from_dto(data)

    @strawberry.mutation
    def archive_task_masterlist_items(self, task_ids: list[str], changed_by: str | None = None) -> list[TaskMasterlistType]:
        return [TaskMasterlistType.from_dto(item) for item in task_client.archive(task_ids, changed_by=changed_by)]

    @strawberry.mutation
    def restore_task_masterlist_items(self, task_ids: list[str], changed_by: str | None = None, status: str = "saved") -> list[TaskMasterlistType]:
        return [TaskMasterlistType.from_dto(item) for item in task_client.restore(task_ids, changed_by=changed_by, status=status)]

    @strawberry.mutation
    def submit_task_masterlist_items(self, task_ids: list[str], changed_by: str | None = None) -> JobAcceptedType:
        return JobAcceptedType(**enqueue_task(command="submit-task-masterlist-items", task_func=submit_task_masterlist_items_task, payload={"task_ids": task_ids, "changed_by": changed_by, "dry_run": False}, meeting_ids=[]))

    @strawberry.mutation
    def set_task_monday_fields(self, input: MondayTaskFieldsInput) -> list[TaskMasterlistType]:
        return [TaskMasterlistType.from_dto(item) for item in task_client.set_monday_fields(input.task_ids, monday_board_id=input.monday_board_id, monday_board_name=input.monday_board_name, monday_group_id=input.monday_group_id, monday_group_title=input.monday_group_title, monday_field_values=input.monday_field_values, changed_by=input.changed_by)]

    @strawberry.mutation
    def upsert_person(self, input: PersonInput) -> PersonType:
        return PersonType.from_dto(people_client.upsert_person(email=input.email, identity_type=input.identity_type, role=input.role, is_active=input.is_active, source=input.source, metadata=input.metadata or {}))

    @strawberry.mutation
    def upsert_person_alias(self, input: PersonAliasInput) -> PersonAliasType:
        return PersonAliasType.from_dto(people_client.upsert_alias(alias=input.alias, email=input.email, source=input.source, confidence=input.confidence, metadata=input.metadata or {}))

    @strawberry.mutation
    def add_person_email_alias(self, owner_email: str, alias_email: str, is_primary: bool = False, source: str = "manual", metadata: JSON | None = None) -> JSON:
        return people_client.add_email_alias(owner_email=owner_email, alias_email=alias_email, is_primary=is_primary, source=source, metadata=metadata or {})
