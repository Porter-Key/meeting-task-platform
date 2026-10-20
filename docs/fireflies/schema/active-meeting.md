<!-- Source: https://docs.fireflies.ai/schema/active-meeting.md -->
<!-- Title: ActiveMeeting -->
<!-- Description: Schema for ActiveMeeting -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# ActiveMeeting

> Schema for ActiveMeeting

<ResponseField name="id" type="String">
  Unique identifier for the active meeting
</ResponseField>

<ResponseField name="title" type="String">
  Title of the active meeting
</ResponseField>

<ResponseField name="organizer_email" type="String">
  Email address of the meeting organizer
</ResponseField>

<ResponseField name="meeting_link" type="String">
  The URL link to join the meeting (e.g., Zoom, Google Meet, Microsoft Teams link)
</ResponseField>

<ResponseField name="start_time" type="String">
  ISO 8601 formatted timestamp indicating when the meeting started (e.g., `2024-01-15T10:00:00.000Z`)
</ResponseField>

<ResponseField name="end_time" type="String">
  ISO 8601 formatted timestamp indicating when the meeting is scheduled to end (e.g., `2024-01-15T11:00:00.000Z`)
</ResponseField>

<ResponseField name="privacy" type="MeetingPrivacy">
  Privacy setting for the meeting. Possible values:

  * `link`: Anyone with the link can access
  * `owner`: Only the owner can access
  * `participants`: Only meeting participants can access
  * `teammates_and_participants`: Team members and participants can access
  * `participating_teammates`: Only teammates who participated can access
  * `teammates`: All team members can access
</ResponseField>

<ResponseField name="state" type="MeetingState">
  Current state of the meeting. Possible values:

  * `active`: Meeting is currently in progress
  * `paused`: Meeting has been paused
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Active Meetings Query" icon="link" href="/graphql-api/query/active-meetings">
    Query active meetings in progress
  </Card>

  <Card title="Transcript Schema" icon="link" href="/schema/transcript">
    Schema for completed meeting transcripts
  </Card>
</CardGroup>
