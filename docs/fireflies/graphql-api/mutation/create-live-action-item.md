<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/create-live-action-item.md -->
<!-- Title: Create Live Action Item -->
<!-- Description: Use the API to create an action item during a live meeting -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create Live Action Item

> Use the API to create an action item during a live meeting

## Overview

The `createLiveActionItem` mutation allows you to create an action item during a live meeting through the API. The action item is created using natural language processing via Fred, Fireflies' AI assistant.

This mutation is rate-limited to 10 requests per hour across all user tiers. It also requires AI credits to be available on the user's account.

## Arguments

<ParamField path="input" type="CreateLiveActionItemInput!" required>
  Input object containing the meeting ID and prompt for the action item. See [CreateLiveActionItemInput](/schema/input/create-live-action-item-input) for details.
</ParamField>

## Response

<ResponseField name="success" type="Boolean!">
  Whether the action item was created successfully
</ResponseField>

## Usage Example

To create a live action item, provide the meeting ID and a natural language prompt:

```graphql theme={null}
mutation CreateLiveActionItem($input: CreateLiveActionItemInput!) {
  createLiveActionItem(input: $input) {
    success
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation CreateLiveActionItem($input: CreateLiveActionItemInput!) { createLiveActionItem(input: $input) { success } }",
      "variables": {
        "input": {
          "meeting_id": "your_meeting_id",
          "prompt": "Follow up with the client about the proposal"
        }
      }
    }'
  ```

  ```javascript javascript theme={null}
  const axios = require('axios');

  const url = 'https://api.fireflies.ai/graphql';
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer your_api_key'
  };

  const data = {
    query: `mutation CreateLiveActionItem($input: CreateLiveActionItemInput!) {
      createLiveActionItem(input: $input) {
        success
      }
    }`,
    variables: {
      input: {
        meeting_id: 'your_meeting_id',
        prompt: 'Follow up with the client about the proposal'
      }
    }
  };

  axios
    .post(url, data, { headers: headers })
    .then(result => {
      console.log(result.data);
    })
    .catch(e => {
      console.log(JSON.stringify(e));
    });
  ```

  ```python python theme={null}
  import requests

  url = 'https://api.fireflies.ai/graphql'

  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
  }

  data = {
      'query': '''
        mutation CreateLiveActionItem($input: CreateLiveActionItemInput!) {
          createLiveActionItem(input: $input) {
            success
          }
        }
      ''',
      'variables': {
          'input': {
              'meeting_id': 'your_meeting_id',
              'prompt': 'Follow up with the client about the proposal'
          }
      }
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:
      print(response.json()['data'])
  else:
      print(response.text)
  ```

  ```java java theme={null}
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.net.http.HttpRequest.BodyPublishers;

  public class ApiRequest {
      public static void main(String[] args) {
          HttpClient client = HttpClient.newHttpClient();
          String jsonRequest = "{\"query\": \"mutation CreateLiveActionItem($input: CreateLiveActionItemInput!) { createLiveActionItem(input: $input) { success } }\", \"variables\": {\"input\": {\"meeting_id\": \"your_meeting_id\", \"prompt\": \"Follow up with the client about the proposal\"}}}";
          HttpRequest request = HttpRequest.newBuilder()
              .uri(URI.create("https://api.fireflies.ai/graphql"))
              .header("Content-Type", "application/json")
              .header("Authorization", "Bearer your_api_key")
              .POST(BodyPublishers.ofString(jsonRequest))
              .build();

          client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
              .thenApply(HttpResponse::body)
              .thenAccept(System.out::println)
              .join();
      }
  }
  ```
</RequestExample>

<ResponseExample>
  ```json Response theme={null}
  {
    "data": {
      "createLiveActionItem": {
        "success": true
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `createLiveActionItem` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found">
  <p>The meeting with the specified ID was not found or you do not have access to it.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>You do not have permission to create action items for this meeting. Only the meeting organizer or team admin can create live action items.</p>
</Accordion>

<Accordion title="insufficient_ai_credits">
  <p>Your account does not have sufficient AI credits to perform this operation. Please upgrade your plan or purchase additional credits.</p>
</Accordion>

<Accordion title="too_many_requests">
  <p>You have exceeded the rate limit for this mutation. The limit is 10 requests per hour. Please wait before making additional requests.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Live Action Items" icon="link" href="/graphql-api/query/live-action-items">
    Query live action items for a meeting
  </Card>

  <Card title="Update Meeting State" icon="link" href="/graphql-api/mutation/update-meeting-state">
    Pause or resume recording for a live meeting
  </Card>
</CardGroup>
