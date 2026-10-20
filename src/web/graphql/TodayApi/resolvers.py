from __future__ import annotations

import strawberry
from strawberry.scalars import JSON

from web.graphql.TodayApi import service
from web.graphql.TodayApi.types import TodayReviewBundle, TodaySubmitResult, TodayTaskMutationResult, TodayTaskPatchInput


class TodayQueryMixin:
    @strawberry.field
    def today_review_bundle(self, from_date: str, to_date: str, include_archived: bool = False) -> TodayReviewBundle:
        return TodayReviewBundle.from_dto(service.today_review_bundle(from_date=from_date, to_date=to_date, include_archived=include_archived))


class TodayMutationMixin:
    @strawberry.mutation
    def set_today_task_due_date(self, task_id: str, due_date: str | None, due_note: str | None = None, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(service.set_due_date(task_id, due_date=due_date, due_note=due_note, changed_by=changed_by))

    @strawberry.mutation
    def clear_today_task_due_date(self, task_id: str, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(service.set_due_date(task_id, due_date=None, due_note=None, changed_by=changed_by))

    @strawberry.mutation
    def set_today_task_monday_target(self, task_id: str, board_id: str, group_id: str, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(service.set_monday_target(task_id, board_id=board_id, group_id=group_id, changed_by=changed_by))

    @strawberry.mutation
    def choose_monday_group(self, task_id: str, board_id: str, group_id: str, changed_by: str | None = None) -> TodayTaskMutationResult:
        return self.set_today_task_monday_target(task_id=task_id, board_id=board_id, group_id=group_id, changed_by=changed_by)

    @strawberry.mutation
    def save_today_task_schema(self, task_id: str, values: JSON, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(service.save_schema(task_id, values=values or {}, changed_by=changed_by))

    @strawberry.mutation
    def save_required_fields(self, task_id: str, values: JSON, changed_by: str | None = None) -> TodayTaskMutationResult:
        return self.save_today_task_schema(task_id=task_id, values=values, changed_by=changed_by)

    @strawberry.mutation
    def update_today_task_fields(self, task_id: str, patch: TodayTaskPatchInput, changed_by: str | None = None) -> TodayTaskMutationResult:
        return TodayTaskMutationResult.from_dto(service.update_fields(task_id, patch={key: value for key, value in patch.__dict__.items() if value is not None}, changed_by=changed_by))

    @strawberry.mutation
    def submit_today_tasks(self, task_ids: list[str], changed_by: str | None = None) -> TodaySubmitResult:
        return TodaySubmitResult.from_dto(service.submit_today_tasks(task_ids, changed_by=changed_by))
