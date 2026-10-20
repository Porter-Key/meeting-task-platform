<!-- Source: https://docs.fireflies.ai/schema/input/revoke-shared-meeting-access-input.md -->
<!-- Title: RevokeSharedMeetingAccessInput -->
<!-- Description: Schema for RevokeSharedMeetingAccessInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# RevokeSharedMeetingAccessInput

> Schema for RevokeSharedMeetingAccessInput

<ParamField path="meeting_id" type="ID" required>
  The unique identifier of the meeting / transcript.
</ParamField>

<ParamField path="email" type="String" required>
  The email address of the user whose shared access should be revoked.
</ParamField>
