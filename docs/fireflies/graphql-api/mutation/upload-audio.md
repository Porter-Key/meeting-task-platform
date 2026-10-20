<!-- Source: https://docs.fireflies.ai/graphql-api/mutation/upload-audio.md -->
<!-- Title: Upload Audio -->
<!-- Description: Use the API to upload audio to Fireflies.ai -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Upload Audio

> Use the API to upload audio to Fireflies.ai

## Overview

The `uploadAudio` mutation allows you to upload audio files to Fireflies.ai for transcription.

## Arguments

<ParamField path="input" type="AudioUploadInput">
  <Expandable>
    <ResponseField name="url" type="String" required>
      The url of media file to be transcribed. It MUST be a valid https string and publicly accessible to enable us download the audio / video file. Double check to see if the media file is downloadable and that the link is not a preview link before making the request. The media file must be either of these formats - mp3, mp4, wav, m4a, ogg
    </ResponseField>

    <ResponseField name="title" type="String">
      Title or name of the meeting, this will be used to identify the transcribed file
    </ResponseField>

    <ResponseField name="webhook" type="String">
      URL for the webhook that receives notifications when transcription completes
    </ResponseField>

    <ResponseField name="custom_language" type="String">
      Specify a custom language code for your meeting, e.g. `es` for Spanish or `de` for German. For a complete list of language codes, please view [Language Codes](/miscellaneous/language-codes)
    </ResponseField>

    <ResponseField name="save_video" type="Boolean">
      Specify whether the video should be saved or not.
    </ResponseField>

    <ResponseField name="attendees" type="[Attendees]">
      An array of objects containing meeting [Attendees](#). This is relevant if you have active integrations like Salesforce, Hubspot etc. Fireflies uses the attendees value to push meeting notes to your active CRM integrations where notes are added to an existing contact or a new contact is created. Each object contains -

      * displayName
      * email
      * phoneNumber
    </ResponseField>

    <ResponseField name="client_reference_id" type="String">
      Custom identifier set by the user during upload. You may use this to identify your uploads in your webhook
      events.
    </ResponseField>

    <ResponseField name="bypass_size_check" type="Boolean">
      Bypasses the internal file size validation that normally rejects audio files smaller than 50kb. Set to true if you need to process very short audio clips.
    </ResponseField>

    <ResponseField name="download_auth" type="DownloadAuthInput">
      Authentication configuration for downloading the media file. Use this when your audio/video file requires authentication (bearer token or basic auth). If not provided, defaults to no authentication (publicly accessible URL). See [DownloadAuthInput](/schema/input/download-auth-input) for details.
    </ResponseField>
  </Expandable>
</ParamField>

## Usage Example

To upload a file, provide the necessary input parameters to the mutation. Here's an example of how this mutation could be used:

```graphql theme={null}
mutation uploadAudio($input: AudioUploadInput) {
  uploadAudio(input: $input) {
    success
    title
    message
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation($input: AudioUploadInput) { uploadAudio(input: $input) { success title message } }",
      "variables": {
        "input": {
          "url": "https://url-to-the-audio-file",
          "title": "title of the file",
          "attendees": [
            {
              "displayName": "Fireflies Notetaker",
              "email": "notetaker@fireflies.ai",
              "phoneNumber": "xxxxxxxxxxxxxxxx"
            },
            {
              "displayName": "Fireflies Notetaker 2",
              "email": "notetaker2@fireflies.ai",
              "phoneNumber": "xxxxxxxxxxxxxxxx"
            }
          ]
        }
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

  const input = {
    url: 'https://url-to-the-audio-file',
    title: 'title of the file',
    attendees: [
      {
        displayName: 'Fireflies Notetaker',
        email: 'notetaker@fireflies.ai',
        phoneNumber: 'xxxxxxxxxxxxxxxx'
      },
      {
        displayName: 'Fireflies Notetaker 2',
        email: 'notetaker2@fireflies.ai',
        phoneNumber: 'xxxxxxxxxxxxxxxx'
      }
    ]
  };
  const data = {
    query: `       mutation($input: AudioUploadInput) {
          uploadAudio(input: $input) {
            success
            title
            message
          }
        }
      `,
    variables: { input }
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

  input_data = {
  	"url": "https://url_for_audio_file",
  	"title": "title of the file",
  	"attendees": [
  		{
  			"displayName": "Fireflies Notetaker",
  			"email": "notetaker@fireflies.ai",
  			"phoneNumber": "xxxxxxxxxxxxxxxx"
  		},
  		{
  			"displayName": "Fireflies Notetaker 2",
  			"email": "notetaker2@fireflies.ai",
  			"phoneNumber": "xxxxxxxxxxxxxxxx"
  		}
  	]}

  data = {
  	'query': '''
  		mutation($input: AudioUploadInput) {
  			uploadAudio(input: $input) {
  				success
  				title
  				message
  			}
  		}
  	''',
  	'variables': {'input': input_data}
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

  	String json = "{"
  		+ "\"query\":\"mutation($input: AudioUploadInput) { uploadAudio(input: $input) { success title message } }\","
  		+ "\"variables\":{"
  		+ "\"input\": {"
  			+ "\"url\":\"https://url_for_audio_file.com\","
  			+ "\"title\":\"title of the file\","
  			+ "\"attendees\":["
  			+ "{"
  				+ "\"displayName\": \"Fireflies Notetaker\","
  				+ "\"email\": \"notetaker@fireflies.ai\","
  				+ "\"phoneNumber\": \"xxxxxxxxxxxxxxxx\""
  			+ "},"
  			+ "{"
  				+ "\"displayName\": \"Fireflies Notetaker 2\","
  				+ "\"email\": \"notetaker2@fireflies.ai\","
  				+ "\"phoneNumber\": \"xxxxxxxxxxxxxxxx\""
  			+ "}"
  			+ "]"
  		+ "}"
  		+ "}"
  	+ "}";


  	HttpRequest request = HttpRequest.newBuilder()
  			.uri(URI.create("https://api.fireflies.ai/graphql"))
  			.header("Content-Type", "application/json")
  			.header("Authorization", "Bearer your_api_key")
  			.POST(BodyPublishers.ofString(json))
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
      "uploadAudio": {
        "success": true,
        "title": "title of the file",
        "message": "Uploaded audio has been queued for processing."
      }
    }
  }
  ```
</ResponseExample>

## Authenticated Downloads

The `download_auth` field allows you to upload audio/video files that require authentication. This is useful when your media files are hosted on private servers or behind authentication.

### Bearer Token Authentication

Use bearer token authentication when your media URL requires an `Authorization: Bearer <token>` header:

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://example.com/protected-audio.mp3"
    title: "Protected Meeting Recording"
    download_auth: {
      type: bearer_token
      bearer: {
        token: "your-bearer-token-here"
      }
    }
  }) {
    success
    message
  }
}
```

### Basic Authentication

Use basic authentication when your media URL requires username and password:

```graphql theme={null}
mutation {
  uploadAudio(input: {
    url: "https://example.com/protected-audio.mp3"
    title: "Protected Meeting Recording"
    download_auth: {
      type: basic_auth
      basic: {
        username: "your-username"
        password: "your-password"
      }
    }
  }) {
    success
    message
  }
}
```

**Note:** The username is optional for basic auth. If not provided, only the password will be used.

## FAQ

<Accordion title="Can I upload a file directly from my machine?">
  <p>Audio upload only works with publicly accessible URLs or URLs with supported authentication (bearer token or basic auth). We cannot accept files hosted on your local machine.</p>
</Accordion>

<Accordion title="I don't want to expose my audio files to the public internet. How can I upload them to Fireflies.ai safely?">
  <p>You have two options:</p>

  <ol>
    <li><strong>Signed URLs:</strong> Use signed URLs with short expiry times (e.g., AWS S3 presigned URLs, Google Cloud Storage signed URLs)</li>
    <li><strong>Authenticated Downloads:</strong> Use the <code>download\_auth</code> field to provide bearer token or basic authentication credentials. Fireflies will use these credentials when downloading your media file.</li>
  </ol>
</Accordion>

<Accordion title="What authentication methods are supported?">
  <p>Fireflies supports two authentication methods for downloading media files:</p>

  <ul>
    <li><strong>Bearer Token:</strong> Adds <code>Authorization: Bearer \<token></code> header when downloading</li>
    <li><strong>Basic Auth:</strong> Adds <code>Authorization: Basic \<base64(username:password)></code> header when downloading</li>
  </ul>

  <p>If your media file is publicly accessible, you don't need to provide <code>download\_auth</code>.</p>
</Accordion>

## Error Codes

List of possible error codes that may be returned by the `uploadAudio` mutation. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="paid_required (pro_or_higher)">
  <p>You may receieve this error when uploading audio files or querying `audio_url` field.</p>
  <p>Free plan users cannot upload audio files. Please upgrade to a paid plan to upload audio files.</p>
</Accordion>

<Accordion title="paid_required (business_or_higher)">
  <p>You may receieve this error when querying `video_url` field.</p>
  <p>Free/pro plan users cannot query `video_url` field. Please upgrade to a Business or Enterprise plan to query `video_url` field.</p>
</Accordion>

<Accordion title="payload_too_small">
  <p>The audio file is too short to be processed. Please ensure the audio file is at least 50kb in size.</p>
</Accordion>

<Accordion title="invalid_language_code">
  <p>The language code you provided is invalid. Please refer to the [Language Codes](/miscellaneous/language-codes) page for a list of valid language codes.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Webhooks" icon="link" href="/graphql-api/webhooks">
    Create notifications using webhooks
  </Card>

  <Card title="Add to Live" icon="link" href="/graphql-api/mutation/add-to-live">
    Use the API to add the Fireflies.ai bot to an ongoing meeting
  </Card>
</CardGroup>
