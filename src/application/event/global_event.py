from __future__ import annotations

from typing import Any


class GlobalEventService:
    def __init__(self, event_repo: Any, event_context_repo: Any, event_graph_repo: Any, event_vector_repo: Any) -> None:
        self.event_repo = event_repo
        self.event_context_repo = event_context_repo
        self.event_graph_repo = event_graph_repo
        self.event_vector_repo = event_vector_repo

    def merge_meeting_events(self, meeting: dict[str, Any], meeting_events: list[dict[str, Any]]) -> dict[str, int]:
        created = 0
        updated = 0
        for item in meeting_events:
            candidates = self.event_context_repo.recall_global_event_candidates(item)
            target = candidates[0] if candidates else None
            event_id = self.event_repo.event_id_from_candidate(target)
            is_new_event = target is None
            event = {
                "id": event_id,
                "title": (target or {}).get("title") or item.get("title") or "Untitled event",
                "description": (target or {}).get("description") or item.get("description") or item.get("background") or "",
                "status": (target or {}).get("status") or item.get("status") or "open",
                "owner_person_name": (target or {}).get("owner_person_name") or item.get("owner_person_name"),
                "vector_text": (target or {}).get("vector_text") or item.get("vector_text") or item.get("description") or item.get("title") or "",
                "qdrant_collection": self.event_vector_repo.collection_name,
                "qdrant_point_id": self.event_vector_repo.point_id(event_id),
            }
            metadata = {
                "meeting_id": meeting["id"],
                "meeting_title": meeting.get("title") or "",
                "meeting_event_id": item["local_event_id"],
                "background": item.get("background") or "",
                "actions": item.get("actions") or [],
                "owner_person_name": item.get("owner_person_name"),
                "latest_progress": item.get("latest_progress") or "",
                "status": item.get("status") or "open",
                "topic_ids": item.get("topic_ids") or [],
                "local_topic_titles": item.get("local_topic_titles") or [],
                "chunk_indexes": item.get("chunk_indexes") or [],
            }
            self.event_repo.upsert_event_with_meeting_metadata(event, metadata)
            self.event_graph_repo.upsert_event({**event, "meeting_metadata": [metadata]})
            self.event_graph_repo.link_meeting_event_to_event(metadata["meeting_event_id"], event_id, created=is_new_event)
            if is_new_event:
                self.event_vector_repo.upsert_event(event, item.get("vector") or [])
            if target:
                updated += 1
            else:
                created += 1
        return {"created_events": created, "updated_events": updated}
