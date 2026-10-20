<!-- Source: https://docs.fireflies.ai/graphql-api/query/bites.md -->
<!-- Title: Bites -->
<!-- Description: Querying list of bites -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Bites

> Querying list of bites

## Overview

The bites query is designed to fetch a list of bites against input arguments.

## Arguments

<ParamField path="mine" type="Boolean" required>
  The `mine` parameter, when set to true, fetches results specific to the owner of the API key
</ParamField>

<ParamField path="transcript_id" type="ID">
  You can use `transcript_id` to query all bites against a specific transcript.
</ParamField>

<ParamField path="my_team" type="Boolean">
  The `my_team` parameter, when set to true, fetches results for the owner of the API key
</ParamField>

<ParamField path="limit" type="Int">
  Maximum number of bites to fetch in a single query. Maximum of 50
</ParamField>

<ParamField path="skip" type="Int">
  Number of records to skip over. Helps paginate results when used in combination with the `limit`
  param.
</ParamField>

## Schema

Fields available to the [Bites](/schema/bite) query

## Usage Example

```graphql theme={null}
query Bites($mine: Boolean) {
  bites(mine: $mine) {
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
  	--data '{ "query": "query Bites($mine: Boolean) { bites(mine: $mine) { user_id name end_time } }", "variables": { "mine": true } }' \
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
    query: 'query Bites($mine: Boolean) { bites(mine: $mine) { user_id name end_time } }',
    variables: { mine: true }
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
  data = '{"query": "query Bites($mine: Boolean) { bites(mine: $mine) { user_id name end_time } }", "variables": {"mine": true }}'

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
          String jsonRequest = "{\"query\": \"query Bites($mine: Boolean) { bites(mine: $mine) { user_id name end_time } }\", \"variables\": {\"mine\": true}}";
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
      "bites": [
  		{
  			"user_id": "user-id",
  			"id": "bite-id",
      	},
  		{
  			"user_id": "user-id",
  			"id": "bite-id-2",
      	}
  	]	
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `bites` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="args_required">
  <p>You must provide at least one of the following arguments: `mine`, `transcript_id`, `my_team` to the bites query</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Bite" icon="link" href="/graphql-api/query/bite">
    Querying bite details
  </Card>

  <Card title="Create Bite" icon="link" href="/graphql-api/mutation/create-bite">
    Use the API to create a bite
  </Card>
</CardGroup>
