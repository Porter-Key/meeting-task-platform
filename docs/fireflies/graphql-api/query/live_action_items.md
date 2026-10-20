<!-- Source: https://docs.fireflies.ai/graphql-api/query/live_action_items.md -->
<!-- Title: Live Action Items -->
<!-- Description: Query live action items for a meeting -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Live Action Items

> Query live action items for a meeting

## Overview

The `live_action_items` query allows you to fetch action items for a live meeting. This includes both action items automatically created by Fireflies during the meeting and action items created via the `createLiveActionItem` mutation.

## Arguments

<ParamField path="meeting_id" type="ID!" required>
  The ID of the meeting to fetch live action items for
</ParamField>

## Response

Returns an array of `LiveActionItem` objects with the following fields:

<ResponseField name="name" type="String">
  Name of the person who the action item is associated with
</ResponseField>

<ResponseField name="action_item" type="String!">
  The action item text
</ResponseField>

## Usage Example

To fetch live action items for a meeting:

```graphql theme={null}
query LiveActionItems($meeting_id: ID!) {
  live_action_items(meeting_id: $meeting_id) {
    name
    action_item
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "query LiveActionItems($meeting_id: ID!) { live_action_items(meeting_id: $meeting_id) { name action_item } }",
      "variables": {
        "meeting_id": "your_meeting_id"
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
    query: `query LiveActionItems($meeting_id: ID!) {
      live_action_items(meeting_id: $meeting_id) {
        name
        action_item
      }
    }`,
    variables: {
      meeting_id: 'your_meeting_id'
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
        query LiveActionItems($meeting_id: ID!) {
          live_action_items(meeting_id: $meeting_id) {
            name
            action_item
          }
        }
      ''',
      'variables': {
          'meeting_id': 'your_meeting_id'
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
          String jsonRequest = "{\"query\": \"query LiveActionItems($meeting_id: ID!) { live_action_items(meeting_id: $meeting_id) { name action_item } }\", \"variables\": {\"meeting_id\": \"your_meeting_id\"}}";
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
      "live_action_items": [
        {
          "name": "John Doe",
          "action_item": "Follow up with the client about the proposal"
        },
        {
          "name": "Jane Smith",
          "action_item": "Schedule a follow-up meeting for next week"
        }
      ]
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `live_action_items` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found">
  <p>The meeting with the specified ID was not found or you do not have access to it.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>You do not have permission to view action items for this meeting. Only the meeting organizer or team admin can view live action items.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Create Live Action Item" icon="link" href="/graphql-api/mutation/create-live-action-item">
    Create action items during a live meeting
  </Card>

  <Card title="Update Meeting State" icon="link" href="/graphql-api/mutation/update-meeting-state">
    Pause or resume recording for a live meeting
  </Card>
</CardGroup>
