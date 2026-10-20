<!-- Source: https://docs.fireflies.ai/schema/askfred-thread-summary.md -->
<!-- Title: AskFredThreadSummary -->
<!-- Description: Lightweight schema for AskFred thread listings -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AskFredThreadSummary

> Lightweight schema for AskFred thread listings

## Overview

The `AskFredThreadSummary` type provides a lightweight representation of an AskFred conversation thread, ideal for displaying thread lists without the overhead of loading all messages. This type is returned when querying multiple threads.

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

## Example

```json theme={null}
{
  "id": "thread_abc123",
  "title": "Q4 Planning Meeting Action Items",
  "transcript_id": "transcript_xyz789",
  "user_id": "user_123",
  "created_at": "2024-03-15T10:30:00Z"
}
```

## Example Query

```graphql theme={null}
query GetThreadsSummary {
  askfred_threads {
    id
    title
    transcript_id
    created_at
  }
}
```

## Related Types

<CardGroup cols={2}>
  <Card title="AskFredThread" icon="link" href="/schema/askfred-thread">
    Full thread type with messages
  </Card>

  <Card title="AskFredMessage" icon="link" href="/schema/askfred-message">
    Individual messages within threads
  </Card>
</CardGroup>
