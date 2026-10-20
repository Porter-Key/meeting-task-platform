<!-- Source: https://docs.fireflies.ai/graphql-api/query/channels.md -->
<!-- Title: Channels -->
<!-- Description: Querying list of channels -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Channels

> Querying list of channels

## Overview

The channels query is designed to fetch a list of channels accessible to the authenticated user. This includes public channels in the user's team and private channels where the user is a member.

## Arguments

This query does not require any arguments.

## Schema

Fields available to the [Channel](/schema/channel) query

## Usage Example

```graphql theme={null}
query Channels {
  channels {
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
      --data '{ "query": "query Channels { channels { id title is_private members { user_id email } } }" }' \
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
    query: 'query Channels { channels { id title is_private members { user_id email } } }'
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

  data = '{"query": "query Channels { channels { id title is_private members { user_id email } } }"}'

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
          String json = "{\"query\":\"query Channels { channels { id title is_private members { user_id email } } }\"}";
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
      "channels": [
        {
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
        },
        {
          "id": "channel-id-2",
          "title": "Private Project",
          "is_private": true,
          "members": [
            {
              "user_id": "user-id-1",
              "email": "john@example.com",
              "name": "John Doe"
            }
          ]
        }
      ]
    }
  }
  ```
</ResponseExample>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Channel" icon="link" href="/graphql-api/query/channel">
    Query a single channel by ID
  </Card>

  <Card title="Channel Schema" icon="link" href="/schema/channel">
    Schema for Channel
  </Card>
</CardGroup>
