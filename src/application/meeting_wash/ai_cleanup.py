from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from external_client.llm.structured import with_structured_output

from .schemas import AICleanChunkResult


DEFAULT_AI_CLEANUP_WORKERS = 64


def compact_text(value: Any, max_chars: int = 2500) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = "\n".join(f"- {item}" for item in value)
    text = str(value).strip()
    return text[:max_chars].strip()


def meeting_context(transcript: dict[str, Any]) -> str:
    summary = transcript.get("summary") or {}
    return f"""
Meeting context:
- title: {transcript.get('title')}
- keywords:
{compact_text(summary.get('keywords'), 800)}
- gist: {compact_text(summary.get('gist'), 800)}
- overview:
{compact_text(summary.get('overview'), 1800)}
- shorthand_bullet 精简版:
{compact_text(summary.get('shorthand_bullet'), 2200)}
""".strip()


class AICleanupService:
    """Cleanup-only transcript normalizer. It does not extract tasks, action items, topics, or events."""

    def __init__(self, chat_model: Any, *, max_workers: int = DEFAULT_AI_CLEANUP_WORKERS) -> None:
        self.cleaner = with_structured_output(chat_model, AICleanChunkResult, method="json_mode")
        self.max_workers = max_workers

    def clean_chunk(self, transcript: dict[str, Any], chunk: dict[str, Any]) -> dict[str, Any]:
        prompt = f"""
You clean meeting transcript chunks for a task-management system.

Rules:
- Preserve meaning. Do not invent facts.
- Fix obvious ASR errors only when context is strong.
- Keep domain terms exact: PPC, Buy Box, ASIN, BigQuery, Slack, Jungle Scout, Data Stream, MSRP.
- Remove filler/repetition only if it does not change meaning.
- Keep speaker, time range, and source sentence indexes.
- If uncertain, add the term or phrase to uncertain_terms.
- Do NOT extract tasks, action items, topics, or events. This step is transcript cleanup only.
- Use the meeting context only to resolve ambiguous terms. If context conflicts with the raw chunk, trust the raw chunk.

{meeting_context(transcript)}

Speaker: {chunk.get('speaker')}
Time: {chunk.get('start_time')} - {chunk.get('end_time')} seconds
Source sentence indexes: {chunk.get('sentence_indexes')}

Raw chunk:
{chunk.get('text') or chunk.get('raw_text') or ''}
""".strip()
        parsed = self.cleaner.invoke([
            (
                "system",
                "You are a precise transcript cleanup assistant. Return only valid JSON with keys "
                "clean_text, quality_notes, entities, and uncertain_terms. Do not extract tasks.",
            ),
            ("human", prompt),
        ])
        result = AICleanChunkResult.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()
        raw_text = chunk.get("text") or chunk.get("raw_text") or ""
        clean_text = result.get("clean_text") or raw_text
        return {
            **chunk,
            "raw_text": raw_text,
            "text": clean_text,
            "ai_filters": [
                *(chunk.get("ai_filters") or []),
                {
                    "stage": "ai_cleanup",
                    "raw_text": raw_text,
                    "clean_text": clean_text,
                    "quality_notes": result.get("quality_notes") or [],
                    "entities": result.get("entities") or [],
                    "uncertain_terms": result.get("uncertain_terms") or [],
                    "context_fields": ["title", "keywords", "gist", "overview", "shorthand_bullet"],
                },
            ],
        }

    def clean_chunks(self, transcript: dict[str, Any], chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        cleaned: list[dict[str, Any] | None] = [None] * len(chunks)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.clean_chunk, transcript, chunk): idx for idx, chunk in enumerate(chunks)}
            for future in as_completed(futures):
                idx = futures[future]
                chunk = chunks[idx]
                try:
                    cleaned[idx] = future.result()
                except Exception as exc:  # noqa: BLE001 - keep pipeline moving and preserve raw chunk.
                    cleaned[idx] = {
                        **chunk,
                        "raw_text": chunk.get("text") or chunk.get("raw_text") or "",
                        "ai_filters": [
                            *(chunk.get("ai_filters") or []),
                            {"stage": "ai_cleanup", "error": repr(exc), "raw_text": chunk.get("text") or chunk.get("raw_text") or ""},
                        ],
                    }
        return [item for item in cleaned if item is not None]
