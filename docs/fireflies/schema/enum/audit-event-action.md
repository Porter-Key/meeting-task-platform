<!-- Source: https://docs.fireflies.ai/schema/enum/audit-event-action.md -->
<!-- Title: AuditEventAction -->
<!-- Description: Enum for AuditEventAction - specific audit event actions -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AuditEventAction

> Enum for AuditEventAction - specific audit event actions

The `AuditEventAction` enum identifies the specific action that triggered an audit event.

## Values

<ParamField path="MEETING_DELETED" type="Enum Value">
  A meeting was deleted.
</ParamField>

<ParamField path="MEETING_PRIVACY_UPDATED" type="Enum Value">
  A meeting's privacy setting was changed.
</ParamField>

<ParamField path="MEETING_VIEWED" type="Enum Value">
  A meeting summary was viewed.
</ParamField>

<ParamField path="MEETING_SHARED" type="Enum Value">
  A meeting was shared with another user.
</ParamField>

<ParamField path="MEETING_DOWNLOADED" type="Enum Value">
  A meeting transcript or recording was downloaded.
</ParamField>

<ParamField path="TEAMMATE_ADDED" type="Enum Value">
  A user was added to the team.
</ParamField>

<ParamField path="TEAMMATE_REMOVED" type="Enum Value">
  A user was removed from the team.
</ParamField>

<ParamField path="SETTINGS_UPDATED" type="Enum Value">
  Team settings were updated.
</ParamField>

<ParamField path="LOGIN" type="Enum Value">
  A user logged in.
</ParamField>

<ParamField path="LOGOUT" type="Enum Value">
  A user logged out.
</ParamField>

## Usage

Use this enum to filter audit events by specific action:

```graphql theme={null}
query {
  auditEvents(filters: { category: MEETING_OPERATIONS, action: MEETING_DELETED }) {
    events {
      time
      actor { user_id }
      resource { id }
    }
    has_more
  }
}
```

## Related Types

* [AuditEvent](/schema/audit-event) - The audit event type
* [AuditEventCategory](/schema/enum/audit-event-category) - Category enum
* [Audit Events Query](/graphql-api/query/audit-events) - Query documentation
