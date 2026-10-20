<!-- Source: https://docs.fireflies.ai/schema/input/update-meeting-state-input.md -->
<!-- Title: UpdateMeetingStateInput -->
<!-- Description: Schema for UpdateMeetingStateInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# UpdateMeetingStateInput

> Schema for UpdateMeetingStateInput

<ParamField path="meeting_id" type="ID!" required>
  The ID of the live meeting to update state for
</ParamField>

<ParamField path="action" type="MeetingStateAction!" required>
  The action to perform. Must be one of: `pause_recording` or `resume_recording`
</ParamField>
