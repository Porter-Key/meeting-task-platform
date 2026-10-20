<!-- Source: https://docs.fireflies.ai/schema/input/share-meeting-input.md -->
<!-- Title: ShareMeetingInput -->
<!-- Description: Schema for ShareMeetingInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# ShareMeetingInput

> Schema for ShareMeetingInput

<ParamField path="meeting_id" type="ID" required>
  The unique identifier of the meeting / transcript to share.
</ParamField>

<ParamField path="emails" type="[String]" required>
  An array of email addresses to share the meeting with. Maximum 50 emails per request.
</ParamField>

<ParamField path="expiry_days" type="Int">
  Number of days until the shared access expires. Must be one of: `7`, `14`, or `30`. If omitted, the share does not expire.
</ParamField>
