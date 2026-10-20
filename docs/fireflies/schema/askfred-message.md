<!-- Source: https://docs.fireflies.ai/schema/askfred-message.md -->
<!-- Title: AskFredMessage -->
<!-- Description: Schema definition for individual messages in AskFred conversation threads -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AskFredMessage

> Schema definition for individual messages in AskFred conversation threads

## Overview

The `AskFredMessage` type represents a single question-answer exchange within an AskFred conversation thread. Each message contains the user's query, the AI-generated response, and optional follow-up suggestions.

## Fields

<ResponseField name="id" type="String!" required>
  Unique identifier for the message
</ResponseField>

<ResponseField name="thread_id" type="String!" required>
  ID of the parent thread this message belongs to
</ResponseField>

<ResponseField name="query" type="String!" required>
  The question or query submitted by the user
</ResponseField>

<ResponseField name="answer" type="String!" required>
  The AI-generated response to the query, formatted according to the specified format\_mode
</ResponseField>

<ResponseField name="suggested_queries" type="[String!]">
  Array of suggested follow-up questions based on the context of the conversation
</ResponseField>

<ResponseField name="status" type="AskFredMessageStatus!" required>
  Current status of the message processing. See [AskFredMessageStatus](#askfredmessagestatus) below.
</ResponseField>

<ResponseField name="created_at" type="String!" required>
  ISO 8601 timestamp when the message was created
</ResponseField>

<ResponseField name="updated_at" type="String">
  ISO 8601 timestamp when the message was last updated
</ResponseField>

## AskFredMessageStatus

An enum representing the processing status of a message:

<ResponseField name="processing" type="enum value">
  The query is currently being processed
</ResponseField>

<ResponseField name="completed" type="enum value">
  The query has been successfully processed and answered
</ResponseField>

<ResponseField name="failed" type="enum value">
  The query processing failed
</ResponseField>

## Example

```json theme={null}
{
  "id": "msg_001",
  "thread_id": "thread_abc123",
  "query": "What were the main action items from the meeting?",
  "answer": "Based on the meeting transcript, here are the main action items:\n\n1. **Marketing Team** - Prepare Q4 campaign strategy by March 25th\n2. **Product Team** - Finalize feature roadmap by March 20th\n3. **Engineering** - Complete API v2 architecture review by March 18th",
  "suggested_queries": [
    "Who is responsible for the Q4 campaign strategy?",
    "What features are planned for the roadmap?",
    "What are the API v2 requirements?"
  ],
  "status": "completed",
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T10:30:15Z"
}
```

## Format Modes

The `answer` field can be formatted in different ways based on the `format_mode` parameter used when creating or continuing a thread:

### Markdown Format

Rich text with headers, lists, bold/italic text, and other markdown features for enhanced readability.

### Plaintext Format

Concise text without any formatting, suitable for systems that don't support markdown.

## Related Types

<CardGroup cols={2}>
  <Card title="AskFredThread" icon="link" href="/schema/askfred-thread">
    Parent thread containing messages
  </Card>

  <Card title="AskFredResponse" icon="link" href="/schema/askfred-response">
    Response wrapper for newly created messages
  </Card>
</CardGroup>
