from __future__ import annotations

from uuid import uuid4


def new_id(prefix: str = "id") -> str:
    return f"{prefix}_{uuid4().hex}"


def new_job_id() -> str:
    return new_id("job")


def new_task_id() -> str:
    return new_id("task")


def new_origin_id() -> str:
    return new_id("origin")


def new_version_id() -> str:
    return new_id("version")


def new_assignee_id() -> str:
    return new_id("assignee")
