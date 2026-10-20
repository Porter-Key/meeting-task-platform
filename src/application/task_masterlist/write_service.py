from __future__ import annotations

from datetime import date
from typing import Any

from django_client.repositories import TaskMasterlistRepo


class TaskMasterlistWriteService:
    def __init__(self, repo: TaskMasterlistRepo) -> None:
        self.repo = repo

    def create(self, *, task_date: date, changed_by: str | None, task: dict[str, Any]) -> dict[str, Any]:
        return {"task": self.repo.create_manual(task_date=task_date, changed_by=changed_by, task=task)}

    def update(self, *, changed_by: str | None, updates: list[dict[str, Any]]) -> dict[str, Any]:
        return self.repo.apply_updates(changed_by=changed_by, updates=updates)

    def archive(self, *, changed_by: str | None, task_ids: list[str]) -> dict[str, Any]:
        return self.repo.archive(changed_by=changed_by, task_ids=task_ids)

    def restore(self, *, changed_by: str | None, task_ids: list[str], restore_status: str = "saved") -> dict[str, Any]:
        return self.repo.restore(changed_by=changed_by, task_ids=task_ids, restore_status=restore_status)

    def set_monday_target(self, *, changed_by: str | None, task_ids: list[str], monday_board_id: str, monday_group_id: str, monday_board_name: str | None = None, monday_group_title: str | None = None) -> dict[str, Any]:
        return self.repo.set_monday_target(changed_by=changed_by, task_ids=task_ids, monday_board_id=monday_board_id, monday_group_id=monday_group_id, monday_board_name=monday_board_name, monday_group_title=monday_group_title)

    def set_monday_group(self, *, changed_by: str | None, task_ids: list[str], monday_board_id: str, monday_group_id: str, monday_board_name: str | None = None, monday_group_title: str | None = None) -> dict[str, Any]:
        return self.set_monday_target(changed_by=changed_by, task_ids=task_ids, monday_board_id=monday_board_id, monday_group_id=monday_group_id, monday_board_name=monday_board_name, monday_group_title=monday_group_title)

    def clear_monday_group(self, *, changed_by: str | None, task_ids: list[str]) -> dict[str, Any]:
        return self.repo.clear_monday_target(changed_by=changed_by, task_ids=task_ids)
