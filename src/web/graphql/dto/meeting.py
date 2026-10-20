from __future__ import annotations

from rest_framework import serializers

from domain.models.meeting import Meeting, MeetingPipelineRun


class MeetingDTO(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"


class MeetingPipelineRunDTO(serializers.ModelSerializer):
    class Meta:
        model = MeetingPipelineRun
        fields = "__all__"
