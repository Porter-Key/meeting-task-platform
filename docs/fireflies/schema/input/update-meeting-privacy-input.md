<!-- Source: https://docs.fireflies.ai/schema/input/update-meeting-privacy-input.md -->
<!-- Title: UpdateMeetingPrivacyInput -->
<!-- Description: Schema for UpdateMeetingPrivacyInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# UpdateMeetingPrivacyInput

> Schema for UpdateMeetingPrivacyInput

<ParamField path="id" type="String" required>
  The unique identifier of the meeting / transcript.
</ParamField>

<ParamField path="privacy" type="String" required>
  The privacy level for the meeting. Must be one of the following values:

  * `link` - Anyone with the link can access the meeting
  * `owner` - Only the meeting owner can access
  * `participants` - Only meeting participants can access
  * `teammatesandparticipants` - Both teammates and participants can access
  * `teammates` - Only teammates can access
</ParamField>
