from __future__ import annotations

from django.contrib import admin

from domain.models.event import Event, EventMeetingMetadata
from domain.models.job import ApplicationJob
from domain.models.lifecycle import BeatSchedule
from domain.models.logs import ApplicationLog
from domain.models.meeting import Meeting, MeetingChunk, MeetingConclusion, MeetingPeopleCandidate, MeetingPersonLink, MeetingPipelineRun, MeetingSource, MeetingTopic, MeetingTranscript
from domain.models.monday import MondayBoard, MondayColumn, MondayGroup, MondayIdentityCandidate, MondayPushRun, MondayPushRunItem, MondayTaskLink, MondayTeam, MondayUser, MondayUserMapping
from domain.models.people import Person, PersonAlias, PersonEmailAlias
from domain.models.task_masterlist import TaskAssigneeLink, TaskExternalLink, TaskMasterlist, TaskOrigin, TaskVersion

MODELS = [
    ApplicationJob,
    ApplicationLog,
    BeatSchedule,
    Event,
    EventMeetingMetadata,
    Meeting,
    MeetingChunk,
    MeetingConclusion,
    MeetingPeopleCandidate,
    MeetingPersonLink,
    MeetingPipelineRun,
    MeetingSource,
    MeetingTopic,
    MeetingTranscript,
    MondayBoard,
    MondayColumn,
    MondayGroup,
    MondayIdentityCandidate,
    MondayPushRun,
    MondayPushRunItem,
    MondayTaskLink,
    MondayTeam,
    MondayUser,
    MondayUserMapping,
    Person,
    PersonAlias,
    PersonEmailAlias,
    TaskAssigneeLink,
    TaskExternalLink,
    TaskMasterlist,
    TaskOrigin,
    TaskVersion,
]

for model in MODELS:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
