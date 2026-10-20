<!-- Source: https://docs.fireflies.ai/graphql-api/query/analytics.md -->
<!-- Title: Analytics -->
<!-- Description: Querying conversation and meeting analytics for teams and users -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Analytics

> Querying conversation and meeting analytics for teams and users

## Overview

The analytics query fetches detailed conversation and meeting metrics for teams and users across a specified date range.

## Arguments

<ParamField path="start_time" type="String">
  The `start_time` parameter filters results starting from a specific datetime (ISO 8601 format).
</ParamField>

<ParamField path="end_time" type="String">
  The `end_time` parameter filters results up to a specific datetime (ISO 8601 format).
</ParamField>

## Schema

Fields available to the [Analytics](/schema/analytics) query.

## Usage Example

```graphql theme={null}
query Analytics($startTime: String, $endTime: String) {
  analytics(start_time: $startTime, end_time: $endTime) {
    team {
      conversation {
        average_filler_words
        average_filler_words_diff_pct
        average_monologues_count
        average_monologues_count_diff_pct
        average_questions
        average_questions_diff_pct
        average_sentiments {
          negative_pct
          neutral_pct
          positive_pct
        }
        average_silence_duration
        average_silence_duration_diff_pct
        average_talk_listen_ratio
        average_words_per_minute
        longest_monologue_duration_sec
        longest_monologue_duration_diff_pct
        total_filler_words
        total_filler_words_diff_pct
        total_meeting_notes_count
        total_meetings_count
        total_monologues_count
        total_monologues_diff_pct
        teammates_count
        total_questions
        total_questions_diff_pct
        total_silence_duration
        total_silence_duration_diff_pct
      }
      meeting {
        count
        count_diff_pct
        duration
        duration_diff_pct
        average_count
        average_count_diff_pct
        average_duration
        average_duration_diff_pct
      }
    }
    users {
      user_id
      user_name
      user_email
      conversation {
        talk_listen_pct
        talk_listen_ratio
        total_silence_duration
        total_silence_duration_compare_to
        total_silence_pct
        total_silence_ratio
        total_speak_duration
        total_speak_duration_with_user
        total_word_count
        user_filler_words
        user_filler_words_compare_to
        user_filler_words_diff_pct
        user_longest_monologue_sec
        user_longest_monologue_compare_to
        user_longest_monologue_diff_pct
        user_monologues_count
        user_monologues_count_compare_to
        user_monologues_count_diff_pct
        user_questions
        user_questions_compare_to
        user_questions_diff_pct
        user_speak_duration
        user_word_count
        user_words_per_minute
        user_words_per_minute_compare_to
        user_words_per_minute_diff_pct
      }
      meeting {
        count
        count_diff
        count_diff_compared_to
        count_diff_pct
        duration
        duration_diff
        duration_diff_compared_to
        duration_diff_pct
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
      --data '{ "query": "query Analytics($startTime: String, $endTime: String) { analytics(start_time: $startTime, end_time: $endTime) { team { conversation { average_filler_words } } } }", "variables": { "startTime": "2024-01-01T00:00:00Z", "endTime": "2024-01-31T23:59:59Z" } }' \
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
    query:
      'query Analytics($startTime: String, $endTime: String) { analytics(start_time: $startTime, end_time: $endTime) { team { conversation { average_filler_words } } } }',
    variables: { startTime: '2024-01-01T00:00:00Z', endTime: '2024-01-31T23:59:59Z' }
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

  data = '{"query": "query Analytics($startTime: String, $endTime: String) { analytics(start_time: $startTime, end_time: $endTime) { team { conversation { average_filler_words } } } }", "variables": {"startTime": "2024-01-01T00:00:00Z", "endTime": "2024-01-31T23:59:59Z"}}'

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
          String json = "{\"query\":\"query Analytics($startTime: String, $endTime: String) { analytics(start_time: $startTime, end_time: $endTime) { team { conversation { average_filler_words } } } }\", \"variables\":{\"startTime\":\"2024-01-01T00:00:00Z\", \"endTime\":\"2024-01-31T23:59:59Z\"}}";
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
      "analytics": {
        "team": {
          "conversation": {
            "average_filler_words": 15
          }
        }
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `analytics` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="paid_required (business_or_higher)">
  <p>You need to be on a Business or higher plan to query analytics.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>The user does not have admin privileges to view analytics for team.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcripts" icon="link" href="/graphql-api/query/transcripts">
    Querying list of transcripts
  </Card>

  <Card title="Users" icon="link" href="/graphql-api/query/users">
    Querying list of users
  </Card>
</CardGroup>
