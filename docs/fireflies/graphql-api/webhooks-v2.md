<!-- Source: https://docs.fireflies.ai/graphql-api/webhooks-v2.md -->
<!-- Title: Webhooks V2 -->
<!-- Description: Configure event-driven webhooks with granular event subscriptions using Webhooks V2 -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Webhooks V2

> Configure event-driven webhooks with granular event subscriptions using Webhooks V2

## Overview

Webhooks V2 provides an improved webhook system with granular event subscriptions and enhanced security. You can subscribe to specific meeting lifecycle events and receive real-time notifications at your configured endpoint.

<Note>
  Webhooks V2 replaces the legacy webhook system. If you are currently using [Webhooks V1](/graphql-api/webhooks), we recommend migrating to V2 for a better experience.
</Note>

## Events Supported

Webhooks V2 supports the following events:

| Event Name            | Description                                                              |
| --------------------- | ------------------------------------------------------------------------ |
| `meeting.transcribed` | Triggers when a meeting has been transcribed and the transcript is ready |
| `meeting.summarized`  | Triggers when a meeting summary has been generated                       |

<Note>
  You can subscribe to one or more events per webhook. Only events you subscribe to will be delivered.
</Note>

## Setting Up Webhooks V2

<Steps>
  <Step>Visit the [Webhooks V2 configuration page](https://app.fireflies.ai/integrations/api/webhook)</Step>
  <Step>Enter a valid HTTPS URL that accepts POST requests in the **Webhook URL** field</Step>
  <Step>Optionally, enter a **Signing Secret** for payload signature verification</Step>
  <Step>Select the **events** you want to subscribe to</Step>
  <Step>Save your configuration</Step>
</Steps>

## Webhook Payload

Each webhook notification is sent as a `POST` request with a JSON payload containing the following fields:

<ParamField path="event" type="String" required>
  The event type that triggered the webhook (e.g., `meeting.transcribed`, `meeting.summarized`)
</ParamField>

<ParamField path="timestamp" type="Number" required>
  Unix timestamp in milliseconds indicating when the event was fired
</ParamField>

<ParamField path="meeting_id" type="String" required>
  Identifier for the meeting that the event relates to. This is the same as the transcript ID used throughout the Fireflies API.
</ParamField>

<ParamField path="client_reference_id" type="String">
  Custom identifier set by you during upload. Use this to correlate webhook events with your uploads.
</ParamField>

### Example Payloads

**Meeting Transcribed**

```json theme={null}
{
  "event": "meeting.transcribed",
  "timestamp": 1710876543210,
  "meeting_id": "ASxwZxCstx",
  "client_reference_id": "be582c46-4ac9-4565-9ba6-6ab4264496a8"
}
```

**Meeting Summarized**

```json theme={null}
{
  "event": "meeting.summarized",
  "timestamp": 1710876789456,
  "meeting_id": "ASxwZxCstx"
}
```

## Webhook Authentication

Webhooks V2 uses HMAC-SHA256 signatures to verify that webhook payloads originate from Fireflies and have not been tampered with in transit.

### How It Works

Each webhook request includes an `X-Hub-Signature` header containing a SHA-256 HMAC signature of the request body. The signature is computed using the signing secret you configured during setup.

The signature format is:

```
sha256=<hex-encoded-hmac-sha256-digest>
```

### Verifying the Signature

<Steps>
  <Step>Extract the `X-Hub-Signature` header from the incoming request</Step>
  <Step>Compute the HMAC-SHA256 digest of the raw request body using your signing secret</Step>
  <Step>Prefix the hex-encoded digest with `sha256=`</Step>
  <Step>Compare the computed signature with the header value using a timing-safe comparison</Step>
</Steps>

### Verification Examples

<CodeGroup>
  ```javascript node.js theme={null}
  const crypto = require('crypto');

  function verifyWebhookSignature(payload, signature, secret) {
    const expectedSignature =
      'sha256=' +
      crypto.createHmac('sha256', secret).update(payload, 'utf8').digest('hex');

    const sigBuffer = Buffer.from(signature);
    const expectedBuffer = Buffer.from(expectedSignature);

    if (sigBuffer.length !== expectedBuffer.length) {
      return false;
    }

    return crypto.timingSafeEqual(sigBuffer, expectedBuffer);
  }

  // Express.js example
  app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
    const signature = req.headers['x-hub-signature'];
    const payload = req.body.toString();

    if (!verifyWebhookSignature(payload, signature, 'your_signing_secret')) {
      return res.status(401).send('Invalid signature');
    }

    const event = JSON.parse(payload);
    console.log('Received event:', event.event, 'for meeting:', event.meeting_id);

    res.status(200).send('OK');
  });
  ```

  ```python python theme={null}
  import hmac
  import hashlib
  from flask import Flask, request

  app = Flask(__name__)

  def verify_webhook_signature(payload, signature, secret):
      expected = 'sha256=' + hmac.new(
          secret.encode('utf-8'),
          payload,
          hashlib.sha256
      ).hexdigest()

      return hmac.compare_digest(expected, signature)

  @app.route('/webhook', methods=['POST'])
  def webhook():
      signature = request.headers.get('X-Hub-Signature', '')
      payload = request.get_data()

      if not verify_webhook_signature(payload, signature, 'your_signing_secret'):
          return 'Invalid signature', 401

      event = request.get_json()
      print(f"Received event: {event['event']} for meeting: {event['meeting_id']}")

      return 'OK', 200
  ```

  ```java java theme={null}
  import javax.crypto.Mac;
  import javax.crypto.spec.SecretKeySpec;
  import java.security.MessageDigest;

  public class WebhookVerifier {

      public static boolean verifySignature(String payload, String signature, String secret)
              throws Exception {
          Mac mac = Mac.getInstance("HmacSHA256");
          mac.init(new SecretKeySpec(secret.getBytes("UTF-8"), "HmacSHA256"));

          byte[] hash = mac.doFinal(payload.getBytes("UTF-8"));
          StringBuilder hex = new StringBuilder();
          for (byte b : hash) {
              hex.append(String.format("%02x", b));
          }

          String expected = "sha256=" + hex.toString();
          return MessageDigest.isEqual(
              expected.getBytes("UTF-8"),
              signature.getBytes("UTF-8")
          );
      }
  }
  ```
</CodeGroup>

## Request Headers

Each webhook delivery includes the following headers:

| Header            | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| `Content-Type`    | `application/json`                                             |
| `User-Agent`      | `Fireflies-Webhook/1.0`                                        |
| `X-Hub-Signature` | HMAC-SHA256 signature (only if a signing secret is configured) |

## Delivery Behavior

* Webhooks are sent as `POST` requests to your configured URL
* Your endpoint must respond with a `2xx` status code within **10 seconds** to be considered successful
* If your endpoint does not respond in time or returns a non-`2xx` status code, the delivery is marked as failed

## Migrating from Webhooks V1

If you are using the legacy webhooks system, here is a summary of the key differences:

| Feature          | Webhooks V1                              | Webhooks V2                                                               |
| ---------------- | ---------------------------------------- | ------------------------------------------------------------------------- |
| Configuration    | Developer Settings page                  | [Dedicated setup page](https://app.fireflies.ai/integrations/api/webhook) |
| Events           | Single event (`Transcription completed`) | Multiple events (`meeting.transcribed`, `meeting.summarized`)             |
| Event selection  | All events                               | Granular event subscriptions                                              |
| Payload format   | `meetingId`, `eventType`                 | `meeting_id`, `event`, `timestamp`                                        |
| Signature header | `X-Hub-Signature`                        | `X-Hub-Signature`                                                         |
| Signature format | `sha256=<hex>`                           | `sha256=<hex>`                                                            |

### Migration Steps

<Steps>
  <Step>Go to the [Webhooks V2 setup page](https://app.fireflies.ai/integrations/api/webhook)</Step>
  <Step>Enter your existing webhook URL</Step>
  <Step>If you used a signing secret, enter it in the **Signing Secret** field</Step>
  <Step>Select the events you want to subscribe to (choose `meeting.transcribed` for equivalent V1 behavior)</Step>
  <Step>Save and update your webhook consumer to handle the new payload format and signature header</Step>
</Steps>

## FAQ

<Accordion title="What is the difference between meeting.transcribed and meeting.summarized?">
  `meeting.transcribed` fires when the raw transcript is ready and available for viewing. `meeting.summarized` fires after the AI-generated summary (including action items, notes, and other insights) has been processed.
</Accordion>

<Accordion title="Can I subscribe to multiple events?">
  Yes. You can select one or more events during setup. Only events you subscribe to will trigger webhook deliveries.
</Accordion>

<Accordion title="Why am I not receiving webhook notifications?">
  <ul>
    <li>Webhooks are only fired for meetings you own (i.e., you are the <code>organizer\_email</code>).</li>
    <li>Ensure your endpoint accepts POST requests and responds with a 2xx status code within 10 seconds.</li>
    <li>Verify that you have subscribed to the correct events.</li>
    <li>If using signature verification, ensure your signing secret matches what is configured.</li>
  </ul>
</Accordion>

<Accordion title="Do I need to migrate from Webhooks V1?">
  Webhooks V1 continues to work. However, V2 offers granular event subscriptions, so we recommend migrating when convenient.
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Webhooks V1" icon="link" href="/graphql-api/webhooks">
    Legacy webhook documentation
  </Card>

  <Card title="Upload Audio" icon="link" href="/graphql-api/mutation/upload-audio">
    Use the API to upload audio to Fireflies.ai
  </Card>
</CardGroup>
