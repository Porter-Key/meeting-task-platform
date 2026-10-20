from __future__ import annotations

from rest_framework import serializers

from domain.models.task_masterlist import TaskAssigneeLink, TaskExternalLink, TaskMasterlist


class TaskMasterlistDTO(serializers.ModelSerializer):
    class Meta:
        model = TaskMasterlist
        fields = "__all__"


class TaskAssigneeLinkDTO(serializers.ModelSerializer):
    email = serializers.CharField(source="email_id", allow_null=True)
    alias = serializers.CharField(source="alias_id", allow_null=True)

    class Meta:
        model = TaskAssigneeLink
        fields = "__all__"


class TaskExternalLinkDTO(serializers.ModelSerializer):
    class Meta:
        model = TaskExternalLink
        fields = "__all__"
