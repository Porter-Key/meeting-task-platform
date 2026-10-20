<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/create-live-soundbite.md -->
<!-- Title: Create Live Soundbite -->
<!-- Description: Use the API to create a soundbite during a live meeting -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create Live Soundbite

> Use the API to create a soundbite during a live meeting

## Overview

The `createLiveSoundbite` mutation allows you to create a soundbite during a live meeting through the API. The soundbite is created using natural language processing via Fred, Fireflies' AI assistant.

<Note>
  **Rate Limit:** This mutation is rate-limited to 10 requests per hour across all user tiers. If you exceed this limit, you will receive a `too_many_requests` error with a `retryAfter` timestamp indicating when you can make requests again.

  **AI Credits:** This mutation requires AI credits to be available on the user's account.
</Note>

## Arguments

<ParamField path="input" type="CreateLiveSoundbiteInput!" required>
  Input object containing the meeting ID and prompt for the soundbite. See [CreateLiveSoundbiteInput](/schema/input/create-live-soundbite-input) for details.
</ParamField>

## Response

<ResponseField name="success" type="Boolean!">
  Whether the soundbite was created successfully
</ResponseField>

## Usage Example

To create a live soundbite, provide the meeting ID and a natural language prompt:

```graphql theme={null}
mutation CreateLiveSoundbite($input: CreateLiveSoundbiteInput!) {
  createLiveSoundbite(input: $input) {
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
      "query": "mutation CreateLiveSoundbite($input: CreateLiveSoundbiteInput!) { createLiveSoundbite(input: $input) { success } }",
      "variables": {
        "input": {
          "meeting_id": "your_meeting_id",
          "prompt": "Create a soundbite from the last 2 minutes"
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
    query: `mutation CreateLiveSoundbite($input: CreateLiveSoundbiteInput!) {
      createLiveSoundbite(input: $input) {
        success
      }
    }`,
    variables: {
      input: {
        meeting_id: 'your_meeting_id',
        prompt: 'Create a soundbite from the last 2 minutes'
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
        mutation CreateLiveSoundbite($input: CreateLiveSoundbiteInput!) {
          createLiveSoundbite(input: $input) {
            success
          }
        }
      ''',
      'variables': {
          'input': {
              'meeting_id': 'your_meeting_id',
              'prompt': 'Create a soundbite from the last 2 minutes'
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
          String jsonRequest = "{\"query\": \"mutation CreateLiveSoundbite($input: CreateLiveSoundbiteInput!) { createLiveSoundbite(input: $input) { success } }\", \"variables\": {\"input\": {\"meeting_id\": \"your_meeting_id\", \"prompt\": \"Create a soundbite from the last 2 minutes\"}}}";
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
      "createLiveSoundbite": {
        "success": true
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `createLiveSoundbite` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found">
  <p>The meeting with the specified ID was not found or you do not have access to it.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>You do not have permission to create soundbites for this meeting. Only the meeting organizer or team admin can create live soundbites.</p>
</Accordion>

<Accordion title="insufficient_ai_credits">
  <p>Your account does not have sufficient AI credits to perform this operation. Please upgrade your plan or purchase additional credits.</p>
</Accordion>

<Accordion title="too_many_requests">
  <p>You have exceeded the rate limit of 10 requests per hour. Wait until the time specified in the `retryAfter` field before making additional requests.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Create Bite" icon="link" href="/graphql-api/mutation/create-bite">
    Create a soundbite for a completed meeting
  </Card>

  <Card title="Update Meeting State" icon="link" href="/graphql-api/mutation/update-meeting-state">
    Pause or resume recording for a live meeting
  </Card>
</CardGroup>
