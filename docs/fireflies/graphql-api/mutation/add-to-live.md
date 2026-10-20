<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/add-to-live.md -->
<!-- Title: Add to Live -->
<!-- Description: Use the API to add the Fireflies.ai bot to an ongoing meeting -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Add to Live

> Use the API to add the Fireflies.ai bot to an ongoing meeting

## Overview

The `addToLiveMeeting` mutation allows you to add the Fireflies.ai bot to an ongoing meeting. It is rate limited to 3 requests per 20 minutes.

## Arguments

<ResponseField name="meeting_link" type="String!" required>
  A valid http URL for the meeting link, i.e. gooogle meet, zoom, etc
</ResponseField>

<ResponseField name="title" type="String">
  Title or name of the meeting, this will be used to identify the transcribed file. If title is not
  provided, a default title will be set automatically

  Maximum length is 256 characters.
</ResponseField>

<ResponseField name="meeting_password" type="String">
  Password for the meeting, if applicable.

  Maximum length is 32 characters.
</ResponseField>

<ResponseField name="duration" type="Int">
  Meeting duration in minutes. Defaults to 60 minutes if
  param is not provided

  Minimum is 15 and maximum is 120.
</ResponseField>

<ResponseField name="language" type="String">
  Language of the meeting. Defaults to English if not provided. For a complete list of language codes, please view [Language Codes](/miscellaneous/language-codes)

  Maximum length is 5 characters.
</ResponseField>

<ResponseField name="attendees" type="[Attendee]">
  Array of [Attendees](/schema/input/attendee) for expected meeting participants.
</ResponseField>

## Usage Example

To upload an audio file, provide the necessary input parameters to the mutation. Here's an example of how this mutation could be used:

```graphql theme={null}
mutation AddToLiveMeeting($meetingLink: String!) {
  addToLiveMeeting(meeting_link: $meetingLink) {
    success
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation AddToLiveMeeting($meetingLink: String!) { addToLiveMeeting(meeting_link: $meetingLink) { success } }",
      "variables": {
        "meetingLink": "https://meet.google.com/code-here"
      }
    }' \
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
    query: `  mutation AddToLiveMeeting($meetingLink: String!) {
  				addToLiveMeeting(meeting_link: $meetingLink) {
  					success
  				}
  			}
      `,
    variables: { meetingLink: 'https://meet.google.com/code-here' }
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
  		mutation AddToLiveMeeting($meetingLink: String!) {
  			addToLiveMeeting(meeting_link: $meetingLink) {
  				success
  			}
  		}
  	''',
  	'variables': {'meetingLink': 'https://meet.google.com/code-here'}
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:
      print(response.json())
  else:
      print(response.text)
  ```

  ```java java theme={null}
  import java.io.IOException;
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.net.http.HttpRequest.BodyPublishers;
  import java.net.http.HttpResponse.BodyHandlers;

  public class ApiRequest {
  	public static void main(String[] args) throws IOException, InterruptedException {
  		HttpClient client = HttpClient.newHttpClient();
          String jsonRequest = "{\"query\": \"mutation AddToLiveMeeting($meetingLink: String!) { addToLiveMeeting(meeting_link: $meetingLink) { success } }\", \"variables\": {\"meetingLink\": \"https://meet.google.com/code-here\"}";
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
      "addToLiveMeeting": {
        "success": true,
      }
    }
  }
  ```
</ResponseExample>

## FAQ

<Accordion title="Why am I getting a 'too_many_requests' error?">
  <p>The `addToLive` mutation has a limit of 3 requests per 20 minutes.</p>

  You may view API Rate limits [here](/fundamentals/limits).
</Accordion>

## Error Codes

List of possible error codes that may be returned by the `addToLiveMeeting` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="too_many_requests">
  <p>You have exceeded the rate limit for the `addToLiveMeeting` mutation. It is limited to 3 requests per 20 minutes. Please try again later.</p>
</Accordion>

<Accordion title="invalid_language_code">
  <p>The language code you provided is invalid. Please refer to the [Language Codes](/miscellaneous/language-codes) page for a list of valid language codes.</p>
</Accordion>

<Accordion title="unsupported_platform">
  <p>The meeting platform URL provided is not supported. Please use a supported meeting platform such as Zoom, Google Meet, Microsoft Teams, etc.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Upload Audio" icon="link" href="/graphql-api/mutation/upload-audio">
    Use the API to upload audio to Fireflies.ai
  </Card>

  <Card title="Webhooks" icon="link" href="/graphql-api/webhooks">
    Create notifications using webhooks
  </Card>
</CardGroup>
