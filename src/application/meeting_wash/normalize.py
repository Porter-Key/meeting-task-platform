from __future__ import annotations

import re
from typing import Any


def compact_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_sentence(sentence: dict[str, Any]) -> dict[str, Any]:
    text = compact_text(sentence.get("text") or sentence.get("raw_text"))
    speaker = sentence.get("speaker_name") or f"speaker_{sentence.get('speaker_id')}"
    start = float(sentence.get("start_time") or 0.0)
    end = float(sentence.get("end_time") or start)
    return {
        "index": sentence.get("index"),
        "speaker": speaker,
        "start_time": start,
        "end_time": end,
        "text": text,
        "ai_filters": sentence.get("ai_filters") or {},
    }
