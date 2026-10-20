<!-- Source: https://docs.fireflies.ai/mcp-tools/overview.md -->
<!-- Title: MCP Tools -->
<!-- Description: Complete reference for all available tools in the Fireflies MCP Server -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# MCP Tools

> Complete reference for all available tools in the Fireflies MCP Server

## Overview

The Fireflies MCP (Model Context Protocol) Server provides tools for searching, retrieving, and managing meeting transcripts, summaries, soundbites, channels, and user data. Tools operate within your authenticated Fireflies account — some are read-only while others allow you to take actions like sharing meetings or creating soundbites.

For setup and configuration instructions, see [MCP Server Configuration](/getting-started/mcp-configuration).

## Available Tools

### Meeting & Transcript Tools

<Note>
  `fireflies_search` and `fireflies_fetch` are experimental tools that may not be available to all users. They are being progressively rolled out and may require feature flag enablement.
</Note>

<ParamField path="fireflies_search" type="Tool">
  **Description:** Advanced search for meeting transcripts using mini grammar syntax. *(Experimental)*

  **Parameters:**

  * `query` (string, required) - Search query with grammar syntax
  * `format` (string) - Response format: "toon" (default), "json", or "text"

  **Query Grammar:**

  * `keyword:"term"` - Search keywords
  * `scope:title|sentences|all` - Search scope
  * `from:YYYY-MM-DD` - Filter from date
  * `to:YYYY-MM-DD` - Filter to date
  * `limit:N` - Max results (50)
  * `skip:N` - Pagination offset
  * `organizers:email1,email2` - Filter by organizers
  * `participants:email1,email2` - Filter by participants
  * `mine:true|false` - User's meetings only

  **Example:**

  ```json theme={null}
  {
    "query": "keyword:\"performance\" scope:sentences from:2024-12-01 limit:20"
  }
  ```
</ParamField>

<ParamField path="fireflies_get_transcripts" type="Tool">
  **Description:** Query multiple meetings with structured filters. Returns metadata and summaries.

  **Parameters:**

  * `keyword` (string) - Search term (max 255 chars)
  * `scope` (enum) - "title", "sentences", or "all"
  * `fromDate` (string) - ISO date (YYYY-MM-DD)
  * `toDate` (string) - ISO date (YYYY-MM-DD)
  * `limit` (number) - Max results (max 50)
  * `skip` (number) - Pagination offset
  * `organizers` (array) - Organizer emails
  * `participants` (array) - Participant emails
  * `mine` (boolean) - Only user's meetings
  * `format` (string) - "toon" (default), "json", or "text"

  **Example:**

  ```json theme={null}
  {
    "keyword": "product roadmap",
    "fromDate": "2024-12-01",
    "limit": 20
  }
  ```

  **Returns:** Meeting IDs, titles, dates, participants, summaries (excludes detailed transcript content).
</ParamField>

<ParamField path="fireflies_get_transcript" type="Tool">
  **Description:** Fetch detailed transcript by ID with sentences, speakers, and timestamps. Excludes summary data. If the meeting is currently live (`is_live: true`), returns a point-in-time snapshot of the live transcript with sentences captured so far.

  **Parameters:**

  * `transcriptId` (string, required) - Meeting ID

  **Example:**

  ```json theme={null}
  {
    "transcriptId": "meeting-id-12345"
  }
  ```

  **Returns:** Sentences with speaker attribution, timestamps, analytics, and metadata.
</ParamField>

<ParamField path="fireflies_fetch" type="Tool">
  **Description:** Retrieve complete meeting data including transcript, summary, and metadata. *(Experimental)*

  **Parameters:**

  * `id` (string, required) - Meeting ID

  **Example:**

  ```json theme={null}
  {
    "id": "meeting-id-12345"
  }
  ```

  **Returns:** Complete meeting data with transcript content, summary, analytics, and metadata.
</ParamField>

<ParamField path="fireflies_get_summary" type="Tool">
  **Description:** Fetch meeting summary by ID with action items, keywords, and overview. Excludes transcript content.

  **Parameters:**

  * `transcriptId` (string, required) - Meeting ID

  **Example:**

  ```json theme={null}
  {
    "transcriptId": "meeting-id-12345"
  }
  ```

  **Returns:** Keywords, action items, overview, topics discussed, meeting type, and outline.
</ParamField>

<ParamField path="fireflies_get_active_meetings" type="Tool">
  **Description:** Retrieves a list of currently active (in-progress) meetings. Returns meeting details including ID, title, organizer, meeting link, start/end time, privacy, and state. Admins can query active meetings for any user; regular users can only query their own.

  **Parameters:**

  * `email` (string, optional) - Email address to filter active meetings by a specific user. Admins can query any team member; regular users can only use their own email or omit this field.
  * `states` (array, optional) - Array of meeting states to filter by. Possible values: `"active"` (currently in progress), `"paused"` (meeting has been paused). If omitted, returns meetings in both states.

  **Example:**

  ```json theme={null}
  {
    "email": "user@example.com",
    "states": ["active"]
  }
  ```

  **Returns:** List of active meetings with ID, title, organizer, meeting link, start time, privacy, and state.
</ParamField>

<ParamField path="fireflies_get_analytics" type="Tool">
  **Description:** Retrieves team and per-user meeting and conversation analytics. Returns meeting counts, durations, conversation metrics (filler words, questions, monologues, sentiment, talk-listen ratio, words per minute), and comparison data against previous periods. Team-level analytics require admin privileges.

  **Parameters:**

  * `startTime` (string, optional) - Start date/time filter in ISO 8601 format (e.g. `"2024-01-01T00:00:00.000Z"`). Limits analytics to meetings after this time.
  * `endTime` (string, optional) - End date/time filter in ISO 8601 format (e.g. `"2024-12-31T23:59:59.999Z"`). Limits analytics to meetings before this time.

  **Example:**

  ```json theme={null}
  {
    "startTime": "2024-01-01T00:00:00.000Z",
    "endTime": "2024-12-31T23:59:59.999Z"
  }
  ```

  **Returns:** Team and per-user meeting counts, durations, and conversation metrics with period-over-period comparisons.
</ParamField>

### Meeting Management Tools

<ParamField path="fireflies_share_meeting" type="Tool">
  **Description:** Shares a meeting transcript with specified email addresses. The authenticated user must be the owner of the meeting or a team admin. Up to 100 emails can be provided. Optionally set an expiry period for the shared access.

  **Parameters:**

  * `meetingId` (string, required) - The meeting ID / transcript ID to share
  * `emails` (array, required) - Array of email addresses to share the meeting with (max 100)
  * `expiryDays` (number, optional) - Expiry period in days for the shared access. Must be one of: `7`, `14`, `30`

  **Example:**

  ```json theme={null}
  {
    "meetingId": "meeting-id-12345",
    "emails": ["user1@example.com", "user2@example.com"],
    "expiryDays": 14
  }
  ```

  **Returns:** Confirmation of the sharing operation.
</ParamField>

<ParamField path="fireflies_revoke_meeting_access" type="Tool">
  **Description:** Revokes a previously shared meeting access for a specific email address. The authenticated user must be the owner of the meeting or a team admin.

  **Parameters:**

  * `meetingId` (string, required) - The meeting ID / transcript ID to revoke access from
  * `email` (string, required) - The email address to revoke access for

  **Example:**

  ```json theme={null}
  {
    "meetingId": "meeting-id-12345",
    "email": "user@example.com"
  }
  ```

  **Returns:** Confirmation of the access revocation.
</ParamField>

<ParamField path="fireflies_update_meeting_title" type="Tool">
  **Description:** Updates the title of a meeting transcript. The authenticated user must be the owner of the meeting or a team admin. The title must be between 5 and 256 characters.

  **Parameters:**

  * `meetingId` (string, required) - The meeting ID / transcript ID to update
  * `title` (string, required) - The new title for the meeting (5-256 characters)

  **Example:**

  ```json theme={null}
  {
    "meetingId": "meeting-id-12345",
    "title": "Q1 Product Roadmap Review"
  }
  ```

  **Returns:** Confirmation of the title update.
</ParamField>

<ParamField path="fireflies_move_meeting" type="Tool">
  **Description:** Moves one or more meeting transcripts to a specified channel/folder. The authenticated user must be the owner of the meetings or a team admin. Up to 5 meeting IDs can be provided.

  **Parameters:**

  * `meetingIds` (array, required) - Array of meeting IDs / transcript IDs to move (max 5)
  * `channelId` (string, required) - The target channel/folder ID to move the meetings to

  **Example:**

  ```json theme={null}
  {
    "meetingIds": ["meeting-id-1", "meeting-id-2"],
    "channelId": "channel-id-12345"
  }
  ```

  **Returns:** Confirmation of the move operation.
</ParamField>

### Channel Tools

<ParamField path="fireflies_list_channels" type="Tool">
  **Description:** Lists all channels/folders available to the authenticated user. Returns channel details including ID, title, privacy setting, and members.

  **Parameters:** None

  **Example:**

  ```json theme={null}
  {}
  ```

  **Returns:** List of channels with ID, title, privacy setting, and member details.
</ParamField>

<ParamField path="fireflies_get_channel" type="Tool">
  **Description:** Retrieves details of a specific channel/folder by its ID. Returns channel title, privacy setting, and member list.

  **Parameters:**

  * `channelId` (string, required) - The ID of the channel to retrieve

  **Example:**

  ```json theme={null}
  {
    "channelId": "channel-id-12345"
  }
  ```

  **Returns:** Channel title, privacy setting, and member list.
</ParamField>

### Soundbite Tools

<ParamField path="fireflies_get_soundbites" type="Tool">
  **Description:** Fetches soundbites (short shareable audio/transcript clips from meetings). Can filter by transcript, ownership, or team. At least one of `mine`, `transcript_id`, or `my_team` must be provided.

  **Parameters:**

  * `transcript_id` (string, optional) - Transcript/meeting ID to get soundbites for a specific meeting
  * `mine` (boolean, optional) - Filter to only include soundbites owned by the authenticated user
  * `my_team` (boolean, optional) - Filter to include soundbites from the authenticated user's team
  * `limit` (number, optional) - Limit for the number of soundbites to return (max 50)
  * `skip` (number, optional) - Number of soundbites to skip for pagination
  * `format` (string) - "toon" (default), "json", or "text"

  **Example:**

  ```json theme={null}
  {
    "mine": true,
    "limit": 10
  }
  ```

  **Returns:** List of soundbites with IDs, names, start/end times, summaries, and associated meeting details.
</ParamField>

<ParamField path="fireflies_create_soundbite" type="Tool">
  **Description:** Creates a soundbite (clip) from a meeting transcript. A soundbite is a short audio/video segment extracted from a meeting. The authenticated user must have write access to the meeting.

  **Parameters:**

  * `transcriptId` (string, required) - The transcript ID / meeting ID to create the soundbite from
  * `startTime` (number, required) - Start time of the soundbite in seconds (must be >= 0)
  * `endTime` (number, required) - End time of the soundbite in seconds (must be > 0 and > startTime)
  * `name` (string, optional) - Name/title for the soundbite (max 256 characters)
  * `mediaType` (string, optional) - Media type (e.g. "audio", "video")
  * `privacies` (array, optional) - Privacy settings. Values: `"public"`, `"team"`, `"participants"`
  * `summary` (string, optional) - Summary text for the soundbite (max 500 characters)

  **Example:**

  ```json theme={null}
  {
    "transcriptId": "meeting-id-12345",
    "startTime": 120,
    "endTime": 180,
    "name": "Key product decision"
  }
  ```

  **Returns:** Created soundbite details including ID and share URL.
</ParamField>

### User & Team Tools

<ParamField path="fireflies_get_user" type="Tool">
  **Description:** Fetch user account details. Returns authenticated user if no ID provided.

  **Parameters:**

  * `userId` (string, optional) - User ID (omit for current user)

  **Example:**

  ```json theme={null}
  {
    "userId": "user-id-12345"
  }
  ```

  **Returns:** User ID, email, name, transcript count, recent meeting date, minutes consumed, admin status, and integrations.
</ParamField>

<ParamField path="fireflies_get_usergroups" type="Tool">
  **Description:** Fetch user groups for the authenticated user or team.

  **Parameters:**

  * `mine` (boolean) - true for user's groups only, false (default) for all team groups

  **Example:**

  ```json theme={null}
  {
    "mine": false
  }
  ```

  **Returns:** Group ID, name, handle, members with emails and roles.
</ParamField>

<ParamField path="fireflies_get_user_contacts" type="Tool">
  **Description:** Fetch contact list sorted by most recent meeting date.

  **Parameters:**

  * `format` (string) - "toon" (default), "json", or "text"

  **Example:**

  ```json theme={null}
  {
    "format": "json"
  }
  ```

  **Returns:** Contact emails, names, profile pictures, and last meeting dates.
</ParamField>

### Automation Tools

<ParamField path="fireflies_get_rule_executions" type="Tool">
  **Description:** Retrieves rule execution logs grouped by meeting. Shows which automation rules were triggered on meetings, including the actions taken (sharing, moving to channels, changing privacy). Requires Enterprise tier access. Results are paginated.

  **Parameters:**

  * `ruleId` (string, optional) - Filter by a specific rule ID
  * `meetingId` (string, optional) - Filter by a specific meeting ID
  * `dateFrom` (string, optional) - Filter executions from this date (ISO 8601 format, e.g. `"2024-01-01T00:00:00Z"`)
  * `dateTo` (string, optional) - Filter executions up to this date (ISO 8601 format, e.g. `"2024-12-31T23:59:59Z"`)
  * `limit` (number, optional) - Maximum number of meeting groups to return (default: 10, max: 50)
  * `cursor` (string, optional) - Pagination cursor from a previous response to fetch the next page

  **Example:**

  ```json theme={null}
  {
    "dateFrom": "2024-01-01T00:00:00Z",
    "dateTo": "2024-12-31T23:59:59Z",
    "limit": 20
  }
  ```

  **Returns:** Rule execution logs grouped by meeting, including rule names, actions taken, and execution status.
</ParamField>

## Tool Comparison Matrix

| Tool                              | Content Type      | Summary | Parameters            | Best For                              |
| --------------------------------- | ----------------- | ------- | --------------------- | ------------------------------------- |
| `fireflies_search`                | Multiple meetings | Yes     | Complex grammar       | Advanced filtering with mini grammar  |
| `fireflies_get_transcripts`       | Multiple meetings | Yes     | Structured params     | Structured queries with clear filters |
| `fireflies_get_transcript`        | Single meeting    | No      | Meeting ID only       | Full conversation with timestamps     |
| `fireflies_fetch`                 | Single meeting    | Yes     | Meeting ID only       | Complete meeting data in one call     |
| `fireflies_get_summary`           | Single meeting    | Yes     | Meeting ID only       | Quick insights and action items       |
| `fireflies_get_active_meetings`   | Active meetings   | No      | Optional email/states | Monitoring live meetings              |
| `fireflies_get_analytics`         | Team analytics    | N/A     | Optional date range   | Meeting and conversation metrics      |
| `fireflies_share_meeting`         | Single meeting    | N/A     | Meeting ID + emails   | Sharing access with others            |
| `fireflies_revoke_meeting_access` | Single meeting    | N/A     | Meeting ID + email    | Removing shared access                |
| `fireflies_update_meeting_title`  | Single meeting    | N/A     | Meeting ID + title    | Renaming meetings                     |
| `fireflies_move_meeting`          | Multiple meetings | N/A     | Meeting IDs + channel | Organizing into channels              |
| `fireflies_list_channels`         | Channel list      | N/A     | None                  | Viewing available channels            |
| `fireflies_get_channel`           | Single channel    | N/A     | Channel ID            | Channel details and members           |
| `fireflies_get_soundbites`        | Soundbite list    | N/A     | Filter params         | Browsing meeting clips                |
| `fireflies_create_soundbite`      | Single soundbite  | N/A     | Transcript ID + times | Creating meeting clips                |
| `fireflies_get_user`              | User data         | N/A     | Optional user ID      | Profile and account information       |
| `fireflies_get_usergroups`        | Team data         | N/A     | Optional mine filter  | Team structure and membership         |
| `fireflies_get_user_contacts`     | Contact list      | N/A     | Optional format       | Recent interaction history            |
| `fireflies_get_rule_executions`   | Automation logs   | N/A     | Filter params         | Viewing rule execution history        |

## Response Formats

Several tools support multiple response formats via the `format` parameter:

* **toon** (default) - Token-efficient format optimized for AI model consumption
* **json** - Standard JSON format for programmatic processing
* **text** - Human-readable text format for display

## Common Workflows

### Search and Retrieve Pattern

1. Use `fireflies_search` or `fireflies_get_transcripts` to find relevant meetings
2. Extract meeting IDs from results
3. Use `fireflies_fetch` to get complete details, or:
   * Use `fireflies_get_transcript` for conversation only
   * Use `fireflies_get_summary` for insights only

### Team Analysis Pattern

1. Use `fireflies_get_usergroups` to get team structure
2. Extract member emails from target groups
3. Use `fireflies_get_transcripts` with `participants` filter
4. Optionally use `fireflies_get_user` for individual member details

### Contact-Based Search Pattern

1. Use `fireflies_get_user_contacts` to get contact list
2. Find target contact by name or email
3. Use `fireflies_get_transcripts` with contact email in `participants`
4. Retrieve detailed transcripts or summaries as needed

### Meeting Management Pattern

1. Use `fireflies_get_transcripts` to find meetings to organize
2. Use `fireflies_list_channels` to see available channels
3. Use `fireflies_move_meeting` to move meetings into channels
4. Use `fireflies_update_meeting_title` to rename meetings as needed

### Soundbite Workflow

1. Use `fireflies_get_transcript` to review a meeting's conversation
2. Identify key moments by timestamp
3. Use `fireflies_create_soundbite` to clip important segments
4. Use `fireflies_get_soundbites` to browse existing clips

### Meeting Sharing Pattern

1. Use `fireflies_get_transcripts` to find meetings to share
2. Use `fireflies_share_meeting` to share with external or internal users
3. Use `fireflies_revoke_meeting_access` to remove access when no longer needed

## Getting Started

To use these tools:

1. **Configure MCP Server** - Add Fireflies MCP Server to your AI application
   * Remote server URL: `https://api.fireflies.ai/mcp`
   * Supports OAuth or API key authentication

2. **Authenticate** - Use OAuth flow or provide API key in configuration

3. **Invoke Tools** - Call tools using their standardized names with JSON parameters

For detailed setup instructions, see [MCP Server Configuration](/getting-started/mcp-configuration).

## Additional Resources

<CardGroup cols={2}>
  <Card title="MCP Configuration" icon="gear" href="/getting-started/mcp-configuration">
    Set up the Fireflies MCP Server in your AI application
  </Card>

  <Card title="GraphQL API" icon="code" href="/graphql-api/query/transcripts">
    Direct GraphQL API access for custom integrations
  </Card>

  <Card title="Authorization" icon="lock" href="/fundamentals/authorization">
    Learn about API authentication and security
  </Card>

  <Card title="LLM Development" icon="robot" href="/getting-started/llm-development">
    Enhance AI coding experience with Fireflies data
  </Card>
</CardGroup>
