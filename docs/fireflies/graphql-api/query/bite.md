<!-- Source: https://docs.fireflies.ai/graphql-api/query/bite.md -->
<!-- Title: Bite -->
<!-- Description: Querying bite details -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Bite

> Querying bite details

## Overview

The bite query is designed to fetch details associated with a specific bite ID.

## Arguments

<ParamField path="id" type="ID" required>
  Unique identifier of the bite
</ParamField>

## Schema

Fields available to the [Bite](/schema/bite) query

## Usage Example

```graphql theme={null}
query Bite($biteId: ID!) {
  bite(id: $biteId) {
    transcript_id
    name
    id
    thumbnail
    preview
    status
    summary
    user_id
    start_time
    end_time
    summary_status
    media_type
    created_at
    created_from {
      description
      duration
      id
      name
      type
    }
    captions {
      end_time
      index
      speaker_id
      speaker_name
      start_time
      text
    }
    sources {
      src
      type
    }
    privacies
    user {
      first_name
      last_name
      picture
      name
      id
    }
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	--data '{ "query": "query Bite($biteId: ID!) { bite(id: $biteId) { user_id name status summary } }", "variables": { "biteId": "your_bite_id" } }' \
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
    query: 'query Bite($biteId: ID!) { bite(id: $biteId) { user_id name status summary } }',
    variables: { biteId: 'your_bite_id' }
  };

  axios
    .post(url, data, { headers: headers })
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  ```

  ```python python theme={null}
  import requests

  url = 'https://api.fireflies.ai/graphql'
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
  }
  data = '{"query": "query Bite($biteId: ID!) { bite(id: $biteId) { user_id name status summary } }", "variables": {"biteId": "your_bite_id"}}'

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
          String jsonRequest = "{\"query\": \"query Bite($biteId: ID!) { bite(id: $biteId) { user_id name status summary } }\", \"variables\": {\"biteId\": \"your_bite_id\"}}";
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
      "bite": {
        "user_id": "user-id",
        "id": "bite-id",
      }
    }
  }
  ```
</ResponseExample>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Bites" icon="link" href="/graphql-api/query/bites">
    Querying list of bites
  </Card>

  <Card title="Create Bite" icon="link" href="/graphql-api/mutation/create-bite">
    Use the API to create a bite
  </Card>
</CardGroup>
