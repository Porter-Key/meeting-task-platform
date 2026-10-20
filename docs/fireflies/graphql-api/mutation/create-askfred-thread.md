<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/create-askfred-thread.md -->
<!-- Title: Create AskFred Thread -->
<!-- Description: Create a new AskFred conversation thread with a question about your meetings -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create AskFred Thread

> Create a new AskFred conversation thread with a question about your meetings

## Overview

The `createAskFredThread` mutation allows you to start a new AskFred conversation by asking questions about your meeting transcripts. You can ask about a specific meeting or search across multiple meetings using filters. AskFred uses AI to analyze your meeting data and provide intelligent, context-aware answers.

## Arguments

<ParamField path="input" type="CreateAskFredThreadInput">
  <Expandable>
    <ResponseField name="query" type="String" required>
      Your question or query about the meeting(s). Maximum 2000 characters.
    </ResponseField>

    <ResponseField name="transcript_id" type="String">
      ID of a specific transcript/meeting to query. If provided, the question will be answered based only on this meeting.
    </ResponseField>

    <ResponseField name="filters" type="AskFredMeetingFiltersInput">
      Filters to search across multiple meetings. Only used if transcript\_id is not provided.

      <Expandable>
        <ResponseField name="start_time" type="String">
          Filter meetings from this date/time (ISO 8601 format). Cannot be more than 1 year in the past. If not provided, defaults to 30 days before end\_time.
        </ResponseField>

        <ResponseField name="end_time" type="String">
          Filter meetings until this date/time (ISO 8601 format). If not provided, defaults to today.
        </ResponseField>

        <ResponseField name="channel_ids" type="[String]">
          Filter by specific channel/integration IDs
        </ResponseField>

        <ResponseField name="organizers" type="[String]">
          Filter by meeting organizer email addresses
        </ResponseField>

        <ResponseField name="participants" type="[String]">
          Filter by participant email addresses
        </ResponseField>

        <ResponseField name="transcript_ids" type="[String]">
          Filter by specific transcript IDs
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="response_language" type="LanguageCode">
      Language code for the response (e.g., 'en' for English, 'es' for Spanish). See [Language Codes](/miscellaneous/language-codes) for full list.
    </ResponseField>

    <ResponseField name="format_mode" type="FormatMode">
      Response format: 'markdown' for rich formatting or 'plaintext' for simple text
    </ResponseField>
  </Expandable>
</ParamField>

## Returns

Returns an `AskFredResponse` object containing the generated message with the answer to your query.

## Usage Example

### Query a Specific Meeting

```graphql theme={null}
mutation CreateThreadForMeeting($input: CreateAskFredThreadInput!) {
  createAskFredThread(input: $input) {
    message {
      id
      thread_id
      query
      answer
      suggested_queries
      status
      created_at
    }
  }
}
```

### Query Across Multiple Meetings

```graphql theme={null}
mutation CreateThreadWithFilters($input: CreateAskFredThreadInput!) {
  createAskFredThread(input: $input) {
    message {
      id
      thread_id
      query
      answer
      suggested_queries
      status
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
      "query": "mutation CreateThread($input: CreateAskFredThreadInput!) { createAskFredThread(input: $input) { message { id thread_id query answer suggested_queries status } } }",
      "variables": {
        "input": {
          "query": "What were the main decisions made in the product planning meeting?",
          "transcript_id": "transcript_xyz789",
          "response_language": "en",
          "format_mode": "markdown"
        }
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

  // Example 1: Query a specific meeting
  const inputForSpecificMeeting = {
    query: "What were the action items discussed?",
    transcript_id: "transcript_xyz789",
    response_language: "en",
    format_mode: "markdown"
  };

  // Example 2: Query across meetings with filters
  const inputWithFilters = {
    query: "What customer concerns were raised this week?",
    filters: {
      start_time: "2024-03-10T00:00:00Z",
      end_time: "2024-03-17T00:00:00Z",
      participants: ["customer@example.com"]
    },
    response_language: "en",
    format_mode: "markdown"
  };

  const data = {
    query: `
      mutation CreateAskFredThread($input: CreateAskFredThreadInput!) {
        createAskFredThread(input: $input) {
          message {
            id
            thread_id
            query
            answer
            suggested_queries
            status
            created_at
          }
        }
      }
    `,
    variables: { input: inputForSpecificMeeting }
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

  # Example 1: Query a specific meeting
  input_specific = {
      "query": "What were the action items discussed?",
      "transcript_id": "transcript_xyz789",
      "response_language": "en",
      "format_mode": "markdown"
  }

  # Example 2: Query across meetings with filters
  input_filtered = {
      "query": "What customer concerns were raised this week?",
      "filters": {
          "start_time": "2024-03-10T00:00:00Z",
          "end_time": "2024-03-17T00:00:00Z",
          "participants": ["customer@example.com"]
      },
      "response_language": "en",
      "format_mode": "markdown"
  }

  query = '''
      mutation CreateAskFredThread($input: CreateAskFredThreadInput!) {
          createAskFredThread(input: $input) {
              message {
                  id
                  thread_id
                  query
                  answer
                  suggested_queries
                  status
                  created_at
              }
          }
      }
  '''

  data = {
      'query': query,
      'variables': {'input': input_specific}
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
      "createAskFredThread": {
        "message": {
          "id": "msg_001",
          "thread_id": "thread_new123",
          "query": "What were the main decisions made in the product planning meeting?",
          "answer": "Based on the product planning meeting transcript, here are the main decisions made:\n\n## Product Roadmap\n- **Q4 Focus**: Prioritize mobile app improvements and API v2 development\n- **Feature Freeze**: No new features after November 15th to focus on stability\n\n## Resource Allocation\n- **Team Expansion**: Approved hiring 2 senior engineers and 1 UX designer\n- **Budget**: Allocated $150K for Q4 development initiatives\n\n## Timeline\n- **Beta Release**: Scheduled for December 1st\n- **Public Launch**: Targeted for January 15th\n\n## Strategic Partnerships\n- **Integration Partners**: Approved partnerships with Slack and Microsoft Teams\n- **API Access**: Will provide early access to 5 strategic partners",
          "suggested_queries": [
            "What specific mobile app improvements were discussed?",
            "Who will be responsible for the API v2 development?",
            "What were the concerns raised about the timeline?"
          ],
          "status": "completed",
          "created_at": "2024-03-15T10:30:00Z"
        }
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

<Accordion title="invalid_arguments">
  <p>Validation error occurred. Common causes:</p>

  <ul>
    <li>Query exceeds 2000 character limit or is empty</li>
    <li>Both transcript\_id and filters are provided (only one is allowed)</li>
    <li>start\_time is more than 1 year in the past</li>
    <li>start\_time is not before end\_time</li>
  </ul>
</Accordion>

<Accordion title="object_not_found">
  <p>The specified transcript\_id does not exist or you don't have access to it</p>
</Accordion>

<Accordion title="require_ai_credits">
  <p>You don't have access to AI credits. Upgrade your plan to use AskFred.</p>
</Accordion>

<Accordion title="invalid_language_code">
  <p>The provided response\_language code is not supported. See <a href="/miscellaneous/language-codes">Language Codes</a> for valid options.</p>
</Accordion>

## Related

<CardGroup cols={2}>
  <Card title="Continue Thread" icon="link" href="/graphql-api/mutation/continue-askfred-thread">
    Add follow-up questions to continue the conversation
  </Card>

  <Card title="List Threads" icon="link" href="/graphql-api/query/askfred-threads">
    View all your AskFred conversation threads
  </Card>
</CardGroup>
