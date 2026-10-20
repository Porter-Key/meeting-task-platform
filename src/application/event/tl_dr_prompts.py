from __future__ import annotations

import json
from typing import Any

from .fact_layer import render_fact_layer


def tl_dr_prompt(meeting: dict[str, Any], conclusion: dict[str, Any], fact_layer: dict[str, Any] | None = None) -> str:
    return f"""
Generate the final tl_dr from the refined events and people tasks.

Do not generate events.
Do not generate tasks.
Return up to 5 bullets covering the most important meeting workstreams.
Each bullet must be short and cover only one workstream.
Coverage is more important than compression.

Fact layer preview:
{render_fact_layer(fact_layer or {}, max_facts=10)}

Refined conclusion:
{json.dumps(conclusion, ensure_ascii=False, indent=2)}

Return JSON: {{"one_sentence_summary":"...","tl_dr":["..."],"summary":"..."}}

Meeting: {meeting.get('title')} ({meeting.get('id')})
""".strip()
