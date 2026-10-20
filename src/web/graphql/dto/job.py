from __future__ import annotations

from rest_framework import serializers

from domain.models.job import ApplicationJob
from domain.models.logs import ApplicationLog


class ApplicationJobDTO(serializers.ModelSerializer):
    class Meta:
        model = ApplicationJob
        fields = "__all__"


class ApplicationLogDTO(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLog
        fields = "__all__"
