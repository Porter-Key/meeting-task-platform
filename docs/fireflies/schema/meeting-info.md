<!-- Source: https://docs.fireflies.ai/schema/meeting-info.md -->
<!-- Title: MeetingInfo -->
<!-- Description: Schema for MeetingInfo -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# MeetingInfo

> Schema for MeetingInfo

<ResponseField name="fred_joined" type="Boolean">
  Boolean value that returns `true` if the bot joined the call, `false` otherwise.
</ResponseField>

<ResponseField name="silent_meeting" type="Boolean">
  Boolean value that returns `true` if the meeting does not contain any spoken words. Otherwise
  false.
</ResponseField>

<ResponseField name="summary_status" type="SummaryStatus">
  String value representing the summary status. Possible values are `processing`, `processed`,
  `failed`, `skipped`.
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcript" icon="link" href="/schema/transcript">
    Schema for Transcript
  </Card>

  <Card title="Summary" icon="link" href="/schema/summary">
    Schema for Summary
  </Card>
</CardGroup>
