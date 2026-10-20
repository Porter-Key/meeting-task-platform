<!-- Source: https://docs.fireflies.ai/graphql-api/query/user-groups.md -->
<!-- Title: UserGroups -->
<!-- Description: Querying user groups -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# UserGroups

> Querying user groups

## Overview

The user\_groups query is designed to fetch a list of all user groups within the team. This query allows you to retrieve information about user groups including their members.

## Arguments

<ParamField path="mine" type="Boolean">
  `mine` is an optional boolean argument. If set to `true`, returns only user groups that the
  current user belongs to. If not provided or set to `false`, returns all user groups in the team.
</ParamField>

## Schema

Fields available to the [UserGroup](/schema/user-groups) query

## Usage Example

```graphql theme={null}
query UserGroups($mine: Boolean) {
  user_groups(mine: $mine) {
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
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	--data '{ "query": "{ user_groups { name handle members { first_name last_name email } } }" }' \
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
    query: '{ user_groups { name handle members { first_name last_name email } } }'
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
  data = '{"query": "{ user_groups { name handle members { first_name last_name email } } }"}'

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
          String jsonRequest = "{\"query\": \"{ user_groups { name handle members { first_name last_name email } } }\"}";
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
      "user_groups": [
        {
          "id": "group_123",
          "name": "Engineering Team",
          "handle": "engineering",
          "members": [
            {
              "user_id": "user_456",
              "first_name": "John",
              "last_name": "Doe",
              "email": "john.doe@example.com"
            },
            {
              "user_id": "user_789",
              "first_name": "Jane",
              "last_name": "Smith",
              "email": "jane.smith@example.com"
            }
          ]
        },
        {
          "id": "group_124",
          "name": "Sales Team",
          "handle": "sales",
          "members": [
            {
              "user_id": "user_101",
              "first_name": "Bob",
              "last_name": "Johnson",
              "email": "bob.johnson@example.com"
            }
          ]
        }
      ]
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `user_groups` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="not_authorized">
  <p>You do not have permission to access user groups for this team.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Users" icon="link" href="/graphql-api/query/users">
    Querying list of users
  </Card>

  <Card title="User" icon="link" href="/graphql-api/query/user">
    Querying user details
  </Card>
</CardGroup>
