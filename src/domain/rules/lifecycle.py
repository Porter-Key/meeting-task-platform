from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


LifecycleSubjectType = Literal["meeting", "beat_schedule", "job"]

MEETING_STAGES = frozenset({"ingest", "ingested", "process", "wash", "washed", "generate", "event_generation", "topic_generated", "conclusion_generated", "task_extracted", "masterlist_sync", "pipeline"})
BEAT_STAGES = frozenset({"schedule", "dispatch", "run"})
JOB_STAGES = frozenset({"job"})

ACTIVE_STATUSES = frozenset({"queued", "running", "retryable_failed", "failed_retryable"})
TERMINAL_STATUSES = frozenset({"completed", "ready", "terminal_failed", "blocked_terminal", "skipped_terminal", "no_tasks", "no_tasks_terminal", "disabled", "blocked"})
RETRYABLE_STATUSES = frozenset({"retryable_failed", "failed_retryable"})

STATUS_ALIASES = {
    "failed_retryable": "retryable_failed",
    "blocked_terminal": "terminal_failed",
    "skipped_terminal": "skipped",
    "no_tasks_terminal": "no_tasks",
}

ALLOWED_TRANSITIONS: dict[str | None, frozenset[str]] = {
    None: frozenset({"queued", "running", "ingested", "completed", "ready", "failed", "skipped", "enabled", "disabled", "blocked", "retryable_failed", "failed_retryable", "terminal_failed", "blocked_terminal", "skipped_terminal", "no_tasks", "no_tasks_terminal"}),
    "queued": frozenset({"queued", "running", "skipped", "failed", "disabled", "blocked", "retryable_failed", "failed_retryable", "terminal_failed", "blocked_terminal", "skipped_terminal"}),
    "running": frozenset({"completed", "ready", "failed", "skipped", "blocked", "retryable_failed", "failed_retryable", "terminal_failed", "blocked_terminal", "skipped_terminal", "no_tasks", "no_tasks_terminal"}),
    "enabled": frozenset({"enabled", "queued", "running", "disabled"}),
    "disabled": frozenset({"disabled", "enabled"}),
    "completed": frozenset({"completed", "running"}),
    "ingested": frozenset({"ingested", "running"}),
    "ready": frozenset({"ready", "running"}),
    "failed": frozenset({"running", "queued", "completed", "ready", "blocked", "blocked_terminal", "retryable_failed", "failed_retryable"}),
    "retryable_failed": frozenset({"retryable_failed", "running", "queued", "terminal_failed", "blocked_terminal", "failed_retryable"}),
    "failed_retryable": frozenset({"failed_retryable", "running", "queued", "terminal_failed", "blocked_terminal", "retryable_failed"}),
    "skipped": frozenset({"queued", "running", "skipped"}),
    "blocked": frozenset({"queued", "running", "disabled", "blocked"}),
    "terminal_failed": frozenset({"terminal_failed", "running"}),
    "blocked_terminal": frozenset({"blocked_terminal", "running", "terminal_failed"}),
    "skipped_terminal": frozenset({"skipped_terminal", "running", "blocked_terminal", "failed_retryable"}),
    "no_tasks": frozenset({"no_tasks", "running"}),
    "no_tasks_terminal": frozenset({"no_tasks_terminal", "running", "blocked_terminal", "failed_retryable"}),
}


@dataclass(frozen=True, slots=True)
class LifecycleDecision:
    allowed: bool
    reason: str
    subject_type: str
    stage: str
    from_status: str | None
    to_status: str
    canonical_to_status: str
    metadata: dict[str, Any]

    def model_dump(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "subject_type": self.subject_type,
            "stage": self.stage,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "canonical_to_status": self.canonical_to_status,
            "metadata": self.metadata,
        }


def canonical_status(status: str | None) -> str | None:
    if status is None:
        return None
    return STATUS_ALIASES.get(status, status)


def is_terminal(status: str | None) -> bool:
    return bool(status in TERMINAL_STATUSES or canonical_status(status) in TERMINAL_STATUSES)


def can_change_state(*, subject_type: LifecycleSubjectType, stage: str, from_status: str | None, to_status: str, metadata: dict[str, Any] | None = None) -> LifecycleDecision:
    allowed_stages = {"meeting": MEETING_STAGES, "beat_schedule": BEAT_STAGES, "job": JOB_STAGES}[subject_type]
    canonical_to = canonical_status(to_status) or to_status
    canonical_from = canonical_status(from_status)
    base = {"canonical_from_status": canonical_from, **(metadata or {})}
    if stage not in allowed_stages:
        return LifecycleDecision(False, "invalid_stage", subject_type, stage, from_status, to_status, canonical_to, base)
    allowed_next = ALLOWED_TRANSITIONS.get(canonical_from)
    if allowed_next is not None and canonical_to not in allowed_next:
        return LifecycleDecision(False, "invalid_transition", subject_type, stage, from_status, to_status, canonical_to, base)
    return LifecycleDecision(True, "domain_allowed", subject_type, stage, from_status, to_status, canonical_to, base)


def retry_attempt_decision(*, attempt: int, max_attempts: int, error: Exception | str) -> tuple[str, dict[str, Any]]:
    terminal = attempt >= max_attempts
    return ("terminal_failed" if terminal else "retryable_failed", {"attempt": attempt, "max_attempts": max_attempts, "terminal": terminal, "error": repr(error)})
