<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/update-meeting-state.md -->
<!-- Title: Update Meeting State -->
<!-- Description: Use the API to pause or resume recording for a live meeting -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Update Meeting State

> Use the API to pause or resume recording for a live meeting

## Overview

The `updateMeetingState` mutation allows you to pause or resume recording for a live meeting through the API. This is useful for controlling the Fireflies bot during an active meeting.

This mutation is rate-limited to 10 requests per hour across all user tiers.

## Arguments

<ParamField path="input" type="UpdateMeetingStateInput!" required>
  Input object containing the meeting ID and action to perform. See [UpdateMeetingStateInput](/schema/input/update-meeting-state-input) for details.
</ParamField>

## Response

<ResponseField name="success" type="Boolean!">
  Whether the action was executed successfully
</ResponseField>

<ResponseField name="action" type="MeetingStateAction!">
  The action that was executed
</ResponseField>

## Usage Example

To update the meeting state, provide the meeting ID and the desired action:

```graphql theme={null}
mutation UpdateMeetingState($input: UpdateMeetingStateInput!) {
  updateMeetingState(input: $input) {
    success
    action
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation UpdateMeetingState($input: UpdateMeetingStateInput!) { updateMeetingState(input: $input) { success action } }",
      "variables": {
        "input": {
          "meeting_id": "your_meeting_id",
          "action": "pause_recording"
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
    query: `mutation UpdateMeetingState($input: UpdateMeetingStateInput!) {
      updateMeetingState(input: $input) {
        success
        action
      }
    }`,
    variables: {
      input: {
        meeting_id: 'your_meeting_id',
        action: 'pause_recording'
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
        mutation UpdateMeetingState($input: UpdateMeetingStateInput!) {
          updateMeetingState(input: $input) {
            success
            action
          }
        }
      ''',
      'variables': {
          'input': {
              'meeting_id': 'your_meeting_id',
              'action': 'pause_recording'
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
          String jsonRequest = "{\"query\": \"mutation UpdateMeetingState($input: UpdateMeetingStateInput!) { updateMeetingState(input: $input) { success action } }\", \"variables\": {\"input\": {\"meeting_id\": \"your_meeting_id\", \"action\": \"pause_recording\"}}}";
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
      "updateMeetingState": {
        "success": true,
        "action": "pause_recording"
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `updateMeetingState` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found">
  <p>The meeting with the specified ID was not found or you do not have access to it.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>You do not have permission to control this meeting. Only the meeting organizer or team admin can update the meeting state.</p>
</Accordion>

<Accordion title="too_many_requests">
  <p>You have exceeded the rate limit for this mutation. The limit is 10 requests per hour. Please wait before making additional requests.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Create Live Action Item" icon="link" href="/graphql-api/mutation/create-live-action-item">
    Create action items during a live meeting
  </Card>

  <Card title="Create Live Soundbite" icon="link" href="/graphql-api/mutation/create-live-soundbite">
    Create soundbites during a live meeting
  </Card>
</CardGroup>
