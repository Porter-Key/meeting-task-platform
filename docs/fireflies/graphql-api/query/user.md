<!-- Source: https://docs.fireflies.ai/graphql-api/query/user.md -->
<!-- Title: User -->
<!-- Description: Querying user details -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# User

> Querying user details

## Overview

The user query is designed to fetch details associated with a specific user id.

## Arguments

<ParamField path="id" type="String" />

<Note>
  `id` is an optional argument. Not passing an ID to this query will return user details for the
  owner of the API key
</Note>

## Schema

Fields available to the [User](/schema/user) query

## Usage Example

```graphql theme={null}
query User($userId: String!) {
  user(id: $userId) {
    user_id
    recent_transcript
    recent_meeting
    num_transcripts
    name
    minutes_consumed
    is_admin
    integrations
    email
    user_groups {
      id
      name
      handle
      members {
        user_id
        first_name
        last_name
        email
      }
    }
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	--data '{ "query": "query User($userId: String!) { user(id: $userId) { name integrations } }", "variables": { "userId": "your_user_id" } }' \
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
    query: 'query User($userId: String!) { user(id: $userId) { name integrations } }',
    variables: { userId: 'your_user_id' }
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
  data = '{"query": "query User($userId: String!) { user(id: $userId) { name integrations } }", "variables": {"userId": "your_user_id"}}'

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
          String jsonRequest = "{\"query\": \"query User($userId: String!) { user(id: $userId) { name integrations } }\", \"variables\": {\"userId\": \"your_user_id\"}}";
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
      "user": {
        "name": "Justin Fly",
        "integrations": ["string"],
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `user` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found (user)">
  <p>The user ID you are trying to query does not exist.</p>
</Accordion>

<Accordion title="not_in_team">
  <p>The user ID you are trying to query is not in your team.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Users" icon="link" href="/graphql-api/query/users">
    Querying list of users
  </Card>

  <Card title="UserGroups" icon="link" href="/graphql-api/query/user-groups">
    Querying user groups
  </Card>
</CardGroup>
