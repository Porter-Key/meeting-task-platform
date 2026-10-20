<!-- Source: https://docs.fireflies.ai/graphql-api/query/askfred-threads.md -->
<!-- Title: AskFred Threads -->
<!-- Description: Get a summary of all AskFred conversation threads for the current user -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AskFred Threads

> Get a summary of all AskFred conversation threads for the current user

## Overview

The `askfred_threads` query retrieves a summary of all AskFred conversation threads belonging to the authenticated user. This query provides a lightweight overview of threads without including the full message history, making it ideal for listing and browsing conversations.

## Arguments

<ParamField path="transcript_id" type="String">
  Filter threads to only those associated with a specific transcript ID
</ParamField>

## Schema

Fields available to the [AskFredThreadSummary](/schema/askfred-thread-summary) query:

* `id`: Unique identifier for the thread
* `title`: Thread title (typically derived from the first question)
* `transcript_id`: Associated transcript/meeting ID (if applicable)
* `user_id`: ID of the user who created the thread
* `created_at`: Timestamp when the thread was created

## Usage Example

```graphql theme={null}
query GetAskFredThreads {
  askfred_threads {
    id
    title
    transcript_id
    user_id
    created_at
  }
}
```

### With Filter

```graphql theme={null}
query GetFilteredThreads($transcriptId: String) {
  askfred_threads(transcript_id: $transcriptId) {
    id
    title
    transcript_id
    user_id
    created_at
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "query { askfred_threads { id title transcript_id user_id created_at } }"
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

  const data = {
    query: `
      query GetAskFredThreads {
        askfred_threads {
          id
          title
          transcript_id
          user_id
          created_at
        }
      }
    `
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

  query = '''
      query GetAskFredThreads {
          askfred_threads {
              id
              title
              transcript_id
              user_id
              created_at
          }
      }
  '''

  data = {
      'query': query
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
      "askfred_threads": [
        {
          "id": "thread_abc123",
          "title": "What were the action items from the Q4 planning meeting?",
          "transcript_id": "transcript_xyz789",
          "user_id": "user_123",
          "created_at": "2024-03-15T10:30:00Z"
        },
        {
          "id": "thread_def456",
          "title": "Summary of customer feedback discussions",
          "transcript_id": null,
          "user_id": "user_123",
          "created_at": "2024-03-14T14:20:00Z"
        }
      ]
    }
  }
  ```
</ResponseExample>

## Related

<CardGroup cols={2}>
  <Card title="Get Thread Details" icon="link" href="/graphql-api/query/askfred-thread">
    Retrieve complete thread with message history
  </Card>

  <Card title="Create Thread" icon="link" href="/graphql-api/mutation/create-askfred-thread">
    Start a new AskFred conversation
  </Card>
</CardGroup>
