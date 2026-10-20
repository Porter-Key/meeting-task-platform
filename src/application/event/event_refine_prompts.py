from __future__ import annotations

import json
from typing import Any

from .fact_layer import render_fact_layer
from .prompt_utils import compact


def event_refine_prompt(
    meeting: dict[str, Any],
    event: dict[str, Any],
    event_topics: list[dict[str, Any]],
    event_chunks: list[dict[str, Any]],
    conclusion: dict[str, Any],
    event_index: int,
    fact_layer: dict[str, Any] | None = None,
) -> str:
    topic_lines = []
    source_topic_indexes = event.get("source_topic_indexes") or []
    for idx, topic in enumerate(event_topics):
        source_idx = source_topic_indexes[idx] if idx < len(source_topic_indexes) else idx
        topic_lines.append(f"[{source_idx}] title={topic.get('title')} | chunks={topic.get('chunk_indexes') or []} | summary={compact(topic.get('summary'), 600)}")
    chunk_lines = [f"[{c['chunk_index']}] {c.get('speaker')} {c.get('start_time')}-{c.get('end_time')}: {c.get('text') or ''}" for c in event_chunks]
    return f"""
Role
You are a professional business analyst and senior executive secretary. You are skilled at turning messy meeting dialogue into logically structured, factually accurate event records with traceable evidence.

Task
Refine and correct the current focused meeting event using the provided fact layer and original recalled chunks.

Specific Guidelines
1. Summary: Use one sentence to capture the core essence of this event: what happened and what the result was.
2. Details:
   - Must follow a logical sequence.
   - Include key arguments, supporting numbers, and any disagreement between participants, if present.
   - Never remove key proper nouns, timestamps, or concrete numbers that appear in the source record.
3. Decisions:
   - Only record conclusions that were actually agreed upon.
   - Must be deterministic, such as "decided to adopt option A" or "approved the budget".
   - If something is only a proposal, put it in Details or Open Issues.
4. Open Issues:
   - Record all unresolved questions, items requiring follow-up research, or topics left open for the next meeting.
5. Sentiment:
   - Assess the tone of the discussion. Options: collaborative, heated, hesitant, neutral.
6. Fact Layer First:
   - The fact layer is the highest authority.
   - If the original chunks conflict with the fact layer, follow the fact layer.
   - Never invent a deadline, amount, or owner that was not stated.

Constraints
- Keep the tasks array empty.
- Do not generate a people_tasks layer.
- Output must be strict JSON only, with no Markdown fences or explanation text.

Context
- Current conclusion: {json.dumps(conclusion, ensure_ascii=False, indent=2)}
- Focused event: {json.dumps(event, ensure_ascii=False, indent=2)}
- Event source Topics: {chr(10).join(topic_lines)}
- Event recalled chunks: {chr(10).join(chunk_lines)}
- Fact layer preview: {render_fact_layer(fact_layer or {}, max_facts=12)}

Output Schema
{{"title":"...","summary":"...","details":"...","decisions":[{{"text":"...","relevant_topic_indexes":[]}}],"tasks":[],"open_issues":[{{"text":"...","source_topic_indexes":[],"source_chunk_indexes":[]}}],"sentiment":"...","source_topic_indexes":[],"source_chunk_indexes":[],"keywords":[],"entities":[],"confidence":0.0}}
""".strip()
