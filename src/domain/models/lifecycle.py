from __future__ import annotations

from django.db import models

from .base import ExistingTableModel


class BeatSchedule(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    name = models.TextField(default="")
    task_name = models.CharField(max_length=160, default="")
    workflow_key = models.CharField(max_length=160, null=True, blank=True)
    workflow_type = models.CharField(max_length=40, default="canvas")
    payload = models.JSONField(default=dict)
    schedule_type = models.CharField(max_length=40, default="cron")
    cron = models.CharField(max_length=80, null=True, blank=True)
    interval_seconds = models.IntegerField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    metadata_payload = models.JSONField(default=dict)
    last_enqueued_at = models.DateTimeField(null=True, blank=True)
    last_job_id = models.CharField(max_length=120, null=True, blank=True)

    class Meta(ExistingTableModel.Meta):
        db_table = "beat_schedules"
