<!-- Source: https://docs.fireflies.ai/askfred/quickstart.md -->
<!-- Title: Quickstart -->
<!-- Description: Get started with AskFred in minutes - learn how to create threads and ask questions about your meetings -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart

> Get started with AskFred in minutes - learn how to create threads and ask questions about your meetings

## Prerequisites

Before you begin, make sure you have:

1. **API Key**: Obtain your API key from [app.fireflies.ai/integrations](https://app.fireflies.ai/integrations/custom/fireflies)
2. **AI Credits**: Your account must have AI credits to use AskFred. Visit [Upgrade](https://app.fireflies.ai/upgrade) to add AI credits to your plan.
3. **Transcript ID** (optional): The ID of a meeting transcript you want to query

<Note>
  If you don't have a transcript ID, you can query across all your meetings using filters. See [Step 3](#step-3-query-across-meetings) below.
</Note>

## Step 1: Create Your First Thread

Start by asking a question about a specific meeting:

<CodeGroup>
  ```graphql GraphQL theme={null}
  mutation CreateThread {
    createAskFredThread(input: {
      query: "What were the main discussion points?",
      transcript_id: "your_transcript_id",
      response_language: "en",
      format_mode: "markdown"
    }) {
      message {
        id
        thread_id
        answer
        suggested_queries
      }
    }
  }
  ```

  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation CreateThread($input: CreateAskFredThreadInput!) { createAskFredThread(input: $input) { message { id thread_id answer suggested_queries } } }",
      "variables": {
        "input": {
          "query": "What were the main discussion points?",
          "transcript_id": "your_transcript_id",
          "response_language": "en",
          "format_mode": "markdown"
        }
      }
    }' \
    https://api.fireflies.ai/graphql
  ```

  ```javascript JavaScript theme={null}
  const axios = require('axios');

  const url = 'https://api.fireflies.ai/graphql';
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer your_api_key'
  };

  const mutation = `
    mutation CreateThread($input: CreateAskFredThreadInput!) {
      createAskFredThread(input: $input) {
        message {
          id
          thread_id
          answer
          suggested_queries
        }
      }
    }
  `;

  const variables = {
    input: {
      query: 'What were the main discussion points?',
      transcript_id: 'your_transcript_id',
      response_language: 'en',
      format_mode: 'markdown'
    }
  };

  axios
    .post(url, { query: mutation, variables }, { headers })
    .then(response => {
      console.log(response.data.data.createAskFredThread);
    })
    .catch(error => {
      console.error(error);
    });
  ```

  ```python Python theme={null}
  import requests

  url = 'https://api.fireflies.ai/graphql'
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
  }

  mutation = """
  mutation CreateThread($input: CreateAskFredThreadInput!) {
    createAskFredThread(input: $input) {
      message {
        id
        thread_id
        answer
        suggested_queries
      }
    }
  }
  """

  variables = {
      'input': {
          'query': 'What were the main discussion points?',
          'transcript_id': 'your_transcript_id',
          'response_language': 'en',
          'format_mode': 'markdown'
      }
  }

  response = requests.post(
      url,
      json={'query': mutation, 'variables': variables},
      headers=headers
  )

  print(response.json())
  ```
</CodeGroup>

### Response

```json theme={null}
{
  "data": {
    "createAskFredThread": {
      "message": {
        "id": "msg_abc123",
        "thread_id": "thread_xyz789",
        "answer": "The main discussion points were:\n\n1. **Q4 Product Roadmap**: The team reviewed upcoming features...\n2. **Budget Allocation**: Discussion on resource allocation...\n3. **Timeline Concerns**: Several concerns about launch dates...",
        "suggested_queries": [
          "Can you elaborate on the timeline concerns?",
          "What features are prioritized for Q4?",
          "Who raised concerns about the budget?"
        ]
      }
    }
  }
}
```

## Step 2: Ask Follow-up Questions

Continue the conversation with context-aware follow-ups using the `thread_id` from the previous response:

<CodeGroup>
  ```graphql GraphQL theme={null}
  mutation ContinueThread {
    continueAskFredThread(input: {
      thread_id: "thread_xyz789",
      query: "Can you elaborate on the timeline concerns?"
    }) {
      message {
        answer
        suggested_queries
      }
    }
  }
  ```

  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation ContinueThread($input: ContinueAskFredThreadInput!) { continueAskFredThread(input: $input) { message { answer suggested_queries } } }",
      "variables": {
        "input": {
          "thread_id": "thread_xyz789",
          "query": "Can you elaborate on the timeline concerns?"
        }
      }
    }' \
    https://api.fireflies.ai/graphql
  ```

  ```javascript JavaScript theme={null}
  const variables = {
    input: {
      thread_id: 'thread_xyz789',
      query: 'Can you elaborate on the timeline concerns?'
    }
  };

  const mutation = `
    mutation ContinueThread($input: ContinueAskFredThreadInput!) {
      continueAskFredThread(input: $input) {
        message {
          answer
          suggested_queries
        }
      }
    }
  `;

  axios.post(url, { query: mutation, variables }, { headers })
    .then(response => console.log(response.data))
    .catch(error => console.error(error));
  ```

  ```python Python theme={null}
  variables = {
      'input': {
          'thread_id': 'thread_xyz789',
          'query': 'Can you elaborate on the timeline concerns?'
      }
  }

  mutation = """
  mutation ContinueThread($input: ContinueAskFredThreadInput!) {
    continueAskFredThread(input: $input) {
      message {
        answer
        suggested_queries
      }
    }
  }
  """

  response = requests.post(
      url,
      json={'query': mutation, 'variables': variables},
      headers=headers
  )

  print(response.json())
  ```
</CodeGroup>

## Step 3: Query Across Meetings

Analyze patterns across multiple meetings using filters:

<CodeGroup>
  ```graphql GraphQL theme={null}
  mutation CrossMeetingAnalysis {
    createAskFredThread(input: {
      query: "What customer concerns were raised this month?",
      filters: {
        start_time: "2024-03-01T00:00:00Z",
        end_time: "2024-03-31T23:59:59Z",
        participants: ["customer@example.com"]
      }
    }) {
      message {
        answer
        suggested_queries
      }
    }
  }
  ```

  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation CrossMeetingAnalysis($input: CreateAskFredThreadInput!) { createAskFredThread(input: $input) { message { answer suggested_queries } } }",
      "variables": {
        "input": {
          "query": "What customer concerns were raised this month?",
          "filters": {
            "start_time": "2024-03-01T00:00:00Z",
            "end_time": "2024-03-31T23:59:59Z",
            "participants": ["customer@example.com"]
          }
        }
      }
    }' \
    https://api.fireflies.ai/graphql
  ```
</CodeGroup>

<Note>
  For more details on available filters and parameters, see the [createAskFredThread](/graphql-api/mutation/create-askfred-thread) documentation.
</Note>

## Step 4: List Your Threads

Retrieve all your conversation threads:

<CodeGroup>
  ```graphql GraphQL theme={null}
  query GetThreads {
    askfred_threads {
      id
      title
      transcript_id
      created_at
    }
  }
  ```

  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "query { askfred_threads { id title transcript_id created_at } }"
    }' \
    https://api.fireflies.ai/graphql
  ```
</CodeGroup>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Explore Use Cases" icon="lightbulb" href="/askfred/use-cases">
    Discover common scenarios and example questions
  </Card>

  <Card title="API Reference" icon="book" href="/graphql-api/mutation/create-askfred-thread">
    Explore all available parameters and options
  </Card>
</CardGroup>
