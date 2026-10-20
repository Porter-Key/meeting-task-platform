from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FailureDecision:
    status: str
    reason: str
    retryable: bool
    cleanup_artifacts: bool = True
    disable_beat: bool = False


def classify_pipeline_error(error: Exception | str) -> FailureDecision:
    text = repr(error) if not isinstance(error, str) else error
    lowered = text.lower()
    if "insufficient_user_quota" in lowered or "用户额度不足" in lowered or "permissiondeniederror" in lowered:
        return FailureDecision(status="blocked_terminal", reason="llm_quota_exhausted", retryable=False, disable_beat=True)
    if "apiconnectionerror" in lowered or "timeout" in lowered or "temporar" in lowered or "503" in lowered:
        return FailureDecision(status="failed_retryable", reason="transient_provider_error", retryable=True)
    if "validationerror" in lowered or "invalid" in lowered:
        return FailureDecision(status="blocked_terminal", reason="validation_or_schema_error", retryable=False)
    return FailureDecision(status="failed_retryable", reason="unknown_retryable_error", retryable=True)
