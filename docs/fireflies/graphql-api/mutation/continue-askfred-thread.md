<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/continue-askfred-thread.md -->
<!-- Title: Continue AskFred Thread -->
<!-- Description: Continue an existing AskFred conversation with follow-up questions -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Continue AskFred Thread

> Continue an existing AskFred conversation with follow-up questions

## Overview

The `continueAskFredThread` mutation allows you to add follow-up questions to an existing AskFred conversation thread. This maintains the context of previous questions and answers, enabling more sophisticated multi-turn conversations about your meeting data.

## Arguments

<ParamField path="input" type="ContinueAskFredThreadInput">
  <Expandable>
    <ResponseField name="thread_id" type="String" required>
      The ID of the existing thread to continue
    </ResponseField>

    <ResponseField name="query" type="String" required>
      Your follow-up question or query. Maximum 2000 characters.
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

Returns an `AskFredResponse` object containing the generated message with the answer to your follow-up query.

## Usage Example

```graphql theme={null}
mutation ContinueThread($input: ContinueAskFredThreadInput!) {
  continueAskFredThread(input: $input) {
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

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation ContinueThread($input: ContinueAskFredThreadInput!) { continueAskFredThread(input: $input) { message { id thread_id query answer suggested_queries status } } }",
      "variables": {
        "input": {
          "thread_id": "thread_abc123",
          "query": "Can you provide more details about the budget allocation?",
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

  const input = {
    thread_id: "thread_abc123",
    query: "Can you provide more details about the budget allocation?",
    response_language: "en",
    format_mode: "markdown"
  };

  const data = {
    query: `
      mutation ContinueAskFredThread($input: ContinueAskFredThreadInput!) {
        continueAskFredThread(input: $input) {
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
    variables: { input }
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

  input_data = {
      "thread_id": "thread_abc123",
      "query": "Can you provide more details about the budget allocation?",
      "response_language": "en",
      "format_mode": "markdown"
  }

  query = '''
      mutation ContinueAskFredThread($input: ContinueAskFredThreadInput!) {
          continueAskFredThread(input: $input) {
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
      'variables': {'input': input_data}
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
      "continueAskFredThread": {
        "message": {
          "id": "msg_003",
          "thread_id": "thread_abc123",
          "query": "Can you provide more details about the budget allocation?",
          "answer": "Certainly! Here are the detailed budget allocations discussed in the meeting:\n\n## Q4 Budget Breakdown ($150K Total)\n\n### Engineering (60% - $90K)\n- **Infrastructure Improvements**: $30K\n  - Cloud services optimization\n  - Database scaling\n  - Security enhancements\n- **Feature Development**: $45K\n  - Mobile app features: $25K\n  - API v2 development: $20K\n- **Technical Debt**: $15K\n  - Code refactoring\n  - Legacy system migration\n\n### Design & UX (25% - $37.5K)\n- **User Research**: $10K\n- **Design System Updates**: $15K\n- **Prototype Development**: $12.5K\n\n### Marketing & Growth (15% - $22.5K)\n- **Content Creation**: $7.5K\n- **Paid Acquisition Tests**: $10K\n- **Partnership Development**: $5K\n\nThe CFO emphasized maintaining a 10% contingency within each category for unexpected costs.",
          "suggested_queries": [
            "Who is responsible for managing each budget category?",
            "What are the key milestones for the infrastructure improvements?",
            "How will the budget be tracked and reported?"
          ],
          "status": "completed",
          "created_at": "2024-03-15T10:35:00Z"
        }
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

<Accordion title="object_not_found">
  <p>The specified thread\_id does not exist or you don't have access to it</p>
</Accordion>

<Accordion title="require_ai_credits">
  <p>You have insufficient AI credits to continue the thread. Please upgrade your plan or purchase additional credits.</p>
</Accordion>

<Accordion title="invalid_language_code">
  <p>The language code you provided is invalid. Please refer to the [Language Codes](/miscellaneous/language-codes) page for a list of valid language codes.</p>
</Accordion>

## Related

<CardGroup cols={2}>
  <Card title="View Thread" icon="link" href="/graphql-api/query/askfred-thread">
    Get complete thread with all messages
  </Card>

  <Card title="Create New Thread" icon="link" href="/graphql-api/mutation/create-askfred-thread">
    Start a new conversation thread
  </Card>
</CardGroup>
