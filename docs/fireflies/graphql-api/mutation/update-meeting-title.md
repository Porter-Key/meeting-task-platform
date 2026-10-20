<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/update-meeting-title.md -->
<!-- Title: Update Meeting Title -->
<!-- Description: Use the API to update meeting titles -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Update Meeting Title

> Use the API to update meeting titles

## Overview

The `updateMeetingTitle` mutation allows for updating the title of a meeting transcript. This operation requires admin privileges within the team.

## Arguments

<ParamField path="input" type="UpdateMeetingTitleInput" required>
  The new title to be assigned to the meeting / transcript.
</ParamField>

## Usage Example

To update a meeting title, provide the transcript ID and the new title as arguments to the mutation. Here's an example of how this mutation could be used:

```graphql theme={null}
mutation UpdateMeetingTitle($input: UpdateMeetingTitleInput!) {
  updateMeetingTitle(input: $input) {
    title
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	-d '{
  		"query": "mutation($input: UpdateMeetingTitleInput!) { updateMeetingTitle(input: $input) { title } }",
  		"variables": {
  			"input": {
  				"id": "your_transcript_id",
  				"title": "New Title"
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
      mutation($input: UpdateMeetingTitleInput!) {
        updateMeetingTitle(input: $input) {
          title
        }
      }
    `,
    variables: {
      input: {
        id: 'your_transcript_id',
        title: 'New Title'
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
      mutation($input: UpdateMeetingTitleInput!) {
        updateMeetingTitle(input: $input) {
          title
        }
      }
    `,
    'variables': {
      'input': {
        'id': 'your_transcript_id',
        'title': 'New Title'
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

  public class UpdateMeetingTitleExample {
      public static void main(String[] args) throws IOException, InterruptedException {
          HttpClient client = HttpClient.newHttpClient();

          String json = "{"
              + "\"query\":\"mutation($input: UpdateMeetingTitleInput!) { updateMeetingTitle(input: $input) { title } }\","
              + "\"variables\":{"
              + "\"input\":{"
              + "\"id\":\"your_transcript_id\","
              + "\"title\":\"New Title\""
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
      "updateMeetingTitle": {
        "title": "New Title"
      }
    }
  }
  ```
</ResponseExample>

## FAQ

<Accordion title="Who has permission to update meeting titles?">
  <p>Only users with admin privileges can update meeting titles. The meeting owner also needs to be in your team.</p>
</Accordion>

## Error Codes

List of possible error codes that may be returned by the `updateMeetingTitle` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="require_elevated_privilege">
  <p>The user does not have admin privileges to update meeting titles.</p>
</Accordion>

<Accordion title="object_not_found (transcript)">
  <p>The specified transcript could not be found or you do not have access to it</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcript" icon="link" href="/graphql-api/query/transcript">
    Querying transcript details
  </Card>

  <Card title="Update Meeting Privacy" icon="link" href="/graphql-api/mutation/update-meeting-privacy">
    Update meeting privacy
  </Card>
</CardGroup>
