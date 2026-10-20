<!-- Source: https://docs.fireflies.ai/schema/input/update-meeting-title-input.md -->
<!-- Title: UpdateMeetingTitleInput -->
<!-- Description: Schema for UpdateMeetingTitleInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# UpdateMeetingTitleInput

> Schema for UpdateMeetingTitleInput

<ParamField path="title" type="String" required>
  The new title to be assigned to the meeting / transcript. The title must be a string between 5 and 250 characters long and should not contain any special characters.

  Min / max of 5 / 256 characters.
</ParamField>

<ParamField path="id" type="String" required>
  The unique identifier of the meeting / transcript.
</ParamField>
