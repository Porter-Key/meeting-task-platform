<!-- Source: https://docs.fireflies.ai/schema/askfred-response.md -->
<!-- Title: AskFredResponse -->
<!-- Description: Response wrapper for AskFred mutations -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AskFredResponse

> Response wrapper for AskFred mutations

## Overview

The `AskFredResponse` type is a wrapper object returned by AskFred mutations when creating or continuing conversation threads. It contains the newly generated message with the AI's response to your query.

## Fields

<ResponseField name="message" type="AskFredMessage!" required>
  The generated message containing the query, answer, and metadata. See [AskFredMessage](/schema/askfred-message) for detailed field descriptions.
</ResponseField>

## Example

```json theme={null}
{
  "message": {
    "id": "msg_001",
    "thread_id": "thread_abc123",
    "query": "What were the key decisions made in today's meeting?",
    "answer": "Based on today's meeting, here are the key decisions made:\n\n1. **Product Launch Date**: Confirmed for April 15th, 2024\n2. **Budget Allocation**: Approved $250K for Q2 marketing initiatives\n3. **Team Structure**: Decided to hire 3 additional engineers\n4. **Partnership Strategy**: Approved collaboration with TechCorp",
    "suggested_queries": [
      "What are the specific marketing initiatives planned?",
      "What roles are we hiring for engineering?",
      "What are the terms of the TechCorp partnership?"
    ],
    "status": "completed",
    "created_at": "2024-03-15T14:30:00Z",
    "updated_at": "2024-03-15T14:30:05Z"
  }
}
```

## Related Types

<CardGroup cols={2}>
  <Card title="AskFredMessage" icon="link" href="/schema/askfred-message">
    Detailed message structure
  </Card>

  <Card title="AskFredThread" icon="link" href="/schema/askfred-thread">
    Thread containing multiple messages
  </Card>
</CardGroup>
