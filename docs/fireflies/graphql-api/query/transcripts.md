<!-- Source: https://docs.fireflies.ai/graphql-api/query/transcripts.md -->
<!-- Title: Transcripts -->
<!-- Description: Querying list of transcripts -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Transcripts

> Querying list of transcripts

## Overview

The transcripts query is designed to fetch a list of transcripts against input arguments.

## Arguments

<ParamField path="title" type="String">
  <b>This field is deprecated. Please use `keyword` instead.</b>

  Title of the transcript

  This argument is mutually exclusive with `keyword` field

  The maximum allowable length for this field is `256` characters.
</ParamField>

<ParamField path="keyword" type="String">
  Allows searching for keywords in meeting title and/or words spoken during the meeting

  This argument is mutually exclusive with `title` field

  The maximum allowable length for this field is `255` characters.
</ParamField>

<ParamField path="scope" type="TranscriptsQueryScope">
  Specify the scope for keyword search.

  If scope is provided, `keyword` becomes a required field

  Defaults to `TITLE` if no value is provided

  The available options for this field are:

  * `title`: Search within the title.
  * `sentences`: Search within the [sentences](/schema/sentence).
  * `all`: Search within title and sentences.
</ParamField>

<ParamField path="fromDate" type="DateTime">
  Return all transcripts created after `fromDate`. The `fromDate` parameter accepts a date-time
  string in the ISO 8601 format, specifically in the form `YYYY-MM-DDTHH:mm.sssZ`. For example, a
  valid timestamp would be `2024-07-08T22:13:46.660Z`.
</ParamField>

<ParamField path="toDate" type="DateTime">
  Return all transcripts created before `toDate`. The `toDate` parameter accepts a date-time string
  in the ISO 8601 format, specifically in the form `YYYY-MM-DDTHH:mm.sssZ`. For example, a valid
  timestamp would be `2024-07-08T22:13:46.660Z`.
</ParamField>

<ParamField path="date" type="Float">
  <b> This field is deprecated. Please use `fromDate` and `toDate` instead.</b>

  Return all transcripts created within the date specified. Query input value must be in milliseconds.
  For example, you can use the JavaScript `new Date().getTime()` to get the datetime in milliseconds
  which should look like this `1621292557453`. The timezone for this field is UTC +00:00

  For more details regarding time since [EPOCH](https://currentmillis.com/)
</ParamField>

<ParamField path="limit" type="Int">
  Number of transcripts to return. Maxiumum 50 in one query
</ParamField>

<ParamField path="skip" type="Int">
  Number of transcripts to skip.
</ParamField>

<ParamField path="host_email" type="String">
  Filter all meetings accordingly to meetings that have this email as the host.
</ParamField>

<ParamField path="organizer_email" type="String">
  <b>This field is deprecated. Please use `organizers` instead.</b>
  Filter meetings that have this email as the organizer.
</ParamField>

<ParamField path="participant_email" type="String">
  <b>This field is deprecated. Please use `participants` instead.</b>
  Filter meetings that contain this email as an attendee.
</ParamField>

<ParamField path="user_id" type="String">
  [User id](/schema/user). Filter all meetings that have this user ID as the organizer or participant.
</ParamField>

<ParamField path="mine" type="Boolean">
  Filter all meetings that have the API key owner as the organizer.
</ParamField>

<ParamField path="organizers" type="[String]">
  Filter meetings that have any of these emails as organizers. Accepts an array of email addresses.

  Cannot be combined with the deprecated `organizer_email` or `participant_email` fields.

  Each email must be valid and 256 characters or fewer.
</ParamField>

<ParamField path="participants" type="[String]">
  Filter meetings that contain any of these emails as attendees. Accepts an array of email addresses.

  Cannot be combined with the deprecated `organizer_email` or `participant_email` fields.

  Each email must be valid and 256 characters or fewer.
</ParamField>

<ParamField path="channel_id" type="String">
  Filter meetings that belong to a specific channel. Accepts a single channel ID.

  The channel ID must be a valid string and 256 characters or fewer.
</ParamField>

## Schema

Fields available to the [Transcript](/schema/transcript) query

## Usage Example

```graphql theme={null}
query Transcripts(
  $title: String
  $date: Float
  $limit: Int
  $skip: Int
  $hostEmail: String
  $participantEmail: String
  $organizers: [String]
  $participants: [String]
  $userId: String
  $channelId: String
) {
  transcripts(
    title: $title
    date: $date
    limit: $limit
    skip: $skip
    host_email: $hostEmail
    participant_email: $participantEmail
    organizers: $organizers
    participants: $participants
    user_id: $userId
    channel_id: $channelId
  ) {
    id
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
    speakers {
      id
      name
    }
    host_email
    organizer_email
    meeting_info {
      fred_joined
      silent_meeting
      summary_status
    }
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
      --data '{ "query": "query Transcripts($userId: String) { transcripts(user_id: $userId) { title id } }" }' \
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
    query: 'query Transcripts($userId: String) { transcripts(user_id: $userId) { title id } }',
    variables: { userId: 'your_user_id' }
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

  data = '{"query": "query Transcripts($userId: String) { transcripts(user_id: $userId) { title id } }", "variables": {"userId": "user_id"}}'

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
          String json = "{\"query\":\"query Transcripts { transcripts { title id } } \"}";
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
      "transcripts": [
  		{
  			"title": "Weekly sync",
  			"id": "transcript-id",
  		},
  		{
  			"title": "ClientMeeting.mp3",
  			"id": "transcript-id-2",
  		}
  	]
    }
  }
  ```
</ResponseExample>

## Error Codes

List of possible error codes that may be returned by the `transcripts` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="object_not_found (user)">
  <p>The user ID you are trying to query does not exist or you do not have access to it.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcript" icon="link" href="/graphql-api/query/transcript">
    Querying transcript details
  </Card>

  <Card title="Upload Audio" icon="link" href="/graphql-api/mutation/upload-audio">
    Use the API to upload audio to Fireflies.ai
  </Card>
</CardGroup>
