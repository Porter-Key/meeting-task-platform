from __future__ import annotations

from django.db import models

from .base import ExistingTableModel
from .meeting import Meeting


class Event(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    title = models.TextField(default="")
    description = models.TextField(default="")
    status = models.CharField(max_length=40, default="open")
    due_hint = models.TextField(null=True, blank=True)
    vector_text = models.TextField(default="")
    qdrant_collection = models.CharField(max_length=120, null=True, blank=True)
    qdrant_point_id = models.CharField(max_length=120, null=True, blank=True)
    state_changes = models.JSONField(default=list)
    relation_edges = models.JSONField(default=list)

    class Meta(ExistingTableModel.Meta):
        db_table = "events"


class EventMeetingMetadata(ExistingTableModel):
    id = models.CharField(max_length=160, primary_key=True)
    event = models.ForeignKey(Event, db_column="event_id", on_delete=models.CASCADE, related_name="meeting_metadata")
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="event_metadata")
    meeting_title = models.TextField(default="")
    background = models.TextField(default="")
    actions = models.JSONField(default=list)
    latest_progress = models.TextField(default="")
    status = models.CharField(max_length=40, default="open")
    topic_ids = models.JSONField(default=list)
    local_topic_titles = models.JSONField(default=list)
    chunk_indexes = models.JSONField(default=list)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "event_meeting_metadata"
