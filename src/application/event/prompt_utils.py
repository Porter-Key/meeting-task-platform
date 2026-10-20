from __future__ import annotations

from typing import Any


def compact(value: Any, limit: int = 500) -> str:
    if value is None:
        return ""
    return str(value).strip()[:limit]


def chunk_text_limit(chunk_count: int) -> int:
    if chunk_count <= 12:
        return 500
    if chunk_count <= 20:
        return 420
    if chunk_count <= 30:
        return 320
    if chunk_count <= 80:
        return 220
    return 160
