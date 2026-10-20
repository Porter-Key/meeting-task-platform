from __future__ import annotations

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .base import ExistingTableModel


class ApplicationJob(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    queue_task_id = models.CharField(max_length=120, null=True, blank=True)
    command = models.CharField(max_length=120)
    status = models.CharField(max_length=40, default="queued")
    meeting_ids = ArrayField(models.TextField(), default=list, blank=True)
    payload = models.JSONField(default=dict)
    result = models.JSONField(default=dict)
    error = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta(ExistingTableModel.Meta):
        db_table = "application_jobs"
