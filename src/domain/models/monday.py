from __future__ import annotations

from django.db import models

from .base import ExistingTableModel
from .people import Person
from .task_masterlist import TaskMasterlist


class MondayUser(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    monday_user_id = models.CharField(max_length=120, unique=True)
    name = models.TextField(default="")
    email = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(null=True, blank=True)
    is_admin = models.BooleanField(null=True, blank=True)
    is_guest = models.BooleanField(null=True, blank=True)
    is_pending = models.BooleanField(null=True, blank=True)
    is_view_only = models.BooleanField(null=True, blank=True)
    raw_payload = models.JSONField(default=dict)
    synced_at = models.DateTimeField(null=True, blank=True)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_users"


class MondayTeam(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    monday_team_id = models.CharField(max_length=120, unique=True)
    name = models.TextField(default="")
    raw_payload = models.JSONField(default=dict)
    synced_at = models.DateTimeField(null=True, blank=True)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_teams"


class MondayBoard(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    monday_board_id = models.CharField(max_length=120, unique=True)
    name = models.TextField(default="")
    workspace_id = models.CharField(max_length=120, null=True, blank=True)
    workspace_name = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=80, null=True, blank=True)
    board_kind = models.CharField(max_length=80, null=True, blank=True)
    raw_payload = models.JSONField(default=dict)
    synced_at = models.DateTimeField(null=True, blank=True)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_boards"


class MondayGroup(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    monday_board_id = models.CharField(max_length=120)
    monday_group_id = models.CharField(max_length=160)
    title = models.TextField(default="")
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    raw_payload = models.JSONField(default=dict)
    synced_at = models.DateTimeField(null=True, blank=True)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_groups"


class MondayColumn(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    monday_board_id = models.CharField(max_length=120)
    monday_column_id = models.CharField(max_length=160)
    title = models.TextField(default="")
    type = models.CharField(max_length=80, null=True, blank=True)
    settings_str = models.TextField(null=True, blank=True)
    field_key = models.CharField(max_length=160, null=True, blank=True)
    required = models.BooleanField(default=False)
    options = models.JSONField(default=list)
    schema_payload = models.JSONField(default=dict)
    raw_payload = models.JSONField(default=dict)
    synced_at = models.DateTimeField(null=True, blank=True)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_columns"


class MondayIdentityCandidate(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    person_email = models.ForeignKey(Person, db_column="person_email", to_field="email", on_delete=models.CASCADE)
    monday_user_id = models.CharField(max_length=120)
    match_status = models.CharField(max_length=40, default="suggested")
    confidence = models.FloatField(default=0.0)
    reason = models.TextField(default="")
    evidence_payload = models.JSONField(default=dict)
    llm_payload = models.JSONField(default=dict)
    reviewed_by = models.TextField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_identity_candidates"


class MondayUserMapping(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    person_email = models.ForeignKey(Person, db_column="person_email", to_field="email", on_delete=models.CASCADE)
    monday_user_id = models.CharField(max_length=120)
    source = models.CharField(max_length=80)
    confidence = models.FloatField(default=1.0)
    verified = models.BooleanField(default=False)
    verified_by = models.TextField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_user_mappings"


class MondayTaskLink(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    masterlist_task = models.ForeignKey(TaskMasterlist, db_column="masterlist_task_id", on_delete=models.CASCADE, related_name="monday_links")
    monday_board_id = models.CharField(max_length=160)
    monday_group_id = models.CharField(max_length=160, null=True, blank=True)
    monday_item_id = models.CharField(max_length=160)
    monday_item_url = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=40, default="active")
    last_pushed_at = models.DateTimeField(null=True, blank=True)
    last_push_run_id = models.CharField(max_length=120, null=True, blank=True)
    last_error = models.TextField(null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_task_links"


class MondayPushRun(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    requested_by = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=40, default="running")
    total_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    skipped_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_push_runs"


class MondayPushRunItem(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    run = models.ForeignKey(MondayPushRun, db_column="run_id", on_delete=models.CASCADE, related_name="items")
    masterlist_task = models.ForeignKey(TaskMasterlist, db_column="masterlist_task_id", on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    monday_item_id = models.CharField(max_length=160, null=True, blank=True)
    warnings = models.JSONField(default=list)
    error = models.TextField(null=True, blank=True)
    request_payload = models.JSONField(default=dict)
    response_payload = models.JSONField(default=dict)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "monday_push_run_items"
