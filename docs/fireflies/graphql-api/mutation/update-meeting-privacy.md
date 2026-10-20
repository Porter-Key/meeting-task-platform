<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/update-meeting-privacy.md -->
<!-- Title: Update Meeting Privacy -->
<!-- Description: Use the API to update meeting privacy settings -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Update Meeting Privacy

> Use the API to update meeting privacy settings

## Overview

The `updateMeetingPrivacy` mutation allows for updating the privacy setting of a meeting transcript. This operation requires admin privileges within the team or ownership of the meeting.

## Arguments

<ParamField path="input" type="UpdateMeetingPrivacyInput" required>
  The privacy setting to be assigned to the meeting / transcript. See [UpdateMeetingPrivacyInput](/schema/input/update-meeting-privacy-input).
</ParamField>

## Usage Example

To update a meeting's privacy setting, provide the transcript ID and the new privacy level as arguments to the mutation. Here's an example of how this mutation could be used:

```graphql theme={null}
mutation UpdateMeetingPrivacy($input: UpdateMeetingPrivacyInput!) {
  updateMeetingPrivacy(input: $input) {
    id
    title
    privacy
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	-d '{
  		"query": "mutation($input: UpdateMeetingPrivacyInput!) { updateMeetingPrivacy(input: $input) { id title privacy } }",
  		"variables": {
  			"input": {
  				"id": "your_transcript_id",
  				"privacy": "teammates"
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
      mutation($input: UpdateMeetingPrivacyInput!) {
        updateMeetingPrivacy(input: $input) {
          id
          title
          privacy
        }
      }
    `,
    variables: {
      input: {
        id: 'your_transcript_id',
        privacy: 'teammates'
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
    'query': `
      mutation($input: UpdateMeetingPrivacyInput!) {
        updateMeetingPrivacy(input: $input) {
          id
          title
          privacy
        }
      }
    `,
    'variables': {
      'input': {
        'id': 'your_transcript_id',
        'privacy': 'teammates'
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
  import java.net.http.HttpResponse.BodyHandlers;

  public class UpdateMeetingPrivacyExample {
      public static void main(String[] args) throws IOException, InterruptedException {
          HttpClient client = HttpClient.newHttpClient();

          String json = "{"
              + "\"query\":\"mutation($input: UpdateMeetingPrivacyInput!) { updateMeetingPrivacy(input: $input) { id title privacy } }\","
              + "\"variables\":{"
              + "\"input\":{"
              + "\"id\":\"your_transcript_id\","
              + "\"privacy\":\"teammates\""
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
      "updateMeetingPrivacy": {
        "id": "your_transcript_id",
        "title": "Meeting Title",
        "privacy": "teammates"
      }
    }
  }
  ```
</ResponseExample>

## FAQ

<Accordion title="Who has permission to update meeting privacy?">
  <p>Only users with admin privileges or meeting owners can update meeting privacy settings. The meeting owner also needs to be in your team.</p>
</Accordion>

<Accordion title="What privacy levels are available?">
  <p>Available privacy levels are: link (anyone with link), owner (meeting owner only), participants (meeting participants only), teammatesandparticipants (teammates and participants), teammates (teammates only).</p>
</Accordion>

## Error Codes

List of possible error codes that may be returned by the `updateMeetingPrivacy` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="require_elevated_privilege">
  <p>The user must be either the meeting owner or a team admin to update meeting privacy.</p>
</Accordion>

<Accordion title="object_not_found (transcript)">
  <p>The specified transcript could not be found or you do not have access to it</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcript" icon="link" href="/graphql-api/query/transcript">
    Querying transcript details
  </Card>

  <Card title="Update Meeting Title" icon="link" href="/graphql-api/mutation/update-meeting-title">
    Use the API to update meeting titles
  </Card>
</CardGroup>
