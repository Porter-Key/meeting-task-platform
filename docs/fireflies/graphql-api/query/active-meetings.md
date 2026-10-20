<!-- Source: https://docs.fireflies.ai/graphql-api/query/active-meetings.md -->
<!-- Title: Active Meetings -->
<!-- Description: Query active meetings in progress -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Active Meetings

> Query active meetings in progress

## Overview

The active\_meetings query is designed to fetch a list of meetings that are currently active (in progress). This endpoint allows you to monitor ongoing meetings for users in your team.

## Arguments

<ParamField path="email" type="String">
  Filter active meetings by a specific user's email address.

  **Permission requirements:**

  * **Regular users**: Can only query their own active meetings (must pass their own email or omit this field)
  * **Admins**: Can query active meetings for any user in their team

  If this field is omitted, the query returns active meetings for the authenticated user.

  The email must be valid and belong to a user in the same team as the requester.
</ParamField>

<ParamField path="states" type="[MeetingState]">
  Filter active meetings by their state. Accepts an array of [MeetingState](/schema/enum/meeting-state) values.

  **Possible values:**

  * `active`: Meetings that are currently in progress
  * `paused`: Meetings that have been paused

  If this field is omitted, the query returns meetings in both `active` and `paused` states by default.
</ParamField>

## Schema

Fields available to the [ActiveMeeting](/schema/active-meeting) query

## Usage Example

```graphql theme={null}
query ActiveMeetings($email: String, $states: [MeetingState!]) {
  active_meetings(input: { email: $email, states: $states }) {
    id
    title
    organizer_email
    meeting_link
    start_time
    end_time
    privacy
    state
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_api_key" \
      --data '{ "query": "query ActiveMeetings { active_meetings { id title organizer_email meeting_link start_time } }" }' \
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
    query: 'query ActiveMeetings { active_meetings { id title organizer_email meeting_link start_time } }'
  };

  axios
    .post(url, data, { headers: headers })
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });
  ```

  ```python python theme={null}
  import requests

  url = 'https://api.fireflies.ai/graphql'
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
  }

  data = '{"query": "query ActiveMeetings { active_meetings { id title organizer_email meeting_link start_time } }"}'

  response = requests.post(url, headers=headers, data=data)
  print(response.json())
  ```

  ```java java theme={null}
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.net.http.HttpResponse.BodyHandlers;

  public class ApiRequest {
      public static void main(String[] args) throws Exception {
          HttpClient client = HttpClient.newHttpClient();
          String json = "{\"query\":\"query ActiveMeetings { active_meetings { id title organizer_email meeting_link start_time } } \"}";
          HttpRequest request = HttpRequest.newBuilder()
                  .uri(URI.create("https://api.fireflies.ai/graphql"))
                  .header("Content-Type", "application/json")
                  .header("Authorization", "Bearer your_api_key")
                  .POST(HttpRequest.BodyPublishers.ofString(json))
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
      "active_meetings": [
        {
          "id": "meeting-id-1",
          "title": "Team Standup",
          "organizer_email": "user@example.com",
          "meeting_link": "https://zoom.us/j/123456789",
          "start_time": "2024-01-15T10:00:00.000Z",
          "state": "active"
        },
        {
          "id": "meeting-id-2",
          "title": "Client Review",
          "organizer_email": "user@example.com",
          "meeting_link": "https://meet.google.com/abc-defg-hij",
          "start_time": "2024-01-15T14:30:00.000Z",
          "state": "paused"
        }
      ]
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `active_meetings` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found (user)">
  <p>The user email you are trying to query does not exist or is not in the same team as the requesting user.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>You do not have permission to query active meetings for other users. Regular users can only query their own active meetings. Admin privileges are required to query other users' active meetings.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcripts" icon="link" href="/graphql-api/query/transcripts">
    Query completed meetings and transcripts
  </Card>

  <Card title="Add to Live Meeting" icon="link" href="/graphql-api/mutation/add-to-live">
    Join an active meeting with Fireflies.ai bot
  </Card>
</CardGroup>
