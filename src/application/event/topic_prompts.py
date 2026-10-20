from __future__ import annotations

from typing import Any

from .fact_layer import render_fact_layer
from .prompt_utils import chunk_text_limit, compact


def topic_prompt(meeting: dict[str, Any], chunks: list[dict[str, Any]], fact_layer: dict[str, Any] | None = None) -> str:
    text_limit = chunk_text_limit(len(chunks))
    lines = [f"[{c['chunk_index']}] {c.get('speaker')} {c.get('start_time')}-{c.get('end_time')}: {compact(c.get('text'), text_limit)}" for c in chunks]
    return f"""
Generate exactly one Topic from this HDBSCAN batch of cleaned meeting chunks.

Topic is a discussion theme. Do not create Events. Do not create mentions.
Do not create or return any ids. The application generates all ids as UUIDs.
Review every provided chunk before deciding Topics.
The application owns chunk evidence from the HDBSCAN core seed plus temporally relevant recalled chunks; do not decide evidence scope.
You may leave chunk_indexes empty; if returned, they will be ignored by the application.
Each HDBSCAN batch must produce exactly one broad Topic that covers the whole batch.
Do not split the batch into multiple Topics even if it contains several aspects; merge them into one readable batch-level subject.

Write for a business operator who did not attend the meeting.
Use plain, concrete, readable titles. Avoid vague titles like "coordination", "discussion", "general update", or overly narrow transcript fragments.
Topic title should answer: "What was this whole HDBSCAN batch mainly about?"
Topic summary should be 1-2 clear sentences explaining the actual business meaning across the whole batch, not a transcript paraphrase.
Prefer terms like "sample product shipping for video production" over ambiguous wording like "Ukraine-related logistics".
Preserve concrete facts when present: prices, counts, deadlines, dates/weekdays, clip durations, people, locations, platforms, and product names.
Use the fact layer as the source of truth for dates, times, numbers, names, and other objective data; never invent or correct a fact that is not supported.

Fact layer preview:
{render_fact_layer(fact_layer or {}, max_facts=8)}

Return JSON: {{"topic": {{"title":"...","summary":"what the whole batch was about","keywords":[],"entities":[],"chunk_indexes":[],"confidence":0.0}}}}

Meeting: {meeting.get('title')} ({meeting.get('id')})
Chunks:
{chr(10).join(lines)}
""".strip()
