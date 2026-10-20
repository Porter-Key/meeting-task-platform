<!-- Source: https://docs.fireflies.ai/graphql-api/query/channel.md -->
<!-- Title: Channel -->
<!-- Description: Querying channel details -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Channel

> Querying channel details

## Overview

The channel query is designed to fetch details of a specific channel by its ID. The user must have access to the channel (either it's a public channel in their team, or they are a member of the private channel).

## Arguments

<ParamField path="id" type="ID!" required>
  The unique identifier of the channel to fetch.
</ParamField>

## Schema

Fields available to the [Channel](/schema/channel) query

## Usage Example

```graphql theme={null}
query Channel($channelId: ID!) {
  channel(id: $channelId) {
    id
    title
    is_private
    created_by
    created_at
    updated_at
    members {
      user_id
      email
      name
    }
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_api_key" \
      --data '{ "query": "query Channel($channelId: ID!) { channel(id: $channelId) { id title is_private members { user_id email } } }", "variables": { "channelId": "your_channel_id" } }' \
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
    query: 'query Channel($channelId: ID!) { channel(id: $channelId) { id title is_private members { user_id email } } }',
    variables: { channelId: 'your_channel_id' }
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

  data = '{"query": "query Channel($channelId: ID!) { channel(id: $channelId) { id title is_private members { user_id email } } }", "variables": {"channelId": "your_channel_id"}}'

  response = requests.post(url, headers=headers, data=data)
  print(response.json())
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
          String jsonRequest = "{\"query\": \"query Channel($channelId: ID!) { channel(id: $channelId) { id title is_private members { user_id email } } }\", \"variables\": {\"channelId\": \"your_channel_id\"}}";
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
      "channel": {
        "id": "channel-id-1",
        "title": "Engineering",
        "is_private": false,
        "members": [
          {
            "user_id": "user-id-1",
            "email": "john@example.com",
            "name": "John Doe"
          },
          {
            "user_id": "user-id-2",
            "email": "jane@example.com",
            "name": "Jane Smith"
          }
        ]
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `channel` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found (Channel)">
  <p>The channel ID you are trying to query does not exist or you do not have access to it.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Channels" icon="link" href="/graphql-api/query/channels">
    Query list of channels
  </Card>

  <Card title="Channel Schema" icon="link" href="/schema/channel">
    Schema for Channel
  </Card>
</CardGroup>
