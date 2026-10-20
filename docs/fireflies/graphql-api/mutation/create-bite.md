<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/create-bite.md -->
<!-- Title: Create bite -->
<!-- Description: Use the API to create a bite -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create bite

> Use the API to create a bite

## Overview

The `createBite` mutation allows you to create a bite through the API.

## Arguments

<ParamField path="transcript_id" type="ID" required>
  ID of the transcript
</ParamField>

<ParamField path="name" type="String">
  Name of the bite

  Maximum length is 256 characters.
</ParamField>

<ParamField path="start_time" type="Float" required>
  Start time of the bite in seconds
</ParamField>

<ParamField path="end_time" type="Float" required>
  End time of the bite in seconds
</ParamField>

<ParamField path="media_type" type="String">
  Type of the bite, either 'video' or 'audio'
</ParamField>

<ParamField path="privacies" type="[String]">
  Array specifying the visibility of the Soundbite. Possible values are 'public', 'team', and
  'participants'. For example, \["team", "participants"] indicates visibility to both team members
  and participants, while \["public"] denotes full public access.
</ParamField>

<ParamField path="summary" type="String">
  Summary for the bite

  Maximum length is 500 characters.
</ParamField>

## Usage Example

To create a bite, provide the necessary input parameters to the mutation. Here's an example of how this mutation could be used:

```graphql theme={null}
mutation Mutation($transcriptId: ID!, $startTime: Float!, $endTime: Float!) {
  createBite(transcript_id: $transcriptId, start_time: $startTime, end_time: $endTime) {
    status
    name
    id
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST https://api.fireflies.ai/graphql \
  	-H "Content-Type: application/json" \
  	-H "Authorization: Bearer your_api_key" \
  	-d '{
  		"query": "mutation CreateBite($transcriptId: ID!, $startTime: Float!, $endTime: Float!) { createBite(transcript_id: $transcriptId, start_time: $startTime, end_time: $endTime) { summary status id } }",
  		"variables": {
  			"transcriptId": "your_transcript_id",
  			"startTime": 0,
  			"endTime": 5
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
    query: `mutation CreateBite($transcriptId: ID!, $startTime: Float!, $endTime: Float!) {
  			createBite(transcript_id: $transcriptId, start_time: $startTime, end_time: $endTime) {
  				summary
  				status
  				id
  			}
  		}`,
    variables: { transcriptId: 'your_transcript_id', startTime: 0, endTime: 5 }
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
       	mutation CreateBite($transcriptId: ID!, $startTime: Float!, $endTime: Float!) {
  			createBite(transcript_id: $transcriptId, start_time: $startTime, end_time: $endTime) {
  				summary
  				status
  				id
  			}
  		}
      ''',
      'variables': {
          'transcriptId': "your_transcript_id",
          'startTime': 0,
  		'endTime': 5
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
          String jsonRequest = "{\"query\": \"mutation CreateBite($transcriptId: ID!, $startTime: Float!, $endTime: Float!) { createBite(transcript_id: $transcriptId, start_time: $startTime, end_time: $endTime) { summary status id } }\", \"variables\": {\"transcriptId\": \"your_transcript_id\", \"startTime\": 0, \"endTime\": 5}}";
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
      "createBite": {
        "name": "bite-name",
        "status": "pending",
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

  <Card title="Bite" icon="link" href="/graphql-api/query/bite">
    Querying bite details
  </Card>
</CardGroup>
