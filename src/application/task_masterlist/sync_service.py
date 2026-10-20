from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from django_client.repositories import TaskMasterlistRepo


@dataclass(slots=True)
class TaskMasterlistSyncService:
    """Build the frontend masterlist from stable task origins.

    `task_origins` are source/evidence rows produced by meeting generation.
    `task_masterlist` is the editable frontend workbench. This service owns the
    application boundary between those two concepts so event generation does not
    directly call the persistence repo.
    """

    task_masterlist: TaskMasterlistRepo

    def sync_meeting(self, *, meeting_id: str, task_date: date | None = None) -> dict[str, Any]:
        return self.task_masterlist.sync_from_meeting(meeting_id=meeting_id, task_date=task_date)

    def rebuild_meetings(self, *, meeting_ids: list[str], delete_existing: bool = True) -> dict[str, Any]:
        deleted = self.task_masterlist.delete_for_meetings(meeting_ids) if delete_existing else {"skipped": True}
        rebuilt = [self.sync_meeting(meeting_id=meeting_id) for meeting_id in dict.fromkeys(meeting_ids) if meeting_id]
        return {"deleted": deleted, "rebuilt": rebuilt, "created": sum(item.get("created", 0) for item in rebuilt)}
