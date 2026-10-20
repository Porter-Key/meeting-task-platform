from __future__ import annotations

GENERATION_TERMINAL_STATUSES = frozenset({"completed", "ready", "blocked_terminal", "skipped_terminal", "no_tasks_terminal"})
PROCESSING_TERMINAL_STATUSES = frozenset({"completed", "ready", "blocked_terminal", "skipped_terminal", "no_tasks_terminal"})


def should_process_meeting(*, task_count: int, terminal_lifecycle_count: int, running_count: int = 0, attempt_count: int = 0, max_attempts: int = 3, has_chunks: bool = True) -> bool:
    """Return whether automation should spend processing/LLM work on a meeting."""
    return has_chunks and task_count == 0 and terminal_lifecycle_count == 0 and running_count == 0 and attempt_count < max_attempts
