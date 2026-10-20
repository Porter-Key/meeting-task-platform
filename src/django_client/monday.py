from __future__ import annotations

from typing import Any

from domain.models.monday import MondayBoard, MondayColumn, MondayGroup, MondayUser


def structure(*, active_only: bool = True, include_archived_groups: bool = False) -> dict[str, Any]:
    boards = MondayBoard.objects.all().order_by("name")
    if active_only:
        boards = boards.filter(state="active")
    return {"boards": [dump_board(board, include_archived_groups=include_archived_groups) for board in boards]}


def groups(*, board_id: str, include_archived: bool = False) -> dict[str, Any] | None:
    board = MondayBoard.objects.filter(monday_board_id=str(board_id)).first()
    if not board:
        return None
    query = MondayGroup.objects.filter(monday_board_id=str(board_id))
    if not include_archived:
        query = query.filter(archived=False, deleted=False)
    return {"board": dump_board(board, include_archived_groups=include_archived), "groups": [dump_group(row) for row in query.order_by("title")]}


def list_users(*, include_disabled: bool = False) -> list[dict[str, Any]]:
    query = MondayUser.objects.all()
    if not include_disabled:
        query = query.filter(enabled=True)
    return [{"id": row.id, "monday_user_id": row.monday_user_id, "name": row.name, "email": row.email, "title": row.title, "enabled": row.enabled} for row in query.order_by("name")]


def dump_board(board: MondayBoard, *, include_archived_groups: bool = False) -> dict[str, Any]:
    group_query = MondayGroup.objects.filter(monday_board_id=board.monday_board_id)
    if not include_archived_groups:
        group_query = group_query.filter(archived=False, deleted=False)
    columns = MondayColumn.objects.filter(monday_board_id=board.monday_board_id).order_by("title")
    return {"id": board.id, "monday_board_id": board.monday_board_id, "name": board.name, "workspace_id": board.workspace_id, "workspace_name": board.workspace_name, "state": board.state, "board_kind": board.board_kind, "groups": [dump_group(row) for row in group_query.order_by("title")], "columns": [{"id": row.id, "monday_column_id": row.monday_column_id, "title": row.title, "type": row.type, "required": row.required, "field_key": row.field_key} for row in columns]}


def dump_group(row: MondayGroup) -> dict[str, Any]:
    return {"id": row.id, "monday_group_id": row.monday_group_id, "title": row.title, "archived": row.archived, "deleted": row.deleted}
