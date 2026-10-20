from __future__ import annotations

from django.db import models

from .base import ExistingTableModel
from .job import ApplicationJob
from .people import Person, PersonAlias


class Meeting(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    title = models.TextField(default="")
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    timezone = models.CharField(max_length=80, null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meetings"


class MeetingSource(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="sources")
    provider = models.CharField(max_length=80)
    provider_record_id = models.CharField(max_length=160)
    provider_url = models.TextField(null=True, blank=True)
    raw_payload = models.JSONField(default=dict)
    sync_status = models.CharField(max_length=40, default="synced")
    synced_at = models.DateTimeField(null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meeting_sources"


class MeetingTranscript(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="transcripts")
    source = models.ForeignKey(MeetingSource, db_column="source_id", on_delete=models.SET_NULL, null=True, blank=True)
    format = models.CharField(max_length=80)
    content = models.TextField(null=True, blank=True)
    segments = models.JSONField(null=True, blank=True)
    language = models.CharField(max_length=40, null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meeting_transcripts"


class MeetingChunk(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="chunks")
    transcript = models.ForeignKey(MeetingTranscript, db_column="transcript_id", on_delete=models.SET_NULL, null=True, blank=True)
    chunk_index = models.IntegerField()
    speaker_alias = models.ForeignKey(PersonAlias, db_column="speaker_alias_id", on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(default="")
    start_ms = models.IntegerField(null=True, blank=True)
    end_ms = models.IntegerField(null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meeting_chunks"


class MeetingPersonLink(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="person_links")
    email = models.ForeignKey(Person, db_column="email", to_field="email", on_delete=models.SET_NULL, null=True, blank=True)
    alias = models.ForeignKey(PersonAlias, db_column="alias_id", on_delete=models.SET_NULL, null=True, blank=True)
    relation = models.CharField(max_length=80)
    source = models.CharField(max_length=80)
    confidence = models.FloatField(default=1.0)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meeting_person_links"


class MeetingPipelineRun(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="pipeline_runs")
    pipeline_name = models.CharField(max_length=80)
    stage = models.CharField(max_length=80)
    status = models.CharField(max_length=40)
    job = models.ForeignKey(ApplicationJob, db_column="job_id", on_delete=models.SET_NULL, null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meeting_pipeline_runs"


class MeetingPeopleCandidate(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="people_candidates")
    pipeline_run = models.ForeignKey(MeetingPipelineRun, db_column="pipeline_run_id", on_delete=models.SET_NULL, null=True, blank=True)
    ref = models.CharField(max_length=20)
    email = models.ForeignKey(Person, db_column="email", to_field="email", on_delete=models.CASCADE)
    alias = models.ForeignKey(PersonAlias, db_column="alias_id", on_delete=models.SET_NULL, null=True, blank=True)
    identity_type = models.CharField(max_length=40)
    display_label = models.TextField(default="")
    sources = models.JSONField(default=list)
    confidence = models.FloatField(default=1.0)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meeting_people_candidates"


class MeetingTopic(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="topics")
    topic_index = models.IntegerField()
    title = models.TextField(default="")
    summary = models.TextField(default="")
    source_chunk_indexes = models.JSONField(default=list)
    confidence = models.FloatField(default=0.0)
    payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meeting_topics"


class MeetingConclusion(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    meeting = models.ForeignKey(Meeting, db_column="meeting_id", on_delete=models.CASCADE, related_name="conclusions")
    title = models.TextField(default="")
    summary = models.TextField(default="")
    one_sentence_summary = models.TextField(null=True, blank=True)
    tl_dr = models.JSONField(default=list)
    source_topic_indexes = models.JSONField(default=list)
    source_chunk_indexes = models.JSONField(default=list)
    confidence = models.FloatField(default=0.0)
    payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "meeting_conclusions"
