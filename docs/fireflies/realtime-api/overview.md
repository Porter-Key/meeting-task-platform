<!-- Source: https://docs.fireflies.ai/realtime-api/overview.md -->
<!-- Title: Overview -->
<!-- Description: Learn about Fireflies.ai's Realtime API for live transcription -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Overview

> Learn about Fireflies.ai's Realtime API for live transcription

The Fireflies.ai Realtime API allows your application to receive **live transcription events** over WebSockets. This enables building interactive features such as live captioning, transcription overlays, and real-time analysis as users speak.

<Warning>
  The Realtime API is currently in <b>beta</b>. Features and endpoints may change. We welcome your feedback as we continue to improve this API.
</Warning>

## How It Works

The Realtime API uses WebSocket connections to deliver transcription data as it's generated.

## Flow

1. **Authenticate**: Connect using a valid API token and transcript ID.
2. **Listen**: Once connected, you'll start receiving transcription events in real time.
3. **React**: Update your UI or process transcription events as they arrive.

## Features

* **Low Latency**: Data is streamed as soon as it’s transcribed.
* **Event-Based**: Receive structured events for easy handling.
* **Token-Based Authentication**: Secure connections with scoped access.
* **Incremental Transcription**: Receive transcript segments progressively.

## Additional Resources

<CardGroup cols={2}>
  <Card title="Active Meetings" icon="link" href="/graphql-api/query/active-meetings">
    Query meetings currently in progress
  </Card>

  <Card title="Event Schema" icon="link" href="/realtime-api/event-schema">
    Schema for Realtime Events
  </Card>
</CardGroup>
