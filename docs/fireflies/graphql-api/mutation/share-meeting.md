<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/share-meeting.md -->
<!-- Title: Share Meeting -->
<!-- Description: Use the API to share meeting transcripts with external users via email -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Share Meeting

> Use the API to share meeting transcripts with external users via email

## Overview

The `shareMeeting` mutation shares a meeting transcript with one or more users by email. Shared users receive access to view the transcript without needing to be on the same team.

## Arguments

<ParamField path="input" type="ShareMeetingInput" required>
  The sharing configuration. See [ShareMeetingInput](/schema/input/share-meeting-input).
</ParamField>

## Usage Example

To share a meeting, provide the meeting ID and an array of email addresses. You can optionally set an expiry period.

```graphql theme={null}
mutation ShareMeeting($input: ShareMeetingInput!) {
  shareMeeting(input: $input) {
    success
    message
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	-d '{
  		"query": "mutation($input: ShareMeetingInput!) { shareMeeting(input: $input) { success message } }",
  		"variables": {
  			"input": {
  				"meeting_id": "your_meeting_id",
  				"emails": ["user@example.com"],
  				"expiry_days": 7
  			}
  		}
  	}'
  ```

  ```javascript javascript theme={null}
  const axios = require('axios');

  const url = 'https://api.fireflies.ai/graphql';
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your_api_key'
  };

  const data = {
    query: `
      mutation($input: ShareMeetingInput!) {
        shareMeeting(input: $input) {
          success
          message
        }
      }
    `,
    variables: {
      input: {
        meeting_id: 'your_meeting_id',
        emails: ['user@example.com'],
        expiry_days: 7
      }
    }
  };

  const response = await axios.post(url, data, { headers });
  console.log(response.data);
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
      mutation($input: ShareMeetingInput!) {
        shareMeeting(input: $input) {
          success
          message
        }
      }
    ''',
    'variables': {
      'input': {
        'meeting_id': 'your_meeting_id',
        'emails': ['user@example.com'],
        'expiry_days': 7
      }
    }
  }

  response = requests.post(url, json=data, headers=headers)
  print(response.json())
  ```

  ```java java theme={null}
  import java.io.IOException;
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.net.http.HttpRequest.BodyPublishers;

  public class ShareMeetingExample {
      public static void main(String[] args) throws IOException, InterruptedException {
          HttpClient client = HttpClient.newHttpClient();

          String json = "{"
              + "\"query\":\"mutation($input: ShareMeetingInput!) { shareMeeting(input: $input) { success message } }\","
              + "\"variables\":{"
              + "\"input\":{"
              + "\"meeting_id\":\"your_meeting_id\","
              + "\"emails\":[\"user@example.com\"],"
              + "\"expiry_days\":7"
              + "}"
              + "}"
              + "}";

          HttpRequest request = HttpRequest.newBuilder()
                  .uri(URI.create("https://api.fireflies.ai/graphql"))
                  .header("Content-Type", "application/json")
                  .header("Authorization", "Bearer your_api_key")
                  .POST(BodyPublishers.ofString(json))
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
      "shareMeeting": {
        "success": true,
        "message": null
      }
    }
  }
  ```
</ResponseExample>

## FAQ

<Accordion title="Who can share a meeting?">
  <p>Only the meeting owner or a team admin (in the same team as the owner) can share a meeting.</p>
</Accordion>

<Accordion title="What happens if the user is already invited?">
  <p>The mutation returns `success: false` with a message indicating that the invitees are already invited.</p>
</Accordion>

<Accordion title="How many emails can I share with at once?">
  <p>You can share with up to 50 email addresses per request.</p>
</Accordion>

## Rate Limits

The `shareMeeting` mutation is rate-limited to **10 requests per hour** per user, in addition to the general API rate limits.

## Error Codes

List of possible error codes that may be returned by the `shareMeeting` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found">
  <p>The specified transcript could not be found or you do not have access to it.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>The user must be either the meeting owner or a team admin to share the meeting.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Revoke Shared Meeting Access" icon="link" href="/graphql-api/mutation/revoke-shared-meeting-access">
    Revoke shared access to a meeting
  </Card>

  <Card title="Transcript" icon="link" href="/graphql-api/query/transcript">
    Query transcript details including shared\_with
  </Card>
</CardGroup>
