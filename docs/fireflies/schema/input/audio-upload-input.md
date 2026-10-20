<!-- Source: https://docs.fireflies.ai/schema/input/audio-upload-input.md -->
<!-- Title: AudioUploadInput -->
<!-- Description: Schema for AudioUploadInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AudioUploadInput

> Schema for AudioUploadInput

<ParamField path="url" type="String" required>
  URL from which the audio file will be fetched. This should be a direct link to the audio resource.
</ParamField>

<ParamField path="title" type="String">
  Title assigned to the uploaded file. If not provided, the file's original name will be used as its
  title.

  Maximum length is 256 characters.
</ParamField>

<ParamField path="attendees" type="[Attendee]">
  Array of [Attendee](/schema/attendee) objects, as defined in the [Attendee](/schema/attendee)
  schema. Each element in this array represents an attendee.

  Max length of 100 attendees.
</ParamField>

<ParamField path="custom_language" type="String">
  Custom language code for the meeting
</ParamField>

<ParamField path="client_reference_id" type="String">
  Custom identifier set by the user during upload. You may use this to identify your uploads in your
  events.

  Maximum length is 128 characters.
</ParamField>

<ParamField path="save_video" type="Boolean">
  Boolean value that specifies whether the content video needs to be saved.
</ParamField>

<ParamField path="download_auth" type="DownloadAuthInput">
  Authentication configuration for downloading the media file. Use this when your audio/video file requires authentication. Supports bearer token and basic authentication methods. If not provided, defaults to no authentication (publicly accessible URL).

  See [DownloadAuthInput](/schema/input/download-auth-input) for the complete schema definition.
</ParamField>
