from __future__ import annotations

from typing import Any

from .fact_layer import render_fact_layer
from .prompt_utils import compact


def event_grouping_prompt(meeting: dict[str, Any], topics: list[dict[str, Any]], fact_layer: dict[str, Any] | None = None) -> str:
    lines = []
    for idx, topic in enumerate(topics):
        lines.append(
            f"[{idx}] title={topic.get('title') or ''} | chunks={topic.get('chunk_indexes') or []}\n"
            f"summary={compact(topic.get('summary'), 420)}\n"
            f"keywords={topic.get('keywords') or []} | entities={topic.get('entities') or []}"
        )
    return f"""
Group these Topics into 3-4 event groups before event drafting.

Think like a semantic clustering step, similar to HDBSCAN:
- First identify dense centers of meaning across all Topics.
- A group should represent one stable workstream, not one narrow detail.
- Topics belong together when they share the same business object, goal, decision chain, owner/context, system/tool, evidence window, or executable action path.
- Keep related sub-aspects together: status, constraints, decisions, risks/open issues, metrics, and next actions of the same workstream.
- Preserve boundaries between separate workstreams. Do not merge just because Topics share generic words like dashboard, data, tool, project, issue, campaign, task, price, or report.
- Split only when the objective changes, the responsible context changes, the system/tool changes, the cost/strategy decision changes, or the next action path would be executed independently.
- Off-topic or weakly related discussion may be grouped as a low-priority context group, but do not let it split core business workstreams.
- Prefer 3 groups. Use 4 only when there is a clearly independent workstream that would be distorted by merging.

Return only topic indexes. Do not return IDs, titles, or chunk indexes in selection fields.
Every important business Topic should appear in exactly one group. Low-value/off-topic Topics may be omitted if they are not event-worthy.

Fact layer preview:
{render_fact_layer(fact_layer or {}, max_facts=8)}

Return JSON: {{"groups":[{{"title":"short workstream label","rationale":"why these topics belong together and where the boundary is","topic_indexes":[]}}]}}

Meeting: {meeting.get('title')} ({meeting.get('id')})
Topics:
{chr(10).join(lines)}
""".strip()


def event_draft_prompt(
    meeting: dict[str, Any],
    topics: list[dict[str, Any]],
    topic_indexes: list[int],
    fact_layer: dict[str, Any] | None = None,
) -> str:
    lines = []
    for idx in topic_indexes:
        topic = topics[idx]
        lines.append(
            f"[{idx}] title={topic.get('title') or ''} | chunks={topic.get('chunk_indexes') or []} | "
            f"summary={compact(topic.get('summary'), 450)} | keywords={topic.get('keywords') or []} | entities={topic.get('entities') or []}"
        )
    return f"""
Generate exactly one event for this topic group.

Use Topics + the fact layer only.
Do not generate tl_dr.
Do not generate people_tasks.
Do not generate multiple events.
Keep this event faithful to the whole group, not just the strongest sentence.
Use concrete business language; do not over-abstract.
Do not invent dates, owners, metrics, amounts, or deadlines that are not present in the fact layer or topics.

The group topics are the only allowed evidence for this event:
{topic_indexes}

Grouping rule:
- Treat a group as one dense cluster of related topics, similar to how HDBSCAN forms a cluster from nearby points.
- Topics belong in the same event only when they share the same business object, goal, decision chain, owner context, system, or action path.
- Keep related sub-aspects together when they are evidence for the same workstream: status, constraints, decisions, open issues, metrics, and next actions.
- Preserve boundaries between separate workstreams. Do not collapse topics together just because they share generic words like dashboard, data, tool, customer, project, issue, or task.
- Split conceptually when the objective changes, the responsible person/context changes, the system/tool changes, the cost/strategic decision changes, or the action path would be executed independently.
- If one topic is side discussion or weakly related, do not let it dominate the event. Either summarize it as context or leave it out of the event meaning.
- Write the event around the cluster center: what this group is mainly about, why these topics belong together, and what boundary separates it from nearby groups.

Fact layer preview:
{render_fact_layer(fact_layer or {}, max_facts=10)}

Return JSON: {{"title":"...","summary":"...","details":"...","decisions":[{{"text":"...","relevant_topic_indexes":[]}}],"tasks":[],"open_issues":[{{"text":"...","source_topic_indexes":[],"source_chunk_indexes":[]}}],"sentiment":"collaborative","source_topic_indexes":[],"source_chunk_indexes":[],"keywords":[],"entities":[],"confidence":0.0}}

Meeting: {meeting.get('title')} ({meeting.get('id')})
Topic group:
{chr(10).join(lines)}
""".strip()
