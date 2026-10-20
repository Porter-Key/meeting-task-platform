from __future__ import annotations

from django.db import models

from .base import ExistingTableModel
from .meeting import Meeting, MeetingConclusion
from .people import Person, PersonAlias


class TaskOrigin(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    origin_type = models.CharField(max_length=80)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, null=True, blank=True, related_name="task_origins")
    conclusion = models.ForeignKey(MeetingConclusion, db_column="conclusion_id", on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(default="")
    action = models.TextField(default="")
    context = models.TextField(default="")
    priority = models.CharField(max_length=40, default="medium")
    owner_ref = models.CharField(max_length=20, null=True, blank=True)
    owner_email = models.ForeignKey(Person, db_column="owner_email", to_field="email", on_delete=models.SET_NULL, null=True, blank=True)
    owner_alias = models.ForeignKey(PersonAlias, db_column="owner_alias_id", on_delete=models.SET_NULL, null=True, blank=True)
    unknown_owner_text = models.TextField(null=True, blank=True)
    assignment_reason = models.TextField(null=True, blank=True)
    source_topic_indexes = models.JSONField(default=list)
    source_chunk_indexes = models.JSONField(default=list)
    source_quote = models.TextField(null=True, blank=True)
    payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "task_origins"


class TaskMasterlist(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    task_date = models.DateField()
    title = models.TextField(default="")
    action = models.TextField(default="")
    context = models.TextField(default="")
    priority = models.CharField(max_length=40, default="medium")
    status = models.CharField(max_length=40, default="draft")
    origin = models.ForeignKey(TaskOrigin, db_column="origin_id", on_delete=models.SET_NULL, null=True, blank=True)
    origin_type = models.CharField(max_length=80)
    version = models.IntegerField(default=1)
    due_date = models.DateField(null=True, blank=True)
    due_note = models.TextField(null=True, blank=True)
    monday_board_id = models.CharField(max_length=160, null=True, blank=True)
    monday_board_name = models.TextField(null=True, blank=True)
    monday_group_id = models.CharField(max_length=160, null=True, blank=True)
    monday_group_title = models.TextField(null=True, blank=True)
    monday_schema_version = models.CharField(max_length=80, null=True, blank=True)
    monday_field_values = models.JSONField(default=dict)
    monday_target_set_by = models.TextField(null=True, blank=True)
    monday_target_set_at = models.DateTimeField(null=True, blank=True)
    monday_target_status = models.CharField(max_length=40, null=True, blank=True)
    monday_target_checked_at = models.DateTimeField(null=True, blank=True)
    monday_target_error = models.TextField(null=True, blank=True)
    saved_by = models.TextField(null=True, blank=True)
    saved_at = models.DateTimeField(null=True, blank=True)
    submitted_by = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "task_masterlist"


class TaskAssigneeLink(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    masterlist_task = models.ForeignKey(TaskMasterlist, db_column="masterlist_task_id", on_delete=models.CASCADE, related_name="assignees")
    email = models.ForeignKey(Person, db_column="email", to_field="email", on_delete=models.SET_NULL, null=True, blank=True)
    alias = models.ForeignKey(PersonAlias, db_column="alias_id", on_delete=models.SET_NULL, null=True, blank=True)
    relation = models.CharField(max_length=80)
    source = models.CharField(max_length=80)
    confidence = models.FloatField(default=1.0)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "task_assignee_links"


class TaskVersion(models.Model):
    id = models.CharField(max_length=120, primary_key=True)
    masterlist_task = models.ForeignKey(TaskMasterlist, db_column="masterlist_task_id", on_delete=models.CASCADE, related_name="versions")
    version = models.IntegerField()
    change_type = models.CharField(max_length=80)
    changed_by = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField()
    snapshot = models.JSONField(default=dict)
    patch = models.JSONField(default=dict)

    class Meta:
        managed = False
        db_table = "task_versions"


class TaskExternalLink(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    masterlist_task = models.ForeignKey(TaskMasterlist, db_column="masterlist_task_id", on_delete=models.CASCADE, related_name="external_links")
    external_system = models.CharField(max_length=80)
    external_item_id = models.CharField(max_length=160, null=True, blank=True)
    external_board_id = models.CharField(max_length=160, null=True, blank=True)
    external_url = models.TextField(null=True, blank=True)
    sync_status = models.CharField(max_length=40)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "task_external_links"
