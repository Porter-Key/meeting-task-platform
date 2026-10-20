<!-- Source: https://docs.fireflies.ai/schema/audit-event.md -->
<!-- Title: AuditEvent -->
<!-- Description: Schema for AuditEvent - OCSF-compliant audit event for enterprise teams -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# AuditEvent

> Schema for AuditEvent - OCSF-compliant audit event for enterprise teams

The `AuditEvent` type represents an audit log entry for actions performed within your team. Events conform to the OCSF v1.5.0 standard.

## Fields

<ResponseField name="id" type="String!" required>
  Unique identifier for the event.
</ResponseField>

<ResponseField name="time" type="String!" required>
  When the event occurred (ISO 8601 format).
</ResponseField>

<ResponseField name="category" type="AuditEventCategory!" required>
  High-level category: `MEETING_OPERATIONS`, `TEAM_OPERATIONS`, `USER_OPERATIONS`, or `AUTHENTICATION`.
</ResponseField>

<ResponseField name="action" type="AuditEventAction!" required>
  The specific action that occurred (e.g., `MEETING_DELETED`, `TEAMMATE_ADDED`).
</ResponseField>

<ResponseField name="severity" type="String!" required>
  Event severity: `informational`, `low`, `medium`, `high`, `critical`, `fatal`.
</ResponseField>

<ResponseField name="status" type="String!" required>
  Event outcome: `success` or `failure`.
</ResponseField>

<ResponseField name="message" type="String">
  Human-readable event description.
</ResponseField>

<ResponseField name="class_uid" type="Int!" required>
  OCSF class UID for compliance mapping.
</ResponseField>

<ResponseField name="activity_id" type="Int!" required>
  OCSF activity ID for compliance mapping.
</ResponseField>

<ResponseField name="type_uid" type="Int!" required>
  OCSF type UID, computed as `class_uid * 100 + activity_id`.
</ResponseField>

<ResponseField name="actor" type="AuditEventActor">
  The user who performed the action. Contains `user_id`, and optionally `email`, `full_name` (when `include_pii` is true), and `ip_address`.
</ResponseField>

<ResponseField name="resource" type="AuditEventResource">
  The affected resource with `type` (`meeting` or `team`) and `id`.
</ResponseField>

<ResponseField name="metadata" type="String">
  Additional context as a JSON string of key-value pairs.
</ResponseField>

## Related Types

* [AuditEventCategory](/schema/enum/audit-event-category) - Category enum
* [AuditEventAction](/schema/enum/audit-event-action) - Action enum
* [Audit Events Query](/graphql-api/query/audit-events) - Query documentation
