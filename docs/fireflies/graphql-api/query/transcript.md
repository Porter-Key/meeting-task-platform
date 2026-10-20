<!-- Source: https://docs.fireflies.ai/graphql-api/query/transcript.md -->
<!-- Title: Transcript -->
<!-- Description: Querying transcript details -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Transcript

> Querying transcript details

## Overview

The transcript query is designed to fetch details associated with a specific transcript ID.

## Arguments

<ParamField path="id" type="String" required />

## Schema

Fields available to the [Transcript](/schema/transcript) query

## Usage Example

```graphql theme={null}
query Transcript($transcriptId: String!) {
  transcript(id: $transcriptId) {
    id
    dateString
    privacy
    analytics {
      sentiments {
        negative_pct
        neutral_pct
        positive_pct
      }
      categories {
        questions
        date_times
        metrics
        tasks
      }
      speakers {
        speaker_id
        name
        duration
        word_count
        longest_monologue
        monologues_count
        filler_words
        questions
        duration_pct
        words_per_minute
      }
    }
    speakers {
      id
      name
    }
    sentences {
      index
      speaker_name
      speaker_id
      text
      raw_text
      start_time
      end_time
      ai_filters {
        task
        pricing
        metric
        question
        date_and_time
        text_cleanup
        sentiment
      }
    }
    title
    host_email
    organizer_email
    calendar_id
    user {
      user_id
      email
      name
      num_transcripts
      recent_meeting
      minutes_consumed
      is_admin
      integrations
    }
    fireflies_users
    participants
    date
    transcript_url
    audio_url
    video_url
    duration
    meeting_attendees {
      displayName
      email
      phoneNumber
      name
      location
    }
    meeting_attendance {
      name
      join_time
      leave_time
    }
    summary {
      keywords
      action_items
      outline
      shorthand_bullet
      overview
      bullet_gist
      gist
      short_summary
      short_overview
      meeting_type
      topics_discussed
      transcript_chapters
    }
    cal_id
    calendar_type
    meeting_info {
      fred_joined
      silent_meeting
      summary_status
    }
    apps_preview {
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
    meeting_link
    is_live
    channels {
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
  	--data '{ "query": "query Transcript($transcriptId: String!) { transcript(id: $transcriptId) { title id } }", "variables": { "transcriptId": "your_transcript_id" } }' \
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
    query: 'query Transcript($transcriptId: String!) { transcript(id: $transcriptId) { title id } }',
    variables: { transcriptId: 'your_transcript_id' }
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
  data = '{"query": "query Transcript($transcriptId: String!) { transcript(id: $transcriptId) { title id } }", "variables": {"transcriptId": "your_transcript_id"}}'

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
          String jsonRequest = "{\"query\": \"query Transcript($transcriptId: String!) { transcript(id: $transcriptId) { title id } }\", \"variables\": {\"transcriptId\": \"your_transcript_id\"}}";
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
      "transcript": {
        "title": "Weekly sync",
        "id": "transcript-id",
      }
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `transcript` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found (transcript)">
  <p>The transcript ID you are trying to query does not exist or you do not have access to it.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcripts" icon="link" href="/graphql-api/query/transcripts">
    Querying list of transcripts
  </Card>

  <Card title="Update Meeting Title" icon="link" href="/graphql-api/mutation/update-meeting-title">
    Use the API to update meeting titles
  </Card>
</CardGroup>
