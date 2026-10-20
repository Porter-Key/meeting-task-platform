<!-- Source: https://docs.fireflies.ai/getting-started/whats-new.md -->
<!-- Title: What's New -->
<!-- Description: Latest updates to the Fireflies API -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# What's New

> Latest updates to the Fireflies API

Take a look at our latest updates, features, and improvements for the Fireflies API.

<Update label="2.24.0" description="New MCP Tools">
  ### New MCP Tools

  The [Fireflies MCP Server](/mcp-tools/overview) has been expanded with 11 new tools, bringing the total to 17 core tools (plus 2 experimental). The MCP Server now supports write operations in addition to read-only queries, enabling AI assistants to take actions on your behalf.

  **New Meeting Management Tools:**

  * `fireflies_share_meeting` - Share meeting transcripts with up to 100 email recipients, with optional expiry
  * `fireflies_revoke_meeting_access` - Revoke previously shared meeting access
  * `fireflies_update_meeting_title` - Update the title of a meeting transcript
  * `fireflies_move_meeting` - Move meetings to a channel/folder (up to 5 at a time)

  **New Channel Tools:**

  * `fireflies_list_channels` - List all available channels/folders
  * `fireflies_get_channel` - Get details of a specific channel by ID

  **New Soundbite Tools:**

  * `fireflies_get_soundbites` - Fetch soundbites filtered by transcript, ownership, or team
  * `fireflies_create_soundbite` - Create a soundbite clip from a meeting transcript

  **New Analytics & Monitoring Tools:**

  * `fireflies_get_active_meetings` - Retrieve currently active (in-progress) meetings
  * `fireflies_get_analytics` - Get team and per-user meeting and conversation analytics

  **New Automation Tools:**

  * `fireflies_get_rule_executions` - View automation rule execution logs (Enterprise)

  For the complete tool reference, see [MCP Tools](/mcp-tools/overview).
</Update>

<Update label="2.23.0" description="Live Transcript Support">
  ### Live Transcript Support

  The [Transcript](/schema/transcript) schema now includes a new `is_live` field that indicates whether a meeting is currently live (active or paused). When querying a live meeting, the `sentences` field automatically returns real-time captions from the ongoing meeting instead of processed transcript data.

  This enables building features such as:

  * Displaying live captions during an active meeting
  * Monitoring meeting progress in real time
  * Building dashboards that show both live and completed meeting transcripts

  **New Fields:**

  * `is_live` on [Transcript](/schema/transcript) - Boolean indicating whether the meeting is currently live

  **Enhanced Behavior:**

  * `sentences` on [Transcript](/schema/transcript) - Now returns real-time captions for live meetings, and processed transcript data for completed meetings
</Update>

<Update label="2.22.0" description="Meeting Sharing API">
  ### Meeting Sharing API

  The Fireflies API now supports programmatic meeting sharing. Share meetings with external or internal users via email, control access duration, view who has access, and revoke access — all through the API.

  **New Mutations:**

  * [shareMeeting](/graphql-api/mutation/share-meeting) - Share a meeting with up to 100 email recipients, with optional expiry (7, 14, or 30 days)
  * [revokeSharedMeetingAccess](/graphql-api/mutation/revoke-shared-meeting-access) - Revoke a user's access to a shared meeting by email

  **New Query Field:**

  * `shared_with` on [Transcript](/schema/transcript) - List all users a meeting is shared with, including email, name, and expiry details

  All operations require meeting ownership or team admin privileges.
</Update>

<Update label="2.19.0" description="Channels API">
  ### Channels API

  The Fireflies API now includes support for querying channels. The new [Channels](/graphql-api/query/channels) query allows you to fetch all channels accessible to the user, including public channels and private channels where the user is a member.

  **New Queries:**

  * [channels](/graphql-api/query/channels) - Fetch all accessible channels
  * [channel](/graphql-api/query/channel) - Fetch a single channel by ID

  **New Schemas:**

  * [Channel](/schema/channel) - Channel details including `id`, `title`, `is_private`, `created_at`, `updated_at`, `created_by`, and `members`
  * [ChannelMember](/schema/channel-member) - Channel member details with `user_id`, `email`, and `name`

  Channel access follows privacy rules: users can view all public channels and private channels they are members of. Super admins can view all channels within their team.
</Update>

<Update label="2.17.0" description="Authenticated Audio Downloads">
  ### Authenticated Audio Downloads

  The [Upload Audio](/graphql-api/mutation/upload-audio) mutation now supports authenticated downloads for media files that require authentication. You can now upload audio/video files from private servers or protected storage using bearer token or HTTP basic authentication.

  This feature adds a new `download_auth` field to the `AudioUploadInput` type, allowing you to specify authentication credentials that Fireflies will use when downloading your media file. This is particularly useful for:

  * Files stored in private cloud storage (AWS S3, Google Cloud Storage, Azure Blob Storage)
  * Media hosted on servers with HTTP Basic Auth protection
  * API-protected resources requiring bearer tokens
  * Internal company file servers

  The implementation includes four new schema types:

  * [DownloadAuthInput](/schema/input/download-auth-input) - Main authentication configuration
  * [BearerTokenAuthInput](/schema/input/bearer-token-auth-input) - Bearer token configuration
  * [BasicAuthInput](/schema/input/basic-auth-input) - Basic auth configuration
  * [DownloadAuthType](/schema/enum/download-auth-type) - Authentication type enum

  The feature maintains full backward compatibility - existing uploads without authentication continue to work as before.
</Update>

<Update label="2.16.0" description="AskFred - AI Meeting Assistant">
  ### AskFred - AI Meeting Assistant

  Introducing **AskFred**, an AI-powered assistant that lets you query your meeting transcripts using natural language. Ask questions about single meetings or analyze patterns across multiple meetings with context-aware, conversational responses.

  **Key Capabilities:**

  * Ask questions in plain language and get instant answers
  * Maintain conversation threads with contextual follow-ups
  * Query across multiple meetings with flexible filters
  * Receive AI-generated suggestions for deeper exploration
  * Multilingual question and response support

  **Get Started:**

  * [Overview](/askfred/overview) - Learn about capabilities
  * [Quickstart](/askfred/quickstart) - Create your first thread
  * [Use Cases](/askfred/use-cases) - Common scenarios and examples

  **New API Operations:** [askfred\_threads](/graphql-api/query/askfred-threads), [askfred\_thread](/graphql-api/query/askfred-thread), [createAskFredThread](/graphql-api/mutation/create-askfred-thread), [continueAskFredThread](/graphql-api/mutation/continue-askfred-thread), [deleteAskFredThread](/graphql-api/mutation/delete-askfred-thread)
</Update>

<Update label="2.15.0" description="Set Meeting Channels">
  ### Set Meeting Channels

  The new [Update Meeting Channel](/graphql-api/mutation/update-meeting-channel) mutation allows meeting owners and team administrators to set the channel for one or more meetings. You can update 1–5 transcripts to a single channel in one API call with all-or-nothing semantics.

  This mutation requires either meeting ownership or team admin privileges for all specified transcripts. If any transcript fails validation, none of the transcripts will be updated, ensuring data consistency across your channel organization.
</Update>

<Update label="2.14.0" description="Active Meetings Fetching">
  ### Active Meetings Fetching

  The new [Active Meetings](/graphql-api/query/active-meetings) query allows you to fetch meetings currently in progress. This query returns real-time information about active meetings including meeting details, start time, organizer, and meeting link.
</Update>

<Update label="2.14.0" description="AskFred - AI Meeting Assistant">
  ### AskFred - AI Meeting Assistant

  Introducing **AskFred**, an AI-powered assistant that lets you query your meeting transcripts using natural language. Ask questions about single meetings or analyze patterns across multiple meetings with context-aware, conversational responses.

  **Key Capabilities:**

  * Ask questions in plain language and get instant answers
  * Maintain conversation threads with contextual follow-ups
  * Query across multiple meetings with flexible filters
  * Receive AI-generated suggestions for deeper exploration
  * Multilingual question and response support

  **Get Started:**

  * [Overview](/askfred/overview) - Learn about capabilities
  * [Quickstart](/askfred/quickstart) - Create your first thread
  * [Use Cases](/askfred/use-cases) - Common scenarios and examples

  **New API Operations:** [askfred\_threads](/graphql-api/query/askfred-threads), [askfred\_thread](/graphql-api/query/askfred-thread), [createAskFredThread](/graphql-api/mutation/create-askfred-thread), [continueAskFredThread](/graphql-api/mutation/continue-askfred-thread), [deleteAskFredThread](/graphql-api/mutation/delete-askfred-thread)
</Update>

<Update label="2.13.0" description="Rate Limiting for Delete Transcript">
  ### Rate Limiting for Delete Transcript

  The [Delete Transcript](/graphql-api/mutation/delete-transcript) mutation now includes rate limiting protection to prevent abuse. The mutation is limited to 10 requests per minute across all user tiers.

  If you exceed this limit, the API will return a `too_many_requests` error (HTTP 429) with a `retryAfter` timestamp indicating when you can make requests again.
</Update>

<Update label="2.12.0" description="Meeting Privacy Control">
  ### Meeting Privacy Control

  The new [Update Meeting Privacy](/graphql-api/mutation/update-meeting-privacy) mutation allows meeting owners and team administrators to programmatically update meeting privacy settings. You can now change privacy levels between `link`, `owner`, `participants`, `teammatesandparticipants`, and `teammates` to control who can access meeting transcripts.

  This mutation follows the same authorization pattern as other meeting management operations, requiring either meeting ownership or team admin privileges.
</Update>

<Update label="2.10.0" description="Meeting Attendance Tracking">
  ### Meeting Attendance Tracking

  The [Transcript](/schema/transcript) schema now includes a new `meeting_attendance` field that provides detailed participant attendance information. This field returns an array of [MeetingAttendance](/schema/meeting-attendance) records showing when participants joined and left the meeting.

  Each attendance record includes the participant's name, join time (ISO 8601 format), and leave time (if they left during the meeting). This feature enables better meeting analytics and participation tracking by leveraging meeting events data.

  The attendance data is available in both [Transcript](/graphql-api/query/transcript) and [Transcripts](/graphql-api/query/transcripts) queries.
</Update>

<Update label="2.9.0" description="Channel Filtering">
  ### Channel Filtering

  The [Transcripts](/graphql-api/query/transcripts) query now supports filtering by channel using the new `channel_id` parameter. This allows you to retrieve transcripts from specific channels by providing a single channel ID.

  The `channel_id` parameter accepts a string value and enables more targeted querying of meeting transcripts within your organization's channels.
</Update>

<Update label="2.8.0" description="Array Fields for Organizers and Participants">
  ### Array Fields for Organizers and Participants

  The [Transcripts](/graphql-api/query/transcripts) query now supports array fields `organizers` and `participants` that allow filtering by multiple email addresses. These new array fields provide more flexible querying capabilities while maintaining backward compatibility.

  The previous single email fields `organizer_email` and `participant_email` are now deprecated but continue to work. Using both old and new fields simultaneously will result in a validation error.
</Update>

<Update label="2.7.0" description="User Groups">
  ### User Groups

  The Fireflies API now includes comprehensive support for user groups. The new [User Groups](/graphql-api/query/user-groups) query allows you to fetch all user groups within your team or filter to only show groups you belong to using the `mine` parameter.

  Additionally, the [User](/schema/user) and [Users](/graphql-api/query/users) queries now include enhanced `user_groups` fields with detailed member information, providing better visibility into team organization and collaboration.
</Update>

<Update label="2.6.2" description="Keyword search">
  ### Keyword Search

  The [Transcripts](/graphql-api/query/transcripts) query has been enhanced to include keyword search functionality. By utilizing the `keyword` and `scope` parameters, you can now perform advanced searches within both the title and the transcript text, offering more precise retrieval.

  The `title` parameter has been deprecated in favor of `keyword`
</Update>

<Update label="2.6.1" description="Upload audio">
  ### Enhancements to Audio Upload

  The [Upload Audio](/graphql-api/mutation/upload-audio) function now includes a `bypass_size_check` flag. This enhancement provides greater control over filtering unwanted uploads, such as voicemails from dialers.
</Update>

<Update label="2.6.0" description="Realtime API">
  ### Realtime API

  The Fireflies.ai [Realtime API](/realtime-api/overview) allows your application to receive live transcription events over WebSockets. This enables building interactive features such as live captioning, transcription overlays, and real-time analysis as users speak.
</Update>
