from __future__ import annotations

import json
from typing import Any

from .fact_layer import render_fact_layer


def people_tasks_prompt(meeting: dict[str, Any], conclusion: dict[str, Any], fact_layer: dict[str, Any] | None = None) -> str:
    return f"""
Role
You are a senior project management expert (PMP). You excel at converting meeting discussion into actionable items that can be directly assigned and executed.

Task
From the refined meeting conclusion, extract every explicit or implied task and attach it to the most likely responsible person.

Task Definition Guidelines
1. Atomic Action: The task title must begin with a verb + object (for example, "write technical documentation" instead of "documentation related"). Each task can contain only one independent action.
2. Dispatchable: The task must be assignable. If the discussion is too vague, skip it. If the discussion is specific, record it.
3. Ownership Logic:
   - Choose task owners only from PEOPLE_CANDIDATES by owner_ref when candidates are present in the fact layer.
   - Do not output an email as owner and do not invent people or emails.
   - If no candidate fits, set owner_ref=null and unknown_owner_text to the exact phrase from the transcript.
   - You may still fill person_name/suggested_owner for readability, but owner_ref is the assignment contract.
4. Context & Action:
   - Context: briefly explain why this task exists.
   - Action: describe the concrete next step.

Operational Rules
- Do not regenerate Event or TL;DR content.
- Only generate the people_tasks object.
- If a task has no clear action, skip it rather than guessing.
- Priority: use high if the task is described as urgent / immediate / must-do; otherwise use medium.
- Never invent owner emails. Use owner_ref only.

Input Data
- Fact layer preview: {render_fact_layer(fact_layer or {}, max_facts=12)}
- Refined conclusion: {json.dumps(conclusion, ensure_ascii=False, indent=2)}
- Meeting: {meeting.get('title')} ({meeting.get('id')})

Output Schema
{{
  "people_tasks": [
    {{
      "person_name": "specific executor name",
      "owner_ref": "P1 or null",
      "unknown_owner_text": "exact unresolved owner phrase or null",
      "suggested_owner": "suggested role if name is unclear",
      "assignment_reason": "why this person is the owner",
      "tasks": [
        {{
          "title": "short task title",
          "context": "task background",
          "action": "specific execution step",
          "owner_person_name": "same as above",
          "owner_ref": "same owner_ref as group or null",
          "unknown_owner_text": "same unknown owner phrase or null",
          "suggested_owner": "same as above",
          "priority": "high/medium/low",
          "category": "general/technical/admin/etc",
          "status": "pending",
          "due_date": "YYYY-MM-DD if mentioned",
          "original_quote": "supporting source quote",
          "source_topic_indexes": [],
          "source_chunk_indexes": []
        }}
      ]
    }}
  ]
}}
""".strip()
