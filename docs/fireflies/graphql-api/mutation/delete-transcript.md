<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/delete-transcript.md -->
<!-- Title: Delete Transcript -->
<!-- Description: Use the API to manage transcript deletion -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete Transcript

> Use the API to manage transcript deletion

## Overview

The `deleteTranscript` mutation is designed to delete a specific transcript by its ID.

<Note>
  **Rate Limit:** This mutation is rate-limited to 10 requests per minute across all user tiers. If you exceed this limit, you will receive a `too_many_requests` error with a `retryAfter` timestamp indicating when you can make requests again.
</Note>

## Arguments

<ParamField path="id" type="String" required>
  Transcript ID
</ParamField>

## Usage Example

To delete a transcript, provide the unique id of the transcript as an argument to the mutation. The returned subfields will be from the deleted transcript. Here’s an example of how this mutation could be used:

```graphql theme={null}
mutation deleteTranscript($id: String!) {
  deleteTranscript(id: $id) {
    id
    title
    host_email
    organizer_email
    fireflies_users
    participants
    date
    transcript_url
    audio_url
    duration
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{"query": "mutation($transcriptId: String!) { deleteTranscript(id: $transcriptId) { title date duration organizer_email } }", "variables": {"transcriptId": "your_transcript_id"}}' \
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
    query: `
        mutation($transcriptId: String!) {
          deleteTranscript(id: $transcriptId) {
            title
            date
            duration
            organizer_email
          }
        }
      `,
    variables: { transcriptId: 'transcript_id' }
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
          mutation($transcriptId: String!) {
            deleteTranscript(id: $transcriptId) {
              title
              date
              duration
              organizer_email
            }
          }
      ''',
      'variables': {'transcriptId': 'your_transcript_id'}
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:
      print(response.json())
  else:
      print(response.text)


  ```

  ```java java theme={null}
  import java.io.IOException;
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.net.http.HttpRequest.BodyPublishers;
  import java.net.http.HttpResponse.BodyHandlers;

  public class ApiRequest {
      public static void main(String[] args) throws IOException, InterruptedException {
          HttpClient client = HttpClient.newHttpClient();

          String json = "{\"query\":\"mutation($transcriptId: String!) { deleteTranscript(id: $transcriptId) { title date duration organizer_email } }\",\"variables\":{\"transcriptId\":\"your_transcript_id\"}}";
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
      "deleteTranscript": {
        "duration": "1",
        "date": 1699570138000,
        "organizer_email": "justin@fly.ai",
        "title": "Video title"
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `deleteTranscript` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="require_elevated_privilege">
  <p>The user does not have admin privileges to delete the transcript.</p>
</Accordion>

<Accordion title="too_many_requests">
  <p>You have exceeded the rate limit of 10 requests per minute. Wait until the time specified in the `retryAfter` field before making additional requests.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcripts" icon="link" href="/graphql-api/query/transcripts">
    Querying list of transcripts
  </Card>

  <Card title="Update Meeting Privacy" icon="link" href="/graphql-api/mutation/update-meeting-privacy">
    Update meeting privacy
  </Card>
</CardGroup>
