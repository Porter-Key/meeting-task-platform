<!-- Source: https://docs.fireflies.ai/graphql-api/webhooks.md -->
<!-- Title: Webhooks -->
<!-- Description: Webhook events for the Fireflies.ai API -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Webhooks

> Webhook events for the Fireflies.ai API

## Overview

Webhooks enable your application to set up event based notifications. In this section, you'll learn how to configure webhooks to receive updates from Fireflies.

## Events supported

The webhooks support the following events:

* Transcription complete: Triggers when a meeting has been processed and the transcript is ready for viewing

<Note>
  Fireflies sends webhook notifications as POST requests to your specified endpoint. Each request
  contains a JSON payload with information about the event that occurred.
</Note>

## Saving a webhook

Follow the instructions below to save a webhook URL that sends notifications for all subscribed events. This webhook will only be fired for meetings that you own.

<Steps>
  <Step>Visit the [Fireflies.ai dashboard settings](https://app.fireflies.ai/settings)</Step>
  <Step>Navigate to the Developer settings tab</Step>
  <Step>Enter a valid https URL in the webhooks field and save</Step>
</Steps>

You may test your webhook using the upload audio API or by uploading through the dashboard at [app.fireflies.ai/upload](https://app.fireflies.ai/upload)

## Upload audio webhook

You can also include a webhook URL as part of an upload audio request. This is different from the saved webhook as it will only send notifications for that singular audio upload request.

<CodeGroup>
  ```bash curl theme={null}
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_api_key" \
    -d '{
      "query": "mutation($input: AudioUploadInput) { uploadAudio(input: $input) { success title message } }",
      "variables": {
        "input": {
          "url": "https://url_to_the_audio_file",
          "title": "title of the file",
          "webhook": "https://url_for_the_webhook"
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
    url: 'https://url_to_the_audio_file',
    title: 'title of the file',
    webhook: 'https://url_for_the_webhook'
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
  	"webhook": "https://url_for_the_webhook"
  }

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
  			+ "\"webhook\":\"https://url_for_the_webhook\""
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
</CodeGroup>

## Webhook Authentication

Webhook authentication ensures that incoming webhook requests are securely verified before processing. This allows consumers to trust that webhook events originate from a secure and verified source.

### How It Works

Each webhook request sent from the server includes an `x-hub-signature` header containing a SHA-256 HMAC signature of the request payload. This signature is generated using a secret key known only to the server and your application.

When the consumer receives a webhook, they can use the signature provided in the `x-hub-signature` header to verify that the request has not been tampered with. This is done by computing their own HMAC signature using the shared secret key and comparing it to the signature included in the header.

### Saving a secret

1. Go to the settings page at [app.fireflies.ai/settings](https://app.fireflies.ai/settings)
2. Navigate to the **Developer Settings** tab
3. You can either:
   * Enter a custom secret key of 16-32 characters in the input field
   * Click on the refresh button to generate a random secret key
4. Click Save to ensure the secret gets updated
5. Make sure to store this secret key securely, as it will be used to authenticate incoming webhook requests

### Verifying the Signature

1. **Receive the Webhook**:

   * Each request will include the payload and an `x-hub-signature` header

2. **Verify the Signature**:
   * Compute the HMAC SHA-256 signature using the payload and the shared secret key
   * Compare the computed signature to the `x-hub-signature` header value
   * If they match, the request is verified as authentic. If they do not match, treat the request with caution or reject it

By verifying webhook signatures, consumers can ensure that webhook events received are secure and have not been altered during transmission

### See it in action

To see webhook authentication in action, you can view an example at [Fireflies.ai Verifying Webhook Requests](https://replit.com/@firefliesai/Firefliesai-Verifying-webhook-requests#index.js). This example demonstrates how to receive a webhook, compute the HMAC SHA-256 signature, and verify it against the `x-hub-signature` header to ensure the request's authenticity.

## Webhook Schema

<ParamField path="meetingId" type="String" required>
  Identifier for the meeting / transcript that the webhook has triggered for. MeetingId and
  TranscriptId are used interchangeably for the Fireflies.ai Platform.
</ParamField>

<ParamField path="eventType" type="String">
  Name of the event type that has been fired against the webhook
</ParamField>

<ParamField path="clientReferenceId" type="ID">
  Custom identifier set by the user during upload. You may use this to identify your uploads in your
  events.
</ParamField>

## Example Payload

```json theme={null}
{
  "meetingId": "ASxwZxCstx",
  "eventType": "Transcription completed",
  "clientReferenceId": "be582c46-4ac9-4565-9ba6-6ab4264496a8"
}
```

## FAQ

<Accordion title="Why am I not receiving webhook requests">
  <p>There may be multiple reasons why you are not receiving webhook requests. Please go through the following checklist:</p>

  <ul>
    <li>Webhooks are only fired for meeting owners, referred to in the API as the `organizer_email.` Ensure that you have correctly setup the webhooks for the meeting owner.</li>
    <li>Ensure that your webhook is setup as a POST request</li>
    <li>If you have setup secret verification, ensure that you are correctly verifying the request by checking the example implementation [here](https://replit.com/@firefliesai/Firefliesai-Verifying-webhook-requests?v=1).</li>
  </ul>

  <p>Team-wide webhooks are only supported for the Enterprise tier with the Super Admin role. This allows you to setup one webhook for all meetings owned by your team. Details [here](/fundamentals/super-admin).</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Super Admin" icon="link" href="/fundamentals/super-admin">
    Fireflies Super Admin with advanced capabilities
  </Card>

  <Card title="Upload Audio" icon="link" href="/graphql-api/mutation/upload-audio">
    Use the API to upload audio to Fireflies.ai
  </Card>
</CardGroup>
