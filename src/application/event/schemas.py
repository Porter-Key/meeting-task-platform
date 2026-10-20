from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class TopicSchema(BaseModel):
    title: str = "Untitled topic"
    summary: str = ""
    keywords: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    chunk_indexes: list[int] = Field(default_factory=list)
    confidence: float = 0.0


class TopicExtractionSchema(BaseModel):
    topic: TopicSchema = Field(default_factory=TopicSchema)


class MeetingEventSchema(BaseModel):
    title: str = "Untitled event"
    description: str = ""
    background: str = ""
    actions: list[str] = Field(default_factory=list)
    owner_person_name: str | None = None
    latest_progress: str = ""
    status: str = "open"
    source_topic_indexes: list[int] = Field(default_factory=list)
    topic_ids: list[str] = Field(default_factory=list)
    local_topic_titles: list[str] = Field(default_factory=list)
    chunk_indexes: list[int] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    business_object: str = ""
    business_process: str = ""
    platform_or_system: str = ""
    decision_or_action: str = ""
    current_state: str = ""
    why_it_matters: str = ""
    exclusion_boundary: str = ""


class MeetingEventExtractionSchema(BaseModel):
    meeting_events: list[MeetingEventSchema] = Field(default_factory=list)


class MeetingTaskSchema(BaseModel):
    title: str = ""
    context: str = ""
    action: str = ""
    description: str = ""
    owner_person_name: str | None = None
    owner_ref: str | None = None
    unknown_owner_text: str | None = None
    suggested_owner: str | None = None
    priority: str = "medium"
    category: str = "general"
    status: str = "pending"
    due_date: str | None = None
    original_quote: str | None = None
    source_topic_indexes: list[int] = Field(default_factory=list)
    source_topic_titles: list[str] = Field(default_factory=list)
    source_chunk_indexes: list[int] = Field(default_factory=list)


class MeetingMetadataSchema(BaseModel):
    meeting_id: str = ""
    title: str = ""
    date: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    attendees: list[str] = Field(default_factory=list)
    organizer: str | None = None
    language: str | None = None
    source_system: str | None = None


class MeetingFactSchema(BaseModel):
    fact_id: str = ""
    fact_type: str = ""
    value: str = ""
    normalized_value: str = ""
    source_text: str = ""
    source_chunk_indexes: list[int] = Field(default_factory=list)
    speaker_turns: list[int] = Field(default_factory=list)
    timestamp: str | None = None
    confidence: float = 0.0


class FactLayerSchema(BaseModel):
    meeting_metadata: MeetingMetadataSchema = Field(default_factory=MeetingMetadataSchema)
    facts: list[MeetingFactSchema] = Field(default_factory=list)


class MeetingConclusionDraftSchema(BaseModel):
    title: str = "Untitled meeting conclusion"
    events: list[ConclusionEventSchema] = Field(default_factory=list)
    source_topic_indexes: list[int] = Field(default_factory=list)
    source_chunk_indexes: list[int] = Field(default_factory=list)
    confidence: float = 0.0


class EventTopicGroupSchema(BaseModel):
    title: str = "Untitled event group"
    rationale: str = ""
    topic_indexes: list[int] = Field(default_factory=list)


class EventGroupingPlanSchema(BaseModel):
    groups: list[EventTopicGroupSchema] = Field(default_factory=list)


class PersonTaskGroupSchema(BaseModel):
    person_name: str | None = None
    owner_ref: str | None = None
    unknown_owner_text: str | None = None
    suggested_owner: str | None = None
    assignment_reason: str = ""
    tasks: list[MeetingTaskSchema] = Field(default_factory=list)


class PeopleTasksSchema(BaseModel):
    people_tasks: list[PersonTaskGroupSchema] = Field(default_factory=list)


class TlDrSchema(BaseModel):
    one_sentence_summary: str = ""
    tl_dr: list[str] = Field(default_factory=list)
    summary: str = ""


class DecisionSchema(BaseModel):
    text: str = ""
    relevant_topic_indexes: list[int] = Field(default_factory=list)
    relevant_topics: list[str] = Field(default_factory=list)


class OpenIssueSchema(BaseModel):
    text: str = ""
    source_topic_indexes: list[int] = Field(default_factory=list)
    source_topic_titles: list[str] = Field(default_factory=list)
    source_chunk_indexes: list[int] = Field(default_factory=list)


class ConclusionEventSchema(BaseModel):
    title: str = "Untitled event"
    summary: str = ""
    details: str = ""
    decisions: list[DecisionSchema] = Field(default_factory=list)
    tasks: list[MeetingTaskSchema] = Field(default_factory=list)
    open_issues: list[OpenIssueSchema] = Field(default_factory=list)
    sentiment: str = "neutral"
    source_topic_indexes: list[int] = Field(default_factory=list)
    source_topic_titles: list[str] = Field(default_factory=list)
    source_chunk_indexes: list[int] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    confidence: float = 0.0

    @field_validator("decisions", mode="before")
    @classmethod
    def _coerce_decisions(cls, value: Any) -> Any:
        if isinstance(value, list):
            return [{"text": item} if isinstance(item, str) else item for item in value]
        return value

    @field_validator("open_issues", mode="before")
    @classmethod
    def _coerce_open_issues(cls, value: Any) -> Any:
        if isinstance(value, list):
            return [{"text": item} if isinstance(item, str) else item for item in value]
        return value


class MeetingConclusionSchema(BaseModel):
    title: str = "Untitled meeting conclusion"
    one_sentence_summary: str = ""
    tl_dr: list[str] = Field(default_factory=list)
    summary: str = ""
    fact_layer: FactLayerSchema = Field(default_factory=FactLayerSchema)
    events: list[ConclusionEventSchema] = Field(default_factory=list)
    people_tasks: list[PersonTaskGroupSchema] = Field(default_factory=list)
    source_topic_indexes: list[int] = Field(default_factory=list)
    source_topic_titles: list[str] = Field(default_factory=list)
    source_chunk_indexes: list[int] = Field(default_factory=list)
    confidence: float = 0.0


class GenerateEventsRequest(BaseModel):
    meeting_id: str
    use_existing_chunks: bool = True
    use_ai_cleanup: bool = False
    debug: bool = False


class GenerateEventsResult(BaseModel):
    meeting_id: str
    topics: int
    meeting_events: int = 0
    meeting_conclusions: int = 0
    meeting_conclusion: MeetingConclusionSchema | None = None
    created_events: int = 0
    updated_events: int = 0
