<!-- Source: https://docs.fireflies.ai/graphql-api/query/askfred-thread.md -->
<!-- Title: AskFred Thread -->
<!-- Description: Get a specific AskFred conversation thread with all its messages -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AskFred Thread

> Get a specific AskFred conversation thread with all its messages

## Overview

The `askfred_thread` query retrieves a specific AskFred conversation thread by its ID, including the complete message history. This query provides full details about a thread including all questions asked, answers received, and suggested follow-up queries.

## Arguments

<ParamField path="id" type="String" required>
  The unique identifier of the AskFred thread to retrieve
</ParamField>

## Schema

Fields available to the [AskFredThread](/schema/askfred-thread) query:

* `id`: Unique identifier for the thread
* `title`: Thread title
* `transcript_id`: Associated transcript/meeting ID (if applicable)
* `user_id`: ID of the user who created the thread
* `created_at`: Timestamp when the thread was created
* `messages`: Array of [AskFredMessage](/schema/askfred-message) objects containing:
  * `id`: Message identifier
  * `thread_id`: Parent thread ID
  * `query`: The question asked
  * `answer`: The AI-generated response
  * `suggested_queries`: Array of suggested follow-up questions
  * `status`: Message processing status (processing, completed, failed)
  * `error`: Error message if the query failed
  * `created_at`: When the message was created
  * `updated_at`: When the message was last updated

## Usage Example

```graphql theme={null}
query GetAskFredThread($threadId: String!) {
  askfred_thread(id: $threadId) {
    id
    title
    transcript_id
    user_id
    created_at
    messages {
      id
      thread_id
      query
      answer
      suggested_queries
      status
      error
      created_at
      updated_at
    }
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "query GetThread($id: String!) { askfred_thread(id: $id) { id title transcript_id messages { query answer suggested_queries status } } }",
      "variables": {
        "id": "thread_abc123"
      }
    }' \
    https://api.fireflies.ai/graphql
  ```

  ```javascript javascript theme={null}
  const axios = require('axios');

  const url = 'https://api.fireflies.ai/graphql';
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer your_api_key'
  };

  const threadId = 'thread_abc123';

  const data = {
    query: `
      query GetAskFredThread($id: String!) {
        askfred_thread(id: $id) {
          id
          title
          transcript_id
          user_id
          created_at
          messages {
            id
            query
            answer
            suggested_queries
            status
            created_at
          }
        }
      }
    `,
    variables: {
      id: threadId
    }
  };

  axios
    .post(url, data, { headers: headers })
    .then(result => {
      console.log(result.data);
    })
    .catch(e => {
      console.error(e);
    });
  ```

  ```python python theme={null}
  import requests

  url = 'https://api.fireflies.ai/graphql'

  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
  }

  thread_id = 'thread_abc123'

  query = '''
      query GetAskFredThread($id: String!) {
          askfred_thread(id: $id) {
              id
              title
              transcript_id
              user_id
              created_at
              messages {
                  id
                  query
                  answer
                  suggested_queries
                  status
                  created_at
              }
          }
      }
  '''

  variables = {
      'id': thread_id
  }

  data = {
      'query': query,
      'variables': variables
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:
      print(response.json())
  else:
      print(response.text)
  ```
</RequestExample>

<ResponseExample>
  ```json Response theme={null}
  {
    "data": {
      "askfred_thread": {
        "id": "thread_abc123",
        "title": "What were the action items from the Q4 planning meeting?",
        "transcript_id": "transcript_xyz789",
        "user_id": "user_123",
        "created_at": "2024-03-15T10:30:00Z",
        "messages": [
          {
            "id": "msg_001",
            "query": "What were the action items from the Q4 planning meeting?",
            "answer": "Based on the Q4 planning meeting, here are the key action items:\n\n1. **Product Development** - Sarah to finalize the feature roadmap by March 20th\n2. **Marketing Campaign** - John to prepare Q4 marketing strategy presentation by March 25th\n3. **Budget Review** - Finance team to provide updated budget allocations by March 18th\n4. **Customer Success** - Emma to compile customer feedback report by end of week",
            "suggested_queries": [
              "Who is responsible for the product roadmap?",
              "What is the timeline for the marketing strategy?",
              "What were the budget concerns discussed?"
            ],
            "status": "completed",
            "created_at": "2024-03-15T10:30:00Z"
          },
          {
            "id": "msg_002",
            "query": "What were the budget concerns discussed?",
            "answer": "The main budget concerns discussed in the meeting were:\n\n1. **Resource Allocation** - Need to balance investment between product development and marketing\n2. **Headcount** - Discussion about hiring 3 new engineers vs 2 engineers and 1 marketing specialist\n3. **Tool Costs** - Review of current software subscriptions to identify cost-saving opportunities\n4. **Travel Budget** - Proposed 20% reduction in Q4 travel budget due to increased virtual meeting effectiveness",
            "suggested_queries": [
              "What was the final decision on headcount?",
              "Which software subscriptions were identified for review?",
              "How much is the current travel budget?"
            ],
            "status": "completed",
            "created_at": "2024-03-15T10:32:00Z"
          }
        ]
      }
    }
  }
  ```
</ResponseExample>

## Related

<CardGroup cols={2}>
  <Card title="List All Threads" icon="link" href="/graphql-api/query/askfred-threads">
    Get a summary of all your threads
  </Card>

  <Card title="Continue Thread" icon="link" href="/graphql-api/mutation/continue-askfred-thread">
    Add a follow-up question to this thread
  </Card>
</CardGroup>
