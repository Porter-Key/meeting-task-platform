<!-- Source: https://docs.fireflies.ai/schema/meeting-analytics.md -->
<!-- Title: MeetingAnalytics -->
<!-- Description: Schema for MeetingAnalytics -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# MeetingAnalytics

> Schema for MeetingAnalytics

<ResponseField name="sentiments" type="Sentiments">
  Sentiment analysis of the meeting. See [Sentiments](/schema/sentiments)
</ResponseField>

<ResponseField name="categories" type="AnalyticsCategories">
  Categorized analytics of the meeting content. See [AnalyticsCategories](#analyticscategories)
</ResponseField>

<ResponseField name="speakers" type="[AnalyticsSpeaker]">
  Array of analytics data for each speaker in the meeting. See [AnalyticsSpeaker](#analyticsspeaker)
</ResponseField>

## AnalyticsCategories

<ResponseField name="questions" type="Int">
  Number of questions asked during the meeting.
</ResponseField>

<ResponseField name="date_times" type="Int">
  Number of date and time references mentioned in the meeting.
</ResponseField>

<ResponseField name="metrics" type="Int">
  Number of metrics or measurements discussed in the meeting.
</ResponseField>

<ResponseField name="tasks" type="Int">
  Number of tasks or action items identified in the meeting.
</ResponseField>

## AnalyticsSpeaker

<ResponseField name="speaker_id" type="Int">
  Unique identifier for the speaker.
</ResponseField>

<ResponseField name="name" type="String">
  Name of the speaker.
</ResponseField>

<ResponseField name="duration" type="Float">
  Total speaking time of the speaker in seconds.
</ResponseField>

<ResponseField name="word_count" type="Int">
  Total number of words spoken by the speaker.
</ResponseField>

<ResponseField name="longest_monologue" type="Float">
  Duration of the speaker's longest continuous speech in seconds.
</ResponseField>

<ResponseField name="monologues_count" type="Int">
  Number of times the speaker spoke during the meeting.
</ResponseField>

<ResponseField name="filler_words" type="Int">
  Number of filler words (um, uh, like, etc.) used by the speaker.
</ResponseField>

<ResponseField name="questions" type="Int">
  Number of questions asked by the speaker.
</ResponseField>

<ResponseField name="duration_pct" type="Float">
  Percentage of the total meeting time the speaker was talking.
</ResponseField>

<ResponseField name="words_per_minute" type="Float">
  Average speaking rate of the speaker in words per minute.
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Sentiments" icon="link" href="/schema/sentiments">
    Schema for Sentiments
  </Card>

  <Card title="Speaker" icon="link" href="/schema/speaker">
    Schema for Speaker
  </Card>
</CardGroup>
