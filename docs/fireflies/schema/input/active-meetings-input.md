<!-- Source: https://docs.fireflies.ai/schema/input/active-meetings-input.md -->
<!-- Title: GetActiveMeetingsInput -->
<!-- Description: Schema for GetActiveMeetingsInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# GetActiveMeetingsInput

> Schema for GetActiveMeetingsInput

<ParamField path="email" type="String">
  Filter active meetings by a specific user's email address.

  **Permission requirements:**

  * **Regular users**: Can only query their own active meetings (must pass their own email or omit this field)
  * **Admins**: Can query active meetings for any user in their team

  If this field is omitted, the query returns active meetings for the authenticated user.

  The email must be valid and belong to a user in the same team as the requester.
</ParamField>

<ParamField path="states" type="[MeetingState]">
  Filter active meetings by their state. Accepts an array of [MeetingState](/schema/enum/meeting-state) values.

  **Possible values:**

  * `active`: Meetings that are currently in progress
  * `paused`: Meetings that have been paused

  If this field is omitted, the query returns meetings in both `active` and `paused` states by default.
</ParamField>
