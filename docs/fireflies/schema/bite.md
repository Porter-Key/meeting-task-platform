<!-- Source: https://docs.fireflies.ai/schema/bite.md -->
<!-- Title: Bite -->
<!-- Description: Schema for Bite -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Bite

> Schema for Bite

<ResponseField name="id" type="String">
  A unique identifier for the Bite
</ResponseField>

<ResponseField name="transcript_id" type="String">
  A unique identifier for the transcript the Bite is associated to
</ResponseField>

<ResponseField name="start_time" type="String">
  Start time for the Bite
</ResponseField>

<ResponseField name="end_time" type="String">
  End time for the Bite
</ResponseField>

<ResponseField name="name" type="String">
  A string representing the title of the Bite
</ResponseField>

<ResponseField name="thumbnail" type="String">
  URL of the Bite's thumbnail image
</ResponseField>

<ResponseField name="preview" type="String">
  URL to a short preview video of the Bite
</ResponseField>

<ResponseField name="status" type="String">
  Current processing status of the Bite. Acceptable values include 'pending', 'processing', 'ready',
  and 'error'
</ResponseField>

<ResponseField name="summary" type="String">
  An AI-generated summary describing the content of the Bite
</ResponseField>

<ResponseField name="userId" type="String">
  Identifier of the user who created the Bite
</ResponseField>

<ResponseField name="summary_status" type="String">
  Status of the AI summary generation process
</ResponseField>

<ResponseField name="media_type" type="String">
  Type of the Bite, either 'video' or 'audio'
</ResponseField>

<ResponseField name="privacies" type="[BitePrivacy]">
  Array specifying the visibility of the Bite. Possible values are `public`, `team`, and
  `participants`. For example, `["team", "participants"]` indicates visibility to both team members
  and participants, while `["public"]` allows anyone to access the bite through its link
</ResponseField>

<ResponseField name="created_at" type="String">
  The date when this Bite was created
</ResponseField>

<ResponseField name="user" type="BiteUser">
  Object representing the user who created the Bite, including relevant user details

  <Expandable title="properties">
    <ResponseField name="name" type="String" required>
      Name associated with the User
    </ResponseField>

    <ResponseField name="id" type="String" required>
      ID of the User
    </ResponseField>

    <ResponseField name="first_name" type="String">
      First name of the User
    </ResponseField>

    <ResponseField name="last_name" type="String">
      Last name of the User
    </ResponseField>

    <ResponseField name="picture" type="String">
      Picture associated with the User
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="sources" type="[MediaSource]">
  Array of MediaSource objects for the Bite

  <Expandable title="properties">
    <ResponseField name="src" type="String" required>
      Source of the media
    </ResponseField>

    <ResponseField name="type" type="String">
      Type of the media
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="captions" type="[BiteCaption]">
  Array of Object describing text captions associated with the Bite

  <Expandable title="properties">
    <ResponseField name="index" type="String" required>
      Index
    </ResponseField>

    <ResponseField name="speaker_id" type="String" required>
      SpeakerId associated with the caption object
    </ResponseField>

    <ResponseField name="text" type="String" required>
      Text associated with the caption
    </ResponseField>

    <ResponseField name="speaker_name" type="String" required>
      Name of the speaker associated with this caption
    </ResponseField>

    <ResponseField name="start_time" type="String" required>
      Start time for the caption
    </ResponseField>

    <ResponseField name="end_time" type="String" required>
      End time for the caption
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="created_from" type="BiteOrigin">
  Object describing the origin of the Bite with the following properties

  <Expandable title="properties">
    <ResponseField name="id" type="String" required>
      Unique identifier
    </ResponseField>

    <ResponseField name="name" type="String" required>
      Name of the origin source
    </ResponseField>

    <ResponseField name="type" type="String" required>
      Type of the original source, e.g., 'meeting'
    </ResponseField>

    <ResponseField name="duration" type="String">
      Length of the original source in seconds
    </ResponseField>
  </Expandable>
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcript" icon="link" href="/schema/transcript">
    Schema for Transcript
  </Card>

  <Card title="Create Bite" icon="link" href="/graphql-api/mutation/create-bite">
    Use the API to create bites from your transcripts
  </Card>
</CardGroup>
