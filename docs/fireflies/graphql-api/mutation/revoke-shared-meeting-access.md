<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/revoke-shared-meeting-access.md -->
<!-- Title: Revoke Shared Meeting Access -->
<!-- Description: Use the API to revoke shared access to a meeting transcript -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Revoke Shared Meeting Access

> Use the API to revoke shared access to a meeting transcript

## Overview

The `revokeSharedMeetingAccess` mutation revokes a previously shared user's access to a meeting transcript.

## Arguments

<ParamField path="input" type="RevokeSharedMeetingAccessInput" required>
  The revocation details. See [RevokeSharedMeetingAccessInput](/schema/input/revoke-shared-meeting-access-input).
</ParamField>

## Usage Example

To revoke shared access, provide the meeting ID and the email address of the user whose access you want to revoke.

```graphql theme={null}
mutation RevokeSharedMeetingAccess($input: RevokeSharedMeetingAccessInput!) {
  revokeSharedMeetingAccess(input: $input) {
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
  		"query": "mutation($input: RevokeSharedMeetingAccessInput!) { revokeSharedMeetingAccess(input: $input) { success message } }",
  		"variables": {
  			"input": {
  				"meeting_id": "your_meeting_id",
  				"email": "user@example.com"
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
      mutation($input: RevokeSharedMeetingAccessInput!) {
        revokeSharedMeetingAccess(input: $input) {
          success
          message
        }
      }
    `,
    variables: {
      input: {
        meeting_id: 'your_meeting_id',
        email: 'user@example.com'
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
      mutation($input: RevokeSharedMeetingAccessInput!) {
        revokeSharedMeetingAccess(input: $input) {
          success
          message
        }
      }
    ''',
    'variables': {
      'input': {
        'meeting_id': 'your_meeting_id',
        'email': 'user@example.com'
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

  public class RevokeSharedMeetingAccessExample {
      public static void main(String[] args) throws IOException, InterruptedException {
          HttpClient client = HttpClient.newHttpClient();

          String json = "{"
              + "\"query\":\"mutation($input: RevokeSharedMeetingAccessInput!) { revokeSharedMeetingAccess(input: $input) { success message } }\","
              + "\"variables\":{"
              + "\"input\":{"
              + "\"meeting_id\":\"your_meeting_id\","
              + "\"email\":\"user@example.com\""
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
      "revokeSharedMeetingAccess": {
        "success": true,
        "message": "Revoked meeting access"
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `revokeSharedMeetingAccess` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found (transcript)">
  <p>The specified transcript could not be found or you do not have access to it.</p>
</Accordion>

<Accordion title="object_not_found (shared meeting access)">
  <p>The specified email does not have shared access to this meeting.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>The user must be either the meeting owner or a team admin to revoke shared access.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Share Meeting" icon="link" href="/graphql-api/mutation/share-meeting">
    Share a meeting with external users
  </Card>

  <Card title="Transcript" icon="link" href="/graphql-api/query/transcript">
    Query transcript details including shared\_with
  </Card>
</CardGroup>
