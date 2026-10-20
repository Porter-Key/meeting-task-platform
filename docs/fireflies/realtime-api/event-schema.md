<!-- Source: https://docs.fireflies.ai/realtime-api/event-schema.md -->
<!-- Title: Event Schema -->
<!-- Description: Reference for all events emitted by the Fireflies.ai Realtime API -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Event Schema

> Reference for all events emitted by the Fireflies.ai Realtime API

# Event Reference

This page documents the events you may receive from the Fireflies.ai Realtime API WebSocket.

## Event List

| Event Name                | Description                                                                     |
| ------------------------- | ------------------------------------------------------------------------------- |
| `auth.success`            | Emitted when authentication succeeds.                                           |
| `auth.failed`             | Emitted when authentication fails. The socket will disconnect after this event. |
| `connection.established`  | Emitted when the connection is successfully established.                        |
| `connection.error`        | Emitted when there is a connection or authorization error.                      |
| `transcription.broadcast` | Emitted for every new transcription segment or update.                          |

## RealtimeTranscriptionEvent

<ResponseField name="transcript_id" type="String">
  The unique identifier for the transcript / meeting
</ResponseField>

<ResponseField name="chunk_id" type="String">
  The unique identifier for the transcription segment (chunk). You may use this field to deduplicate transcription events. If the transcription is being updated, it will contain the same chunk\_id as the previous event. A new transcription will have a different chunk\_id
</ResponseField>

<ResponseField name="text" type="String">
  The transcribed text for this segment.
</ResponseField>

<ResponseField name="speaker_name" type="String">
  The name of the speaker for this segment.
</ResponseField>

<ResponseField name="start_time" type="Float">
  The start time (in seconds)
</ResponseField>

<ResponseField name="end_time" type="Float">
  The end time (in seconds)
</ResponseField>

## Example Payload

```json theme={null}
{
  "transcript_id": "abc123",
  "chunk_id": "chunk_001",
  "text": "Hello world",
  "speaker_name": "Alice",
  "start_time": 0.0,
  "end_time": 1.25
}
```

## Additional Resources

<CardGroup cols={2}>
  <Card title="Getting Started" icon="link" href="/realtime-api/getting-started">
    Getting started with Realtime API
  </Card>

  <Card title="Sentence" icon="link" href="/schema/sentence">
    Schema for Sentence
  </Card>
</CardGroup>
