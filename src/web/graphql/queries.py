from __future__ import annotations

import strawberry
from django.core.exceptions import ObjectDoesNotExist

from web.graphql import selectors
from web.graphql.TodayApi import service as today_service
from web.graphql.TodayApi.types import TodayReviewBundle
from web.graphql.types import ApplicationJobType, ApplicationLogType, MeetingDetailBundleType, MeetingPipelineRunType, MeetingType, MondayBoardSchemaType, MondayBoardType, TaskMasterlistType


@strawberry.type
class Query:
    @strawberry.field
    def meetings(self, limit: int = 50, offset: int = 0) -> list[MeetingType]:
        return [MeetingType.from_dto(item) for item in selectors.list_meetings(limit=limit, offset=offset)]

    @strawberry.field
    def meeting(self, id: str) -> MeetingType | None:
        data = selectors.get_meeting(id)
        return MeetingType.from_dto(data) if data else None

    @strawberry.field
    def meeting_detail_bundle(self, meeting_id: str) -> MeetingDetailBundleType:
        return MeetingDetailBundleType.from_dto(selectors.meeting_detail_bundle(meeting_id))

    @strawberry.field
    def meeting_progress(self, meeting_id: str, limit: int = 100) -> list[MeetingPipelineRunType]:
        return [MeetingPipelineRunType.from_dto(item) for item in selectors.meeting_progress(meeting_id, limit=limit)]

    @strawberry.field
    def jobs(self, limit: int = 50, offset: int = 0) -> list[ApplicationJobType]:
        return [ApplicationJobType.from_dto(item) for item in selectors.list_jobs(limit=limit, offset=offset)]

    @strawberry.field
    def job(self, id: str) -> ApplicationJobType | None:
        data = selectors.get_job(id)
        return ApplicationJobType.from_dto(data) if data else None

    @strawberry.field
    def logs(self, limit: int = 100, meeting_id: str | None = None, correlation_id: str | None = None) -> list[ApplicationLogType]:
        return [ApplicationLogType.from_dto(item) for item in selectors.list_logs(limit=limit, meeting_id=meeting_id, correlation_id=correlation_id)]

    @strawberry.field
    def task_masterlist(self, limit: int = 200, status: str | None = None) -> list[TaskMasterlistType]:
        return [TaskMasterlistType.from_dto(item) for item in selectors.list_task_masterlist(limit=limit, status=status)]

    @strawberry.field
    def monday_boards(self, active_only: bool = True, limit: int = 200) -> list[MondayBoardType]:
        return [MondayBoardType.from_dto(item) for item in selectors.monday_boards(active_only=active_only, limit=limit)]

    @strawberry.field
    def monday_board_schema(self, board_id: str, include_archived_groups: bool = False) -> MondayBoardSchemaType | None:
        try:
            return MondayBoardSchemaType.from_dto(selectors.monday_board_schema(board_id, include_archived_groups=include_archived_groups))
        except ObjectDoesNotExist:
            return None

    @strawberry.field
    def today_review_bundle(self, from_date: str, to_date: str, include_archived: bool = False) -> TodayReviewBundle:
        return TodayReviewBundle.from_dto(today_service.today_review_bundle(from_date=from_date, to_date=to_date, include_archived=include_archived))
