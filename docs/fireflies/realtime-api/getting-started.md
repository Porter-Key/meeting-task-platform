<!-- Source: https://docs.fireflies.ai/realtime-api/getting-started.md -->
<!-- Title: Getting Started -->
<!-- Description: Learn how to connect to Fireflies.ai's Realtime API for live transcription -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting Started

> Learn how to connect to Fireflies.ai's Realtime API for live transcription

## Overview

This guide shows you how to connect to the Fireflies.ai Realtime API and start receiving transcription events in real time.

## Endpoint

```text theme={null}
wss://api.fireflies.ai
```

## Requirements

You'll need the following:

* A valid API token
* A `transcriptId` (or meeting ID)

<Tip>
  Use the [Active Meetings](/graphql-api/query/active-meetings) query to discover meetings currently in progress and get their IDs for connecting to the Realtime API.
</Tip>

## Connecting via Socket.IO

Use the Socket.IO client to connect and listen for events.

```ts theme={null}
import { io } from 'socket.io-client';

const socket = io('wss://api.fireflies.ai', {
  path: '/ws/realtime',
  auth: {
    token: 'Bearer <YOUR_API_TOKEN>',
    transcriptId: '<TRANSCRIPT_ID>'
  }
});

socket.on('auth.success', data => {
  console.log('Authenticated:', data);
});

socket.on('auth.failed', err => {
  console.error('Authentication failed:', err);
});

socket.on('connection.error', err => {
  console.error('Connection error:', err);
});

socket.on('connection.established', () => {
  console.log('Connection established');
});

socket.on('transcription.broadcast', event => {
  console.log('Transcript event:', event);
});
```

## Auth Parameters

| Field          | Type   | Description                     |
| -------------- | ------ | ------------------------------- |
| `token`        | string | Your API access token           |
| `transcriptId` | string | ID of the meeting or transcript |

If authentication fails, the server emits an `auth.failed` event and disconnects the socket.

See [Authorization](/fundamentals/authorization)

## Additional Resources

<CardGroup cols={2}>
  <Card title="Overview" icon="link" href="/realtime-api/overview">
    Overview of Realtime API
  </Card>

  <Card title="Active Meetings" icon="link" href="/graphql-api/query/active-meetings">
    Query meetings currently in progress
  </Card>

  <Card title="Authorization" icon="link" href="/fundamentals/authorization">
    Authenticating your requests with the Fireflies API
  </Card>
</CardGroup>
