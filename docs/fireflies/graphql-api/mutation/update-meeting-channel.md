<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/update-meeting-channel.md -->
<!-- Title: Update Meeting Channel -->
<!-- Description: Use the API to update meeting channel assignments -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Update Meeting Channel

> Use the API to update meeting channel assignments

## Overview

The `updateMeetingChannel` mutation allows for batch updating the channel assignment of multiple meeting transcripts. This operation requires admin privileges within the team or ownership of the meetings. You can update 1–5 transcripts at once with all-or-nothing semantics—if any transcript fails validation, none are updated.

## Arguments

<ParamField path="input" type="UpdateMeetingChannelInput" required>
  The channel assignment to be applied to the specified transcripts. See [UpdateMeetingChannelInput](/schema/input/update-meeting-channel-input).
</ParamField>

## Usage Example

To update meeting channels, provide an array of transcript IDs (1–5 items) and a single channel ID as arguments to the mutation. Here's an example of how this mutation could be used:

```graphql theme={null}
mutation UpdateMeetingChannel($input: UpdateMeetingChannelInput!) {
  updateMeetingChannel(input: $input) {
    id
    title
    channels {
      id
    }
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	-d '{
  		"query": "mutation($input: UpdateMeetingChannelInput!) { updateMeetingChannel(input: $input) { id title channels { id } } }",
  		"variables": {
  			"input": {
  				"transcript_ids": ["transcript_id_1", "transcript_id_2"],
  				"channel_id": "channel_id"
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
      mutation($input: UpdateMeetingChannelInput!) {
        updateMeetingChannel(input: $input) {
          id
          title
          channels {
            id
          }
        }
      }
    `,
    variables: {
      input: {
        transcript_ids: ['transcript_id_1', 'transcript_id_2'],
        channel_id: 'channel_id'
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
      mutation($input: UpdateMeetingChannelInput!) {
        updateMeetingChannel(input: $input) {
          id
          title
          channels {
            id
          }
        }
      }
    `,
    'variables': {
      'input': {
        'transcript_ids': ['transcript_id_1', 'transcript_id_2'],
        'channel_id': 'channel_id'
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

  public class UpdateMeetingChannelExample {
      public static void main(String[] args) throws IOException, InterruptedException {
          HttpClient client = HttpClient.newHttpClient();

          String json = "{"
              + "\"query\":\"mutation($input: UpdateMeetingChannelInput!) { updateMeetingChannel(input: $input) { id title channels { id } } }\","
              + "\"variables\":{"
              + "\"input\":{"
              + "\"transcript_ids\":[\"transcript_id_1\",\"transcript_id_2\"],"
              + "\"channel_id\":\"channel_id\""
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
      "updateMeetingChannel": [
        {
          "id": "transcript_id_1",
          "title": "Weekly Sync",
          "channels": [
            {
              "id": "channel_id"
            }
          ]
        },
        {
          "id": "transcript_id_2",
          "title": "Product Review",
          "channels": [
            {
              "id": "channel_id"
            }
          ]
        }
      ]
    }
  }
  ```
</ResponseExample>

## FAQ

<Accordion title="Who has permission to update meeting channels?">
  <p>Only users with admin privileges or meeting owners can update meeting channels. All specified meetings must be owned by users in your team.</p>
</Accordion>

<Accordion title="How many transcripts can I update at once?">
  <p>You can update between 1 and 5 transcripts in a single mutation call. If you need to update more transcripts, make multiple mutation calls.</p>
</Accordion>

<Accordion title="What happens if the operation fails for one transcript?">
  <p>The mutation uses all-or-nothing semantics. If any transcript fails validation (not found, no access, or permission denied), none of the transcripts will be updated. All transcripts must pass validation for the update to succeed.</p>
</Accordion>

<Accordion title="Can a meeting belong to multiple channels?">
  <p>No, a meeting can only belong to one channel at a time. This mutation sets the meeting's channel to the specified value, replacing any previous channel assignment.</p>
</Accordion>

<Accordion title="Is the response order guaranteed to match the input order?">
  <p>No, the response order is not guaranteed to match the input order of transcript\_ids. If you need to correlate responses with inputs, use the id field in the response.</p>
</Accordion>

## Error Codes

List of possible error codes that may be returned by the `updateMeetingChannel` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="require_elevated_privilege">
  <p>The user must be either the meeting owner or a team admin to update meeting channels.</p>
</Accordion>

<Accordion title="object_not_found (transcript)">
  <p>One or more specified transcripts could not be found or you do not have access to them.</p>
</Accordion>

<Accordion title="invalid_arguments">
  <p>The input failed validation. Common causes include: empty transcript\_ids array, more than 5 transcript\_ids, or missing/empty channel\_id.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcript" icon="link" href="/graphql-api/query/transcript">
    Querying transcript details
  </Card>

  <Card title="Update Meeting Title" icon="link" href="/graphql-api/mutation/update-meeting-title">
    Update meeting titles
  </Card>

  <Card title="Update Meeting Privacy" icon="link" href="/graphql-api/mutation/update-meeting-privacy">
    Update meeting privacy
  </Card>

  <Card title="Transcripts" icon="link" href="/graphql-api/query/transcripts">
    Querying list of transcripts
  </Card>
</CardGroup>
