<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/delete-askfred-thread.md -->
<!-- Title: Delete AskFred Thread -->
<!-- Description: Delete an AskFred conversation thread and all its messages -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete AskFred Thread

> Delete an AskFred conversation thread and all its messages

## Overview

The `deleteAskFredThread` mutation allows you to permanently delete an AskFred conversation thread along with all its associated messages. This action is irreversible.

## Arguments

<ParamField path="id" type="String" required>
  The unique identifier of the AskFred thread to delete
</ParamField>

## Returns

Returns the deleted `AskFredThread` object if successful, allowing you to confirm the deletion details.

## Usage Example

```graphql theme={null}
mutation DeleteThread($id: String!) {
  deleteAskFredThread(id: $id) {
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
      "query": "mutation DeleteThread($id: String!) { deleteAskFredThread(id: $id) { id title transcript_id created_at } }",
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
      mutation DeleteAskFredThread($id: String!) {
        deleteAskFredThread(id: $id) {
          id
          title
          transcript_id
          user_id
          created_at
        }
      }
    `,
    variables: { id: threadId }
  };

  axios
    .post(url, data, { headers: headers })
    .then(result => {
      console.log('Thread deleted:', result.data);
    })
    .catch(e => {
      console.error('Error deleting thread:', e);
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
      mutation DeleteAskFredThread($id: String!) {
          deleteAskFredThread(id: $id) {
              id
              title
              transcript_id
              user_id
              created_at
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
      print('Thread deleted:', response.json())
  else:
      print('Error:', response.text)
  ```
</RequestExample>

<ResponseExample>
  ```json Response theme={null}
  {
    "data": {
      "deleteAskFredThread": {
        "id": "thread_abc123",
        "title": "What were the action items from the Q4 planning meeting?",
        "transcript_id": "transcript_xyz789",
        "user_id": "user_123",
        "created_at": "2024-03-15T10:30:00Z"
      }
    }
  }
  ```
</ResponseExample>

## Important Notes

<Warning>
  Deletion is permanent and cannot be undone
</Warning>

## Error Codes

<Accordion title="object_not_found">
  <p>The specified thread ID does not exist or you don't have access to it</p>
</Accordion>

## Related

<CardGroup cols={2}>
  <Card title="List Threads" icon="link" href="/graphql-api/query/askfred-threads">
    View all your threads before deletion
  </Card>

  <Card title="View Thread Details" icon="link" href="/graphql-api/query/askfred-thread">
    Review thread content before deletion
  </Card>
</CardGroup>
