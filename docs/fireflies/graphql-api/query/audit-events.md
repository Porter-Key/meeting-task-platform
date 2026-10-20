<!-- Source: https://docs.fireflies.ai/graphql-api/query/audit-events.md -->
<!-- Title: Audit Events -->
<!-- Description: Query OCSF-compliant audit events for your team — meetings, teammates, and settings changes -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Audit Events

> Query OCSF-compliant audit events for your team — meetings, teammates, and settings changes

## Overview

The `auditEvents` query retrieves audit events for your team. Events follow the [OCSF v1.5.0](https://schema.ocsf.io/) standard and cover meeting operations, team operations, user settings changes, and authentication (login/logout) events.

<Note>
  This query requires an **Enterprise** plan and the requesting user must be a **team admin**. See [pricing](https://fireflies.ai/pricing) for more details.
</Note>

## Supported Events

| Action                    | Category           | Description                                      |
| ------------------------- | ------------------ | ------------------------------------------------ |
| `MEETING_DELETED`         | Meeting Operations | A meeting was deleted                            |
| `MEETING_PRIVACY_UPDATED` | Meeting Operations | Meeting privacy setting was changed              |
| `MEETING_VIEWED`          | Meeting Operations | A meeting summary was viewed                     |
| `MEETING_SHARED`          | Meeting Operations | A meeting was shared with someone                |
| `MEETING_DOWNLOADED`      | Meeting Operations | A meeting transcript or recording was downloaded |
| `TEAMMATE_ADDED`          | Team Operations    | A teammate was added to the team                 |
| `TEAMMATE_REMOVED`        | Team Operations    | A teammate was removed from the team             |
| `SETTINGS_UPDATED`        | User Operations    | Team settings were updated                       |
| `LOGIN`                   | Authentication     | A user logged in                                 |
| `LOGOUT`                  | Authentication     | A user logged out                                |

## Arguments

<ParamField path="limit" type="Int" default="20">
  Maximum number of events to return. Must be between 1 and 50.
</ParamField>

<ParamField path="cursor" type="String">
  Pagination cursor for fetching the next page of results. Use the `next_cursor` value from a
  previous response.
</ParamField>

<ParamField path="filters" type="AuditEventFiltersInput" required>
  Filters for the query. The `category` field is required.

  <Expandable title="Filter properties">
    <ParamField path="category" type="AuditEventCategory" required>
      Event category (required): `MEETING_OPERATIONS`, `TEAM_OPERATIONS`, `USER_OPERATIONS`, or `AUTHENTICATION`.
    </ParamField>

    <ParamField path="action" type="AuditEventAction">
      Filter by a specific action (e.g., `MEETING_DELETED`, `TEAMMATE_ADDED`).
    </ParamField>

    <ParamField path="date_from" type="String">
      Filter events from this date (ISO 8601 format).
    </ParamField>

    <ParamField path="date_to" type="String">
      Filter events up to this date (ISO 8601 format).
    </ParamField>

    <ParamField path="actor_user_id" type="String">
      Filter by the user ID of the user who performed the action.
    </ParamField>

    <ParamField path="actor_email" type="String">
      Filter by the email of the user who performed the action. Resolved to a user ID server-side. Takes precedence over `actor_user_id` if both are provided.
    </ParamField>
  </Expandable>
</ParamField>

## Response Fields

<ResponseField name="events" type="[AuditEvent]">
  List of audit events matching the query.

  <Expandable title="Event properties">
    <ResponseField name="id" type="String">
      Unique identifier for the event.
    </ResponseField>

    <ResponseField name="time" type="String">
      When the event occurred (ISO 8601 format).
    </ResponseField>

    <ResponseField name="category" type="AuditEventCategory">
      Event category: `MEETING_OPERATIONS`, `TEAM_OPERATIONS`, `USER_OPERATIONS`, or `AUTHENTICATION`.
    </ResponseField>

    <ResponseField name="action" type="AuditEventAction">
      The specific action that occurred (e.g., `MEETING_DELETED`).
    </ResponseField>

    <ResponseField name="severity" type="String">
      Event severity level: `informational`, `low`, `medium`, `high`, `critical`, `fatal`.
    </ResponseField>

    <ResponseField name="status" type="String">
      Event outcome: `success` or `failure`.
    </ResponseField>

    <ResponseField name="message" type="String">
      Human-readable description of the event.
    </ResponseField>

    <ResponseField name="class_uid" type="Int">
      OCSF class UID for compliance mapping.
    </ResponseField>

    <ResponseField name="activity_id" type="Int">
      OCSF activity ID for compliance mapping.
    </ResponseField>

    <ResponseField name="type_uid" type="Int">
      OCSF type UID (`class_uid * 100 + activity_id`).
    </ResponseField>

    <ResponseField name="actor" type="AuditEventActor">
      The user who performed the action.

      <Expandable title="Actor properties">
        <ResponseField name="user_id" type="String">
          User ID of the actor.
        </ResponseField>

        <ResponseField name="email" type="String">
          Email address of the actor.
        </ResponseField>

        <ResponseField name="full_name" type="String">
          Full name of the actor.
        </ResponseField>

        <ResponseField name="ip_address" type="String">
          IP address from which the action was performed.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="resource" type="AuditEventResource">
      The resource that was affected.

      <Expandable title="Resource properties">
        <ResponseField name="type" type="String">
          Resource type: `meeting` or `team`.
        </ResponseField>

        <ResponseField name="id" type="String">
          Resource identifier (meeting ID or team ID).
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="metadata" type="String">
      Additional context as a JSON string of key-value pairs (e.g., download type, share details).
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="has_more" type="Boolean">
  Indicates if there are more results available.
</ResponseField>

<ResponseField name="next_cursor" type="String">
  Cursor to use for fetching the next page of results.
</ResponseField>

## Usage Example

```graphql theme={null}
query AuditEvents($limit: Int, $filters: AuditEventFiltersInput!) {
  auditEvents(limit: $limit, filters: $filters) {
    events {
      id
      time
      category
      action
      severity
      status
      message
      actor {
        user_id
        email
        full_name
        ip_address
      }
      resource {
        type
        id
      }
      metadata
    }
    has_more
    next_cursor
  }
}
```

<RequestExample>
  ```bash curl theme={null}
  curl -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_api_key" \
      --data '{ "query": "query { auditEvents(limit: 10, filters: { category: MEETING_OPERATIONS }) { events { id time action actor { user_id } resource { type id } } has_more next_cursor } }" }' \
      https://api.fireflies.ai/graphql
  ```

  ```javascript javascript theme={null}
  const axios = require('axios');

  const url = 'https://api.fireflies.ai/graphql';
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer your_api_key',
  };

  const data = {
    query: `query AuditEvents($limit: Int, $filters: AuditEventFiltersInput) {
      auditEvents(limit: $limit, filters: $filters) {
        events {
          id
          time
          category
          action
          message
          actor { user_id email }
          resource { type id }
        }
        has_more
        next_cursor
      }
    }`,
    variables: {
      limit: 10,
      filters: { category: 'MEETING_OPERATIONS' },
    },
  };

  axios
    .post(url, data, { headers: headers })
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
  ```

  ```python python theme={null}
  import requests

  url = 'https://api.fireflies.ai/graphql'
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
  }

  query = '''
  query AuditEvents($limit: Int, $filters: AuditEventFiltersInput) {
    auditEvents(limit: $limit, filters: $filters) {
      events {
        id
        time
        category
        action
        message
        actor { user_id email }
        resource { type id }
      }
      has_more
      next_cursor
    }
  }
  '''

  data = {
      'query': query,
      'variables': {
          'limit': 10,
          'filters': { 'category': 'MEETING_OPERATIONS' }
      }
  }

  response = requests.post(url, headers=headers, json=data)
  print(response.json())
  ```

  ```java java theme={null}
  import java.net.URI;
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;

  public class ApiRequest {
      public static void main(String[] args) throws Exception {
          HttpClient client = HttpClient.newHttpClient();
          String json = "{\"query\":\"query { auditEvents(limit: 10, filters: { category: MEETING_OPERATIONS }) { events { id time action actor { user_id } resource { type id } } has_more next_cursor } }\"}";
          HttpRequest request = HttpRequest.newBuilder()
                  .uri(URI.create("https://api.fireflies.ai/graphql"))
                  .header("Content-Type", "application/json")
                  .header("Authorization", "Bearer your_api_key")
                  .POST(HttpRequest.BodyPublishers.ofString(json))
                  .build();

          client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
              .thenApply(HttpResponse::body)
              .thenAccept(System.out::println)
              .join();
      }
  }
  ```
</RequestExample>

<ResponseExample>
  ```json Response theme={null}
  {
    "data": {
      "auditEvents": {
        "events": [
          {
            "id": "682e3a1b-f4c2-4d9a-b1e7-8c5d3f2a1b0c",
            "time": "2026-04-25T10:30:00.000Z",
            "category": "MEETING_OPERATIONS",
            "action": "MEETING_SHARED",
            "severity": "informational",
            "status": "success",
            "message": "share_meeting by alice@example.com",
            "actor": {
              "user_id": "user_abc123",
              "email": "alice@example.com",
              "full_name": "Alice Johnson",
              "ip_address": "192.168.1.1"
            },
            "resource": {
              "type": "meeting",
              "id": "01K8DV541XM97WMGRCX66TPSWG"
            },
            "metadata": "{\"shareType\":\"email\",\"inviteeCount\":\"2\"}"
          },
          {
            "id": "7a1c4d5e-2b3f-4a8c-9d0e-1f2a3b4c5d6e",
            "time": "2026-04-25T09:15:00.000Z",
            "category": "MEETING_OPERATIONS",
            "action": "MEETING_DELETED",
            "severity": "informational",
            "status": "success",
            "message": "delete_meeting by bob@example.com",
            "actor": {
              "user_id": "user_def456",
              "email": "bob@example.com",
              "full_name": "Bob Smith",
              "ip_address": null
            },
            "resource": {
              "type": "meeting",
              "id": "01L2XY789ABC"
            },
            "metadata": null
          }
        ],
        "has_more": true,
        "next_cursor": "eyJpZCI6IjdhMWM0ZDVlIn0="
      }
    }
  }
  ```
</ResponseExample>

## Pagination

Use cursor-based pagination to fetch additional results:

```graphql theme={null}
query {
  auditEvents(limit: 20, cursor: "eyJpZCI6IjdhMWM0ZDVlIn0=", filters: { category: MEETING_OPERATIONS }) {
    events {
      id
      time
      action
    }
    has_more
    next_cursor
  }
}
```

## OCSF Compliance

All events conform to the [OCSF v1.5.0](https://schema.ocsf.io/) standard. The `class_uid`, `activity_id`, and `type_uid` fields map directly to OCSF event classification, enabling integration with SIEM tools and compliance pipelines.

| Action                    | OCSF Class             | class\_uid | activity\_id |
| ------------------------- | ---------------------- | ---------- | ------------ |
| `MEETING_DELETED`         | API Activity           | 6003       | 4            |
| `MEETING_PRIVACY_UPDATED` | Entity Management      | 3004       | 3            |
| `MEETING_VIEWED`          | Web Resource Activity  | 6001       | 2            |
| `MEETING_SHARED`          | User Access Management | 3005       | 1            |
| `MEETING_DOWNLOADED`      | Web Resource Activity  | 6001       | 7            |
| `TEAMMATE_ADDED`          | User Access Management | 3005       | 1            |
| `TEAMMATE_REMOVED`        | User Access Management | 3005       | 2            |
| `SETTINGS_UPDATED`        | Entity Management      | 3004       | 3            |
| `LOGIN`                   | Authentication         | 3002       | 1            |
| `LOGOUT`                  | Authentication         | 3002       | 2            |

## Error Codes

List of possible error codes that may be returned by the `auditEvents` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="paid_required (enterprise)">
  <p>You need to be on an Enterprise plan to query audit events.</p>
</Accordion>

<Accordion title="require_elevated_privilege">
  <p>You need to be a team admin to query audit events.</p>
</Accordion>

<Accordion title="service_unavailable">
  <p>The audit service is temporarily unavailable. Please try again later.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcripts" icon="link" href="/graphql-api/query/transcripts">
    Querying list of transcripts
  </Card>

  <Card title="Rule Executions" icon="link" href="/graphql-api/query/rule-executions-by-meeting">
    Querying automation rule executions
  </Card>
</CardGroup>
