<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/set-user-role.md -->
<!-- Title: Set User Role -->
<!-- Description: Use the API to set user roles -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Set User Role

> Use the API to set user roles

## Overview

The `setUserRole` mutation allows for the updating of a user's role within a team.

## Arguments

<ParamField path="user_id" type="String" required>
  The unique identifier of the user.
</ParamField>

<ParamField path="role" type="Role" required>
  The [Role](/schema/input/role) to be assigned to the user. Valid types for user are `admin` and
  `user`
</ParamField>

## Usage Example

To set a user's role, provide the user's ID and the desired role as arguments to the mutation. Here's an example of how this mutation could be used:

```graphql theme={null}
mutation setUserRole($userId: String!, $role: Role!) {
  setUserRole(user_id: $userId, role: $role) {
    id
    name
    email
    role
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	-d '{
  		"query": "mutation($user_id: String!, $role: Role!) { setUserRole(user_id: $user_id, role:$role) { name is_admin } }",
  		"variables": {
  			"user_id": "your_user_id",
  			"role": "admin"
  		}
  	}'
  ```

  ```javascript javascript theme={null}
  const axios = require('axios');

  const url = 'https://api.fireflies.ai/graphql';
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer your_api_key'
  };

  const data = {
    query: `mutation Mutation($userId: String!, $role: Role!) {
  		setUserRole(user_id: $userId, role: $role) {
  		  name
  		  is_admin
  		}
  	  }`,
    variables: { userId: 'your_user_id', role: 'admin' }
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
        mutation($user_id: String!, $role: Role!) {
          setUserRole(user_id: $user_id, role:$role) {
            name
            is_admin
          }
        }
      ''',
      'variables': {
          'user_id': "your_user_id",
          'role': "admin"
      }
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:
      print(response.json()['data'])
  else:
      print(response.text)
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
          String jsonRequest = "{\"query\": \"mutation SetUserRole($user_id: String!, $role: Role!) { setUserRole(user_id: $user_id, role: $role) { name is_admin } }\", \"variables\": {\"user_id\": \"your_user_id\", \"role\": \"admin\"}}";
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
      "setUserRole": {
        "name": "Justin Fly",
        "is_admin": "true",
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `setUserRole` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found (team)">
  <p>This may indicate that you are not a part of any team. Please contact support if you encounter this error</p>
</Accordion>

<Accordion title="not_in_team">
  <p>The user ID you are trying to query is not in your team.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>The user does not have admin privileges to set the user role.</p>
</Accordion>

<Accordion title="admin_must_exist">
  <p>The team must have at least one admin. Please add an admin to the team or contact support if you encounter this error.</p>
</Accordion>

<Accordion title="invalid_args">
  <p>An invalid argument was provided to the mutation for the `role` field. Please check the arguments you are providing and try again.</p>
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
