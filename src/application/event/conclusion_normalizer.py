from __future__ import annotations

from typing import Any


def selected_option_indexes(value: Any, *, upper_bound: int) -> list[int]:
    selected: list[int] = []
    if isinstance(value, int):
        value = [value]
    elif isinstance(value, str):
        value = [value]
    elif isinstance(value, dict):
        value = value.values()
    for raw in value or []:
        try:
            idx = int(raw)
        except (TypeError, ValueError):
            continue
        if 0 <= idx < upper_bound and idx not in selected:
            selected.append(idx)
    return selected


def topic_chunks_by_indexes(topics: list[dict[str, Any]], indexes: list[int]) -> list[int]:
    return sorted({int(idx) for topic_idx in indexes for idx in (topics[topic_idx].get("chunk_indexes") or []) if str(idx).isdigit()})


def chunks_by_index(chunks: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    mapping: dict[int, dict[str, Any]] = {}
    for chunk in chunks:
        raw_index = chunk.get("chunk_index")
        if raw_index is not None and str(raw_index).isdigit():
            mapping[int(str(raw_index))] = chunk
    return mapping


def infer_suggested_owner(task: dict[str, Any], event: dict[str, Any]) -> str | None:
    text = " ".join(str(value or "") for value in [task.get("title"), task.get("description"), task.get("original_quote"), event.get("details")])
    entities = [str(entity).strip() for entity in (event.get("entities") or []) if str(entity).strip()]
    blacklist = {"ukraine", "poland", "france", "four reasons usa", "$3,500"}
    for entity in entities:
        normalized = entity.lower()
        if normalized in blacklist or any(char.isdigit() for char in entity):
            continue
        if entity in text or len(entity.split()) >= 2:
            return entity
    return None


def normalize_open_issue(item: Any, topics: list[dict[str, Any]], default_topic_indexes: list[int]) -> dict[str, Any]:
    if isinstance(item, str):
        return {"text": item, "source_topic_indexes": default_topic_indexes, "source_topic_titles": [topics[idx].get("title", "") for idx in default_topic_indexes if topics[idx].get("title")], "source_chunk_indexes": []}
    if isinstance(item, dict):
        topic_indexes = selected_option_indexes(item.get("source_topic_indexes"), upper_bound=len(topics)) or default_topic_indexes
        return {
            "text": str(item.get("text") or item.get("title") or "").strip(),
            "source_topic_indexes": topic_indexes,
            "source_topic_titles": [topics[idx].get("title", "") for idx in topic_indexes if topics[idx].get("title")],
            "source_chunk_indexes": [int(idx) for idx in (item.get("source_chunk_indexes") or []) if str(idx).isdigit()],
        }
    return {"text": str(item).strip(), "source_topic_indexes": default_topic_indexes, "source_topic_titles": [topics[idx].get("title", "") for idx in default_topic_indexes if topics[idx].get("title")], "source_chunk_indexes": []}


def group_label(task: dict[str, Any]) -> str:
    return str(task.get("owner_ref") or task.get("owner_person_name") or task.get("suggested_owner") or "Unassigned").strip() or "Unassigned"


def normalize_task(task: dict[str, Any], topics: list[dict[str, Any]], *, default_topic_indexes: list[int], allowed_chunks: set[int]) -> dict[str, Any]:
    task_topic_indexes = selected_option_indexes(task.get("source_topic_indexes"), upper_bound=len(topics)) or default_topic_indexes
    task["source_topic_indexes"] = task_topic_indexes
    task["source_topic_titles"] = [topics[idx].get("title", "") for idx in task_topic_indexes if topics[idx].get("title")]
    task_topic_chunks = set(topic_chunks_by_indexes(topics, task_topic_indexes)) if task_topic_indexes else allowed_chunks
    task_chunks = {idx for idx in task.get("source_chunk_indexes") or [] if idx in allowed_chunks and idx in task_topic_chunks}
    task["source_chunk_indexes"] = sorted(task_chunks) or sorted(task_topic_chunks)
    task["context"] = str(task.get("context") or "").strip()
    task["action"] = str(task.get("action") or "").strip()
    if not task.get("action"):
        task["action"] = str(task.get("title") or task.get("description") or "").strip()
    if not task.get("title"):
        task["title"] = task["action"] or task["context"] or str(task.get("description") or "").strip()
    if not task.get("description"):
        task["description"] = task["context"] or task["action"]
    task["owner_ref"] = str(task.get("owner_ref") or "").strip() or None
    task["unknown_owner_text"] = str(task.get("unknown_owner_text") or "").strip() or None
    if not task.get("owner_person_name") and task.get("suggested_owner"):
        task["owner_person_name"] = task.get("suggested_owner")
    if task.get("owner_person_name") and not task.get("suggested_owner"):
        task["suggested_owner"] = task.get("owner_person_name")
    task["priority"] = str(task.get("priority") or "medium").lower()
    if task["priority"] not in {"high", "medium", "low"}:
        task["priority"] = "medium"
    task["category"] = str(task.get("category") or "general").lower()
    task["status"] = str(task.get("status") or "pending").lower()
    return task


def normalize_people_tasks(conclusion: dict[str, Any], topics: list[dict[str, Any]], *, default_topic_indexes: list[int], allowed_chunks: set[int], normalize_task_fn=normalize_task) -> list[dict[str, Any]]:
    raw_groups = conclusion.get("people_tasks") or []
    if not raw_groups:
        raw_groups = []
        for event in conclusion.get("events") or []:
            for task in event.get("tasks") or []:
                raw_groups.append(
                    {
                        "person_name": task.get("owner_person_name"),
                        "suggested_owner": task.get("suggested_owner"),
                        "assignment_reason": task.get("description") or task.get("context") or event.get("summary") or "",
                        "tasks": [task],
                    }
                )
    normalized_groups: list[dict[str, Any]] = []
    for group in raw_groups:
        person_name = str(group.get("person_name") or "").strip() or None
        owner_ref = str(group.get("owner_ref") or "").strip() or None
        unknown_owner_text = str(group.get("unknown_owner_text") or "").strip() or None
        suggested_owner = str(group.get("suggested_owner") or "").strip() or None
        tasks = [normalize_task_fn(task, topics, default_topic_indexes=default_topic_indexes, allowed_chunks=allowed_chunks) for task in (group.get("tasks") or [])]
        if not owner_ref and tasks:
            owner_ref = next((task.get("owner_ref") for task in tasks if task.get("owner_ref")), None)
        if not unknown_owner_text and tasks:
            unknown_owner_text = next((task.get("unknown_owner_text") for task in tasks if task.get("unknown_owner_text")), None)
        if not person_name and tasks:
            person_name = next((task.get("owner_person_name") for task in tasks if task.get("owner_person_name")), None)
        if not suggested_owner and tasks:
            suggested_owner = next((task.get("suggested_owner") for task in tasks if task.get("suggested_owner")), None)
        if not suggested_owner:
            suggested_owner = next((owner for owner in (task.get("owner_person_name") for task in tasks) if owner), None)
        if not person_name and suggested_owner:
            person_name = suggested_owner
        if not tasks:
            continue
        normalized_groups.append(
            {
                "person_name": person_name,
                "owner_ref": owner_ref,
                "unknown_owner_text": unknown_owner_text,
                "suggested_owner": suggested_owner,
                "assignment_reason": str(group.get("assignment_reason") or "").strip(),
                "tasks": tasks,
            }
        )
    if not normalized_groups:
        grouped: dict[str, dict[str, Any]] = {}
        for event in conclusion.get("events") or []:
            for task in event.get("tasks") or []:
                normalized_task = normalize_task_fn(task, topics, default_topic_indexes=default_topic_indexes, allowed_chunks=allowed_chunks)
                label = group_label(normalized_task)
                group = grouped.setdefault(
                    label,
                    {"person_name": None if label == "Unassigned" else label, "suggested_owner": None if label == "Unassigned" else label, "assignment_reason": event.get("summary") or "", "tasks": []},
                )
                group["tasks"].append(normalized_task)
        normalized_groups = list(grouped.values())
    return normalized_groups


def normalize_event(event: dict[str, Any], topics: list[dict[str, Any]], *, default_topic_indexes: list[int] | None = None, allowed_chunk_indexes: set[int] | None = None) -> dict[str, Any]:
    allowed_chunks = set(allowed_chunk_indexes or [int(idx) for topic in topics for idx in (topic.get("chunk_indexes") or []) if str(idx).isdigit()])
    event_topic_indexes = selected_option_indexes(event.get("source_topic_indexes"), upper_bound=len(topics)) or (default_topic_indexes or list(range(len(topics))))
    event["source_topic_indexes"] = event_topic_indexes
    event["source_topic_titles"] = [topics[idx].get("title", "") for idx in event_topic_indexes if topics[idx].get("title")]
    event_topic_chunks = set(topic_chunks_by_indexes(topics, event_topic_indexes))
    event_chunks = {idx for idx in event.get("source_chunk_indexes") or [] if idx in allowed_chunks and idx in event_topic_chunks}
    event["source_chunk_indexes"] = sorted(event_chunks) or sorted(event_topic_chunks or allowed_chunks)
    for decision in event.get("decisions") or []:
        decision_topic_indexes = selected_option_indexes(decision.get("relevant_topic_indexes"), upper_bound=len(topics)) or event_topic_indexes
        decision["relevant_topic_indexes"] = decision_topic_indexes
        decision["relevant_topics"] = [topics[idx].get("title", "") for idx in decision_topic_indexes if topics[idx].get("title")]
    event["tasks"] = [normalize_task(task, topics, default_topic_indexes=event_topic_indexes, allowed_chunks=allowed_chunks) for task in (event.get("tasks") or [])]
    for task in event["tasks"]:
        if not task.get("suggested_owner") and not task.get("owner_person_name"):
            task["suggested_owner"] = infer_suggested_owner(task, event)
    event["open_issues"] = [normalize_open_issue(item, topics, event_topic_indexes) for item in (event.get("open_issues") or [])]
    event["sentiment"] = str(event.get("sentiment") or "neutral").lower()
    return event


def normalize_conclusion(conclusion: dict[str, Any], topics: list[dict[str, Any]], *, allowed_chunk_indexes: set[int] | None = None, fact_layer: dict[str, Any] | None = None) -> dict[str, Any]:
    allowed_chunks = set(allowed_chunk_indexes or [int(idx) for topic in topics for idx in (topic.get("chunk_indexes") or []) if str(idx).isdigit()])
    raw_events = conclusion.get("events") or []
    if not raw_events and topics:
        raw_events = [{"title": conclusion.get("title", "Untitled event"), "summary": conclusion.get("summary", ""), "source_topic_indexes": list(range(len(topics)))}]
    events = [normalize_event(event, topics, allowed_chunk_indexes=allowed_chunks) for event in raw_events]
    conclusion["events"] = events
    if fact_layer is not None:
        conclusion["fact_layer"] = fact_layer
    conclusion["one_sentence_summary"] = conclusion.get("one_sentence_summary") or conclusion.get("summary", "")[:240]
    raw_tl_dr = conclusion.get("tl_dr") or [event.get("summary", "") for event in events if event.get("summary")]
    conclusion["tl_dr"] = [str(item).strip() for item in raw_tl_dr if str(item).strip()][:5]
    conclusion["people_tasks"] = normalize_people_tasks(conclusion, topics, default_topic_indexes=list(range(len(topics))), allowed_chunks=allowed_chunks)
    event_topic_indexes = sorted({idx for event in events for idx in (event.get("source_topic_indexes") or [])})
    selected_topic_indexes = selected_option_indexes(conclusion.get("source_topic_indexes"), upper_bound=len(topics)) or event_topic_indexes or list(range(len(topics)))
    conclusion["source_topic_indexes"] = selected_topic_indexes
    conclusion["source_topic_titles"] = [topics[idx].get("title", "") for idx in selected_topic_indexes if topics[idx].get("title")]
    event_chunks = {idx for event in events for idx in (event.get("source_chunk_indexes") or []) if idx in allowed_chunks}
    selected_chunks = {idx for idx in conclusion.get("source_chunk_indexes") or [] if idx in allowed_chunks}
    conclusion["source_chunk_indexes"] = sorted(selected_chunks or event_chunks or allowed_chunks)
    return conclusion
