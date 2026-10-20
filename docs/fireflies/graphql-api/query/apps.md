<!-- Source: https://docs.fireflies.ai/graphql-api/query/apps.md -->
<!-- Title: AI Apps -->
<!-- Description: Querying list of AI App outputs -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AI Apps

> Querying list of AI App outputs

## Overview

The apps query fetches the results of the AI App for all the meetings it ran successfully.

## Arguments

<ParamField path="app_id" type="String">
  The `app_id` parameter retrieves all outputs against a specific AI App.
</ParamField>

<ParamField path="transcript_id" type="String">
  The `transcript_id` parameter retrieves all outputs against a specific meeting/transcript.
</ParamField>

<ParamField path="skip" type="Int">
  Number of records to skip over. Helps paginate results when used in combination with the `limit` param.
</ParamField>

<ParamField path="limit" type="Int">
  Maximum number of `apps` outputs to fetch in a single query. The default query fetches 10 records, which is the maximum for a single request.
</ParamField>

## Schema

Fields available to the [AI Apps](/schema/apps) query

## Usage Example

```graphql theme={null}
query GetAIAppsOutputs($appId: String, $transcriptId: String, $skip: Float, $limit: Float) {
  apps(app_id: $appId, transcript_id: $transcriptId, skip: $skip, limit: $limit) {
    outputs {
      transcript_id
      user_id
      app_id
      created_at
      title
      prompt
      response
    }
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_api_key" \
      --data '{ "query": "query GetAIAppsOutputs($transcriptId: String) { apps(transcript_id: $transcriptId) { outputs { transcript_id user_id app_id created_at title prompt response } } }", "variables": { "transcriptId": "your_transcript_id" } }' \
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
    query: 'query GetAIAppsOutputs($transcriptId: String) { apps(transcript_id: $transcriptId) { outputs { transcript_id user_id app_id created_at title prompt response } } }',
    variables: { transcriptId: 'your_transcript_id' }
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

  data = '{"query": "query GetAIAppsOutputs($transcriptId: String) { apps(transcript_id: $transcriptId) { outputs { transcript_id user_id app_id created_at title prompt response } } }", "variables": {"transcriptId": "transcript_id"}}'

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
          String json = "{\"query\":\"query GetAIAppsOutputs($transcriptId: String) { apps(transcript_id: $transcriptId) { outputs { transcript_id user_id app_id created_at title prompt response } } } \", \"variables\":{\"transcriptId\":\"transcript_id\"}}";
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
      "apps": [
  		{
  			"transcript_id": "transcript-id",
  			"user_id": "user-id",
  			"app_id": "app-id",
  			"title": "Weekly sync"
  		}
  	]
    }
  }
  ```
</ResponseExample>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcript" icon="link" href="/graphql-api/query/transcript">
    Querying transcript details
  </Card>

  <Card title="Transcripts" icon="link" href="/graphql-api/query/transcripts">
    Querying list of transcripts
  </Card>
</CardGroup>
