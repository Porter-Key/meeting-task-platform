from __future__ import annotations


TRANSCRIPT_FIELDS = """
id
title
date
dateString
privacy
host_email
organizer_email
participants
duration
transcript_url
audio_url
video_url
meeting_link
is_live
speakers { id name }
sentences {
  index
  speaker_name
  speaker_id
  text
  raw_text
  start_time
  end_time
  ai_filters { task pricing metric question date_and_time text_cleanup sentiment }
}
summary {
  keywords
  action_items
  outline
  shorthand_bullet
  overview
  bullet_gist
  gist
  short_summary
  short_overview
  meeting_type
  topics_discussed
  transcript_chapters
}
analytics {
  sentiments { negative_pct neutral_pct positive_pct }
  categories { questions date_times metrics tasks }
  speakers {
    speaker_id
    name
    duration
    word_count
    longest_monologue
    monologues_count
    filler_words
    questions
    duration_pct
    words_per_minute
  }
}
meeting_info { fred_joined silent_meeting summary_status }
"""


TRANSCRIPT_QUERY = f"""
query Transcript($transcriptId: String!) {{
  transcript(id: $transcriptId) {{
    {TRANSCRIPT_FIELDS}
  }}
}}
"""


TRANSCRIPTS_QUERY = f"""
query Transcripts(
  $keyword: String
  $scope: String
  $fromDate: DateTime
  $toDate: DateTime
  $limit: Int
  $skip: Int
  $hostEmail: String
  $organizers: [String!]
  $participants: [String!]
  $userId: String
  $mine: Boolean
  $channelId: String
) {{
  transcripts(
    keyword: $keyword
    scope: $scope
    fromDate: $fromDate
    toDate: $toDate
    limit: $limit
    skip: $skip
    host_email: $hostEmail
    organizers: $organizers
    participants: $participants
    user_id: $userId
    mine: $mine
    channel_id: $channelId
  ) {{
    {TRANSCRIPT_FIELDS}
  }}
}}
"""


ACTIVE_MEETINGS_QUERY = """
query ActiveMeetings($email: String, $states: [MeetingState!]) {
  active_meetings(input: { email: $email, states: $states }) {
    id
    title
    organizer_email
    meeting_link
    start_time
    end_time
    privacy
    state
  }
}
"""


ANALYTICS_QUERY = """
query Analytics($startTime: String, $endTime: String) {
  analytics(start_time: $startTime, end_time: $endTime) {
    team {
      conversation {
        average_filler_words
        average_filler_words_diff_pct
        average_monologues_count
        average_monologues_count_diff_pct
        average_questions
        average_questions_diff_pct
        average_sentiments { negative_pct neutral_pct positive_pct }
        average_silence_duration
        average_silence_duration_diff_pct
        average_talk_listen_ratio
        average_words_per_minute
        longest_monologue_duration_sec
        longest_monologue_duration_diff_pct
        total_filler_words
        total_filler_words_diff_pct
        total_meeting_notes_count
        total_meetings_count
        total_monologues_count
        total_monologues_diff_pct
        teammates_count
        total_questions
        total_questions_diff_pct
        total_silence_duration
        total_silence_duration_diff_pct
      }
      meeting {
        count
        count_diff_pct
        duration
        duration_diff_pct
        average_count
        average_count_diff_pct
        average_duration
        average_duration_diff_pct
      }
    }
    users {
      user_id
      user_name
      user_email
      conversation {
        talk_listen_pct
        talk_listen_ratio
        total_silence_duration
        total_silence_duration_compare_to
        total_silence_pct
        total_silence_ratio
        total_speak_duration
        total_speak_duration_with_user
        total_word_count
        user_filler_words
        user_filler_words_compare_to
        user_filler_words_diff_pct
        user_longest_monologue_sec
        user_longest_monologue_compare_to
        user_longest_monologue_diff_pct
        user_monologues_count
        user_monologues_count_compare_to
        user_monologues_count_diff_pct
        user_questions
        user_questions_compare_to
        user_questions_diff_pct
        user_speak_duration
        user_word_count
        user_words_per_minute
        user_words_per_minute_compare_to
        user_words_per_minute_diff_pct
      }
      meeting {
        count
        count_diff
        count_diff_compared_to
        count_diff_pct
        duration
        duration_diff
        duration_diff_compared_to
        duration_diff_pct
      }
    }
  }
}
"""
