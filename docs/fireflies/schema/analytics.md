<!-- Source: https://docs.fireflies.ai/schema/analytics.md -->
<!-- Title: Analytics -->
<!-- Description: Schema for Analytics -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Analytics

> Schema for Analytics

<ParamField path="team" type="TeamAnalytics">
  Analytics data for the team. See [TeamAnalytics](#teamanalytics)
</ParamField>

<ParamField path="users" type="[UserAnalytics]">
  List of analytics data for individual users. See [UserAnalytics](#useranalytics)
</ParamField>

## TeamAnalytics

<ParamField path="conversation" type="TeamConversationStats">
  Conversation statistics for the team. See [TeamConversationStats](#teamconversationstats)
</ParamField>

<ParamField path="meeting" type="TeamMeetingStats">
  Meeting statistics for the team. See [TeamMeetingStats](#teammeetingstats)
</ParamField>

## TeamMeetingStats

<ParamField path="count" type="Int">
  Total count of meetings
</ParamField>

<ParamField path="count_diff_pct" type="Int" optional>
  Percentage difference in meeting count compared to previous period
</ParamField>

<ParamField path="duration" type="Float">
  Total duration of meetings in minutes
</ParamField>

<ParamField path="duration_diff_pct" type="Int" optional>
  Percentage difference in meeting duration compared to previous period
</ParamField>

<ParamField path="average_count" type="Int">
  Average number of meetings per user
</ParamField>

<ParamField path="average_count_diff_pct" type="Int" optional>
  Percentage difference in average meeting count compared to previous period
</ParamField>

<ParamField path="average_duration" type="Int">
  Average duration of meetings in minutes
</ParamField>

<ParamField path="average_duration_diff_pct" type="Int" optional>
  Percentage difference in average meeting duration compared to previous period
</ParamField>

## UserMeetingStats

<ParamField path="count" type="Int">
  Total count of meetings for the user
</ParamField>

<ParamField path="count_diff" type="Int">
  Difference in meeting count compared to previous period
</ParamField>

<ParamField path="count_diff_compared_to" type="Int">
  Meeting count in the previous period
</ParamField>

<ParamField path="count_diff_pct" type="Int" optional>
  Percentage difference in meeting count compared to previous period
</ParamField>

<ParamField path="duration" type="Float">
  Total duration of meetings in minutes for the user
</ParamField>

<ParamField path="duration_diff" type="Int">
  Difference in meeting duration compared to previous period
</ParamField>

<ParamField path="duration_diff_compared_to" type="Int">
  Meeting duration in the previous period
</ParamField>

<ParamField path="duration_diff_pct" type="Int" optional>
  Percentage difference in meeting duration compared to previous period
</ParamField>

## TeamConversationStats

<ParamField path="average_filler_words" type="Int">
  Average number of filler words used per meeting
</ParamField>

<ParamField path="average_filler_words_diff_pct" type="Int" optional>
  Percentage difference in average filler words compared to previous period
</ParamField>

<ParamField path="average_monologues_count" type="Int">
  Average number of monologues per meeting
</ParamField>

<ParamField path="average_monologues_count_diff_pct" type="Int" optional>
  Percentage difference in average monologues count compared to previous period
</ParamField>

<ParamField path="average_questions" type="Int">
  Average number of questions asked per meeting
</ParamField>

<ParamField path="average_questions_diff_pct" type="Int" optional>
  Percentage difference in average questions compared to previous period
</ParamField>

<ParamField path="average_sentiments" type="Sentiments">
  Average sentiment analysis results for team meetings. See [Sentiments](/schema/sentiments)
</ParamField>

<ParamField path="average_silence_duration" type="Float">
  Average duration of silence in minutes per meeting
</ParamField>

<ParamField path="average_silence_duration_diff_pct" type="Int" optional>
  Percentage difference in average silence duration compared to previous period
</ParamField>

<ParamField path="average_talk_listen_ratio" type="Float">
  Average ratio of talking to listening across all meetings
</ParamField>

<ParamField path="average_words_per_minute" type="Float">
  Average words spoken per minute across all meetings
</ParamField>

<ParamField path="longest_monologue_duration_sec" type="Int">
  Duration in seconds of the longest monologue
</ParamField>

<ParamField path="longest_monologue_duration_diff_pct" type="Int" optional>
  Percentage difference in longest monologue duration compared to previous period
</ParamField>

<ParamField path="total_filler_words" type="Int">
  Total number of filler words used across all meetings
</ParamField>

<ParamField path="total_filler_words_diff_pct" type="Int" optional>
  Percentage difference in total filler words compared to previous period
</ParamField>

<ParamField path="total_meeting_notes_count" type="Int">
  Total count of meeting notes created
</ParamField>

<ParamField path="total_meetings_count" type="Int">
  Total count of meetings
</ParamField>

<ParamField path="total_monologues_count" type="Int">
  Total count of monologues across all meetings
</ParamField>

<ParamField path="total_monologues_diff_pct" type="Int" optional>
  Percentage difference in total monologues compared to previous period
</ParamField>

<ParamField path="teammates_count" type="Int">
  Number of teammates included in the analytics
</ParamField>

<ParamField path="total_questions" type="Int">
  Total number of questions asked across all meetings
</ParamField>

<ParamField path="total_questions_diff_pct" type="Int" optional>
  Percentage difference in total questions compared to previous period
</ParamField>

<ParamField path="total_silence_duration" type="Float">
  Total duration of silence in minutes across all meetings
</ParamField>

<ParamField path="total_silence_duration_diff_pct" type="Int" optional>
  Percentage difference in total silence duration compared to previous period
</ParamField>

## UserConversationStats

<ParamField path="talk_listen_pct" type="Float">
  Percentage of time spent talking vs listening
</ParamField>

<ParamField path="talk_listen_ratio" type="Float">
  Ratio of talking to listening
</ParamField>

<ParamField path="total_silence_duration" type="Float">
  Total duration of silence in minutes for the user
</ParamField>

<ParamField path="total_silence_duration_compare_to" type="Float" optional>
  Silence duration in the previous period
</ParamField>

<ParamField path="total_silence_pct" type="Float">
  Percentage of meeting time spent in silence
</ParamField>

<ParamField path="total_silence_ratio" type="Float">
  Ratio of silence to speaking time
</ParamField>

<ParamField path="total_speak_duration" type="Float">
  Total duration of speaking time in minutes
</ParamField>

<ParamField path="total_speak_duration_with_user" type="Float">
  Total duration of speaking time with specific user in minutes
</ParamField>

<ParamField path="total_word_count" type="Int">
  Total count of words spoken
</ParamField>

<ParamField path="user_filler_words" type="Int">
  Number of filler words used by the user
</ParamField>

<ParamField path="user_filler_words_compare_to" type="Int">
  Filler words used in the previous period
</ParamField>

<ParamField path="user_filler_words_diff_pct" type="Int" optional>
  Percentage difference in filler words compared to previous period
</ParamField>

<ParamField path="user_longest_monologue_sec" type="Int">
  Duration in seconds of the user's longest monologue
</ParamField>

<ParamField path="user_longest_monologue_compare_to" type="Int">
  Longest monologue duration in the previous period
</ParamField>

<ParamField path="user_longest_monologue_diff_pct" type="Int" optional>
  Percentage difference in longest monologue duration compared to previous period
</ParamField>

<ParamField path="user_monologues_count" type="Int">
  Count of monologues by the user
</ParamField>

<ParamField path="user_monologues_count_compare_to" type="Int">
  Monologues count in the previous period
</ParamField>

<ParamField path="user_monologues_count_diff_pct" type="Int" optional>
  Percentage difference in monologues count compared to previous period
</ParamField>

<ParamField path="user_questions" type="Int">
  Number of questions asked by the user
</ParamField>

<ParamField path="user_questions_compare_to" type="Int">
  Questions asked in the previous period
</ParamField>

<ParamField path="user_questions_diff_pct" type="Int" optional>
  Percentage difference in questions asked compared to previous period
</ParamField>

<ParamField path="user_speak_duration" type="Float">
  Duration of time the user spent speaking in minutes
</ParamField>

<ParamField path="user_word_count" type="Int">
  Count of words spoken by the user
</ParamField>

<ParamField path="user_words_per_minute" type="Int">
  Words spoken per minute by the user
</ParamField>

<ParamField path="user_words_per_minute_compare_to" type="Int">
  Words per minute in the previous period
</ParamField>

<ParamField path="user_words_per_minute_diff_pct" type="Int" optional>
  Percentage difference in words per minute compared to previous period
</ParamField>

## UserAnalytics

<ParamField path="user_id" type="String">
  Unique identifier for the user
</ParamField>

<ParamField path="user_name" type="String">
  Name of the user
</ParamField>

<ParamField path="user_email" type="String">
  Email address of the user
</ParamField>

<ParamField path="conversation" type="UserConversationStats">
  Conversation statistics for the user. See [UserConversationStats](#userconversationstats)
</ParamField>

<ParamField path="meeting" type="UserMeetingStats">
  Meeting statistics for the user. See [UserMeetingStats](#usermeetingstats)
</ParamField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Sentiments" icon="link" href="/schema/sentiments">
    Schema for Sentiments
  </Card>

  <Card title="Meeting Analytics" icon="link" href="/schema/meeting-analytics">
    Schema for Meeting Analytics
  </Card>
</CardGroup>
