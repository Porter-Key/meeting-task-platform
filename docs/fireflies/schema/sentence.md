<!-- Source: https://docs.fireflies.ai/schema/sentence.md -->
<!-- Title: Sentence -->
<!-- Description: Schema for Sentence -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Sentence

> Schema for Sentence

<ResponseField name="index" type="Int">
  Index
</ResponseField>

<ResponseField name="text" type="String">
  Default transcription sentence or user edited transcription sentence.
</ResponseField>

<ResponseField name="raw_text" type="String">
  Transcribed sentence from meeting audio
</ResponseField>

<ResponseField name="start_time" type="String">
  Start time of Sentence
</ResponseField>

<ResponseField name="end_time" type="String">
  End time of Sentence
</ResponseField>

<ResponseField name="speaker_id" type="ID">
  Unique identifier for Speaker
</ResponseField>

<ResponseField name="speaker_name" type="String">
  Name of the speaker.
</ResponseField>

<ResponseField name="ai_filters" type="AIFilter">
  Sentiment analysis from meeting audio. Type of [AIFilter](/schema/aifilter)
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="AIFilter" icon="link" href="/schema/aifilter">
    Schema for AIFilter
  </Card>

  <Card title="Speaker" icon="link" href="/schema/speaker">
    Schema for Speaker
  </Card>
</CardGroup>
