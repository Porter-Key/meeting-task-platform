from __future__ import annotations

from django.db import models


class ApplicationLog(models.Model):
    id = models.CharField(max_length=120, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20, default="info")
    logger_name = models.CharField(max_length=160, default="application")
    stage = models.CharField(max_length=120, default="")
    event = models.CharField(max_length=160, default="")
    message = models.TextField(default="")
    correlation_id = models.CharField(max_length=160, null=True, blank=True)
    meeting_id = models.CharField(max_length=120, null=True, blank=True)
    payload = models.JSONField(default=dict)

    class Meta:
        managed = False
        db_table = "application_logs"
