from __future__ import annotations

from typing import Any

from .normalize import normalize_sentence


def build_chunks(sentences: list[dict[str, Any]], *, max_words: int = 300, max_gap: float = 2.5) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw in sentences:
        sentence = normalize_sentence(raw)
        if not sentence["text"]:
            continue
        words = len(sentence["text"].split())
        new_chunk = current is None
        if current is not None:
            new_chunk = sentence["speaker"] != current["speaker"] or sentence["start_time"] - float(current["end_time"]) > max_gap or int(current["word_count"]) + words > max_words
        if new_chunk:
            current = {
                "chunk_index": len(chunks),
                "speaker": sentence["speaker"],
                "start_time": sentence["start_time"],
                "end_time": sentence["end_time"],
                "sentence_indexes": [sentence.get("index")],
                "text": sentence["text"],
                "word_count": words,
                "ai_filters": [sentence.get("ai_filters") or {}],
            }
            chunks.append(current)
        else:
            current["end_time"] = sentence["end_time"]
            current["sentence_indexes"].append(sentence.get("index"))
            current["text"] = f"{current['text']} {sentence['text']}"
            current["word_count"] = int(current["word_count"]) + words
            current["ai_filters"].append(sentence.get("ai_filters") or {})
    return chunks
