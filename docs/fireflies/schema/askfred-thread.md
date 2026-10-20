<!-- Source: https://docs.fireflies.ai/schema/askfred-thread.md -->
<!-- Title: AskFredThread -->
<!-- Description: Schema definition for AskFred conversation threads -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AskFredThread

> Schema definition for AskFred conversation threads

## Overview

The `AskFredThread` type represents a conversation thread in the AskFred system. Each thread contains a series of questions and answers about meeting transcripts, maintaining context throughout the conversation.

## Fields

<ResponseField name="id" type="String!" required>
  Unique identifier for the thread
</ResponseField>

<ResponseField name="title" type="String!" required>
  Title of the thread, typically derived from the first question asked
</ResponseField>

<ResponseField name="transcript_id" type="String">
  ID of the specific meeting/transcript this thread is associated with (if applicable)
</ResponseField>

<ResponseField name="user_id" type="String!" required>
  ID of the user who created the thread
</ResponseField>

<ResponseField name="created_at" type="String!" required>
  ISO 8601 timestamp when the thread was created
</ResponseField>

<ResponseField name="messages" type="[AskFredMessage!]!" required>
  Array of messages in the thread, containing questions and answers. See [AskFredMessage](/schema/askfred-message) for details.
</ResponseField>

## Example

```json theme={null}
{
  "id": "thread_abc123",
  "title": "Q4 Planning Meeting Action Items",
  "transcript_id": "transcript_xyz789",
  "user_id": "user_123",
  "created_at": "2024-03-15T10:30:00Z",
  "messages": [
    {
      "id": "msg_001",
      "thread_id": "thread_abc123",
      "query": "What were the action items from the Q4 planning meeting?",
      "answer": "Based on the Q4 planning meeting...",
      "suggested_queries": ["Who is responsible for...", "What is the timeline..."],
      "status": "completed",
      "created_at": "2024-03-15T10:30:00Z"
    }
  ]
}
```

## Related Types

<CardGroup cols={2}>
  <Card title="AskFredMessage" icon="link" href="/schema/askfred-message">
    Individual messages within a thread
  </Card>

  <Card title="AskFredThreadSummary" icon="link" href="/schema/askfred-thread-summary">
    Lightweight thread summary for listings
  </Card>
</CardGroup>
