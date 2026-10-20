<!-- Source: https://docs.fireflies.ai/schema/enum/audit-event-category.md -->
<!-- Title: AuditEventCategory -->
<!-- Description: Enum for AuditEventCategory - categories of audit events -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AuditEventCategory

> Enum for AuditEventCategory - categories of audit events

The `AuditEventCategory` enum groups audit events into high-level categories.

## Values

<ParamField path="MEETING_OPERATIONS" type="Enum Value">
  Events related to meetings: deleted, privacy updated, viewed, shared, downloaded.
</ParamField>

<ParamField path="TEAM_OPERATIONS" type="Enum Value">
  Events related to team membership: teammate added or removed.
</ParamField>

<ParamField path="USER_OPERATIONS" type="Enum Value">
  Events related to user or team settings changes.
</ParamField>

<ParamField path="AUTHENTICATION" type="Enum Value">
  Events related to user authentication: login and logout.
</ParamField>

## Usage

Use this enum to filter audit events by category:

```graphql theme={null}
query {
  auditEvents(filters: { category: MEETING_OPERATIONS }) {
    events {
      action
      time
    }
    has_more
  }
}
```

## Related Types

* [AuditEvent](/schema/audit-event) - The audit event type
* [AuditEventAction](/schema/enum/audit-event-action) - Specific action enum
* [Audit Events Query](/graphql-api/query/audit-events) - Query documentation
