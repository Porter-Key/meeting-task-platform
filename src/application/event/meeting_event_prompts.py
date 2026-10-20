from __future__ import annotations

from typing import Any

from .fact_layer import render_fact_layer
from .prompt_utils import compact


def meeting_event_prompt(meeting: dict[str, Any], topic_group: list[dict[str, Any]], fact_layer: dict[str, Any] | None = None) -> str:
    lines = []
    for idx, topic in enumerate(topic_group):
        lines.append(f"[{idx}] title={topic.get('title')} | chunks={topic.get('chunk_indexes') or []} | {compact(topic.get('summary'), 300)} | keywords={topic.get('keywords') or []}")
    return f"""
Generate one or more MeetingEvents from these Topics.

MeetingEvent is a meeting-level event dossier derived only from Topics.
Do not use mentions. Do not expand raw chunk evidence.
Do not create or return any ids. The application generates all ids as UUIDs.
MeetingEvent should represent a readable transaction/workstream center, not just a narrow topic label.
Different aspects of the same workstream may belong in one MeetingEvent.
Use a natural business title that explains the workstream, for example "Video production project setup and delivery plan".
Avoid titles that are too narrow, awkward, or only name one facet when the Topics form a broader workstream.
Description should summarize what is happening, why it matters, and what dimensions are involved.
Background should capture context. latest_progress should say what changed or became clear in this meeting.
Choose source topics by index only.
For each MeetingEvent, set source_topic_indexes to the exact source Topic option numbers used by that event only.
Do not include titles in any selection field.
Leave chunk_indexes empty; the application derives chunk evidence from source_topic_indexes.
Fill business_object, business_process, platform_or_system, decision_or_action, current_state, why_it_matters, and exclusion_boundary with concrete details for semantic-map quality.
exclusion_boundary should describe what nearby similar-looking workstream this event should not be confused with; it is a guardrail, not the description.
Use the fact layer as the source of truth for dates, times, numbers, names, and other objective data; never invent or correct a fact that is not supported.

Fact layer preview:
{render_fact_layer(fact_layer or {}, max_facts=8)}

Return JSON: {{"meeting_events": [{{"title":"...","description":"...","background":"...","actions":[],"owner_person_name":null,"latest_progress":"...","status":"open","source_topic_indexes":[],"chunk_indexes":[],"keywords":[],"entities":[],"confidence":0.0,"business_object":"...","business_process":"...","platform_or_system":"...","decision_or_action":"...","current_state":"...","why_it_matters":"...","exclusion_boundary":"..."}}]}}

Meeting: {meeting.get('title')} ({meeting.get('id')})
Topics:
{chr(10).join(lines)}
""".strip()
