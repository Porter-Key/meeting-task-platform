<!-- Source: https://docs.fireflies.ai/schema/input/update-meeting-channel-input.md -->
<!-- Title: UpdateMeetingChannelInput -->
<!-- Description: Schema for UpdateMeetingChannelInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# UpdateMeetingChannelInput

> Schema for UpdateMeetingChannelInput

<ParamField path="transcript_ids" type="[String!]!" required>
  Array of Transcript IDs to update. Must contain 1–5 items.
</ParamField>

<ParamField path="channel_id" type="ID!" required>
  The target Channel ID. A meeting can only belong to one channel; this mutation sets the meeting's channel to the specified value.
</ParamField>
