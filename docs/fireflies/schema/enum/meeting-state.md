<!-- Source: https://docs.fireflies.ai/schema/enum/meeting-state.md -->
<!-- Title: MeetingState -->
<!-- Description: Enum for MeetingState - possible states for active meetings -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# MeetingState

> Enum for MeetingState - possible states for active meetings

The `MeetingState` enum specifies the current state of an active meeting.

## Values

<ParamField path="active" type="Enum Value">
  The meeting is currently in progress with the Fireflies bot actively recording.
</ParamField>

<ParamField path="paused" type="Enum Value">
  The meeting has been paused. The Fireflies bot is still in the meeting but recording is temporarily stopped.
</ParamField>

## Usage

The `MeetingState` enum is used in two contexts:

1. **As a filter** in the [GetActiveMeetingsInput](/schema/input/active-meetings-input) to filter meetings by state
2. **As a response field** in the [ActiveMeeting](/schema/active-meeting) type to indicate the current state

### Filtering by State

```graphql theme={null}
query ActiveMeetings {
  active_meetings(input: { states: [active] }) {
    id
    title
    state
  }
}
```

### Getting All States (Default)

When no `states` filter is provided, both `active` and `paused` meetings are returned:

```graphql theme={null}
query ActiveMeetings {
  active_meetings {
    id
    title
    state
  }
}
```

## Related Types

* [ActiveMeeting](/schema/active-meeting) - Schema containing the state field
* [GetActiveMeetingsInput](/schema/input/active-meetings-input) - Input type using this enum for filtering
* [Active Meetings Query](/graphql-api/query/active-meetings) - Query documentation
