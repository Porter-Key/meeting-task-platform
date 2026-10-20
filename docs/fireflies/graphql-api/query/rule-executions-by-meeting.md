<!-- Source: https://docs.fireflies.ai/graphql-api/query/rule-executions-by-meeting.md -->
<!-- Title: Rule Executions by Meeting -->
<!-- Description: Query rule execution logs grouped by meeting for team automation workflows -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Rule Executions by Meeting

> Query rule execution logs grouped by meeting for team automation workflows

## Overview

The `rule_executions_by_meeting` query retrieves rule execution logs grouped by meeting. This allows you to see which automation rules were triggered for each meeting and what actions were taken.

<Note>
  This query requires an **Enterprise** plan. See [pricing](https://fireflies.ai/pricing) for more
  details.
</Note>

## Arguments

<ParamField path="limit" type="Int" default="10">
  Maximum number of meeting groups to return. Must be between 1 and 50.
</ParamField>

<ParamField path="cursor" type="String">
  Pagination cursor for fetching the next page of results. Use the `next_cursor` value from a
  previous response.
</ParamField>

<ParamField path="logs_per_meeting" type="Int" default="5">
  Maximum number of execution logs to return per meeting. Must be between 1 and 20.
</ParamField>

<ParamField path="filters" type="RuleExecutionFiltersInput">
  Optional filters to narrow down the results.

  <Expandable title="Filter properties">
    <ParamField path="rule_id" type="String">
      Filter by a specific rule ID.
    </ParamField>

    <ParamField path="meeting_id" type="String">
      Filter by a specific meeting ID.
    </ParamField>

    <ParamField path="date_from" type="String">
      Filter executions from this date (ISO 8601 format).
    </ParamField>

    <ParamField path="date_to" type="String">
      Filter executions up to this date (ISO 8601 format).
    </ParamField>

    <ParamField path="is_test" type="Boolean">
      Filter by test evaluations. When `true`, returns only test logs. When `false`, returns only production logs. When not provided, returns all logs.
    </ParamField>
  </Expandable>
</ParamField>

## Response Fields

<ResponseField name="meetings" type="[RuleExecutionMeetingGroup]">
  List of meeting groups with their rule executions.

  <Expandable title="Meeting group properties">
    <ResponseField name="meeting_id" type="String">
      The unique identifier of the meeting.
    </ResponseField>

    <ResponseField name="meeting" type="RuleExecutionMeeting">
      Meeting details including `id`, `title`, and `organizer_email`.
    </ResponseField>

    <ResponseField name="resource_attributes" type="RuleExecutionResourceAttributes">
      Additional meeting attributes like `host`, `attendees`, `user_group_ids`, and `host_user_group_ids`.
    </ResponseField>

    <ResponseField name="executions" type="[RuleExecution]">
      List of rule executions for this meeting.

      <Expandable title="Execution properties">
        <ResponseField name="extension_id" type="String">
          The rule ID that was executed.
        </ResponseField>

        <ResponseField name="extension_title" type="String">
          The name of the rule that was executed.
        </ResponseField>

        <ResponseField name="stopped_at" type="String">
          Timestamp when the rule execution completed (ISO 8601 format).
        </ResponseField>

        <ResponseField name="user_name" type="String">
          Name of the meeting organizer.
        </ResponseField>

        <ResponseField name="share" type="RuleExecutionShare">
          Share action details with `group_ids`.
        </ResponseField>

        <ResponseField name="channel" type="RuleExecutionChannel">
          Channel routing action details with `channel_id`.
        </ResponseField>

        <ResponseField name="meeting_privacy" type="RuleExecutionMeetingPrivacy">
          Privacy update action details with `privacy`.
        </ResponseField>
      </Expandable>
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
query RuleExecutionsByMeeting($limit: Int, $filters: RuleExecutionFiltersInput) {
  rule_executions_by_meeting(limit: $limit, filters: $filters) {
    meetings {
      meeting_id
      meeting {
        id
        title
        organizer_email
      }
      executions {
        extension_id
        extension_title
        stopped_at
        user_name
        share {
          group_ids
        }
        channel {
          channel_id
        }
        meeting_privacy {
          privacy
        }
      }
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
      --data '{ "query": "query { rule_executions_by_meeting(limit: 5, filters: { is_test: false }) { meetings { meeting_id meeting { title } executions { extension_title stopped_at } } has_more next_cursor } }" }' \
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
    query: `query RuleExecutionsByMeeting($limit: Int, $filters: RuleExecutionFiltersInput) {
      rule_executions_by_meeting(limit: $limit, filters: $filters) {
        meetings {
          meeting_id
          meeting { title }
          executions { extension_title stopped_at }
        }
        has_more
        next_cursor
      }
    }`,
    variables: {
      limit: 5,
      filters: { is_test: false },
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
  query RuleExecutionsByMeeting($limit: Int, $filters: RuleExecutionFiltersInput) {
    rule_executions_by_meeting(limit: $limit, filters: $filters) {
      meetings {
        meeting_id
        meeting { title }
        executions { extension_title stopped_at }
      }
      has_more
      next_cursor
    }
  }
  '''

  data = {
      'query': query,
      'variables': {
          'limit': 5,
          'filters': { 'is_test': False }
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
          String json = "{\"query\":\"query { rule_executions_by_meeting(limit: 5, filters: { is_test: false }) { meetings { meeting_id meeting { title } executions { extension_title stopped_at } } has_more next_cursor } }\"}";
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
      "rule_executions_by_meeting": {
        "meetings": [
          {
            "meeting_id": "01K8DV541XM97WMGRCX66TPSWG",
            "meeting": {
              "title": "Weekly Team Sync"
            },
            "executions": [
              {
                "extension_title": "Auto-share with Sales Team",
                "stopped_at": "2024-01-15T14:30:00.000Z"
              },
              {
                "extension_title": "Route to #meetings channel",
                "stopped_at": "2024-01-15T14:30:01.000Z"
              }
            ]
          }
        ],
        "has_more": true,
        "next_cursor": "1705329001000_01K8DV541XM97WMGRCX66TPSWG"
      }
    }
  }
  ```
</ResponseExample>

## Pagination

Use cursor-based pagination to fetch additional results:

```graphql theme={null}
query {
  rule_executions_by_meeting(limit: 10, cursor: "1705329001000_01K8DV541XM97WMGRCX66TPSWG") {
    meetings {
      meeting_id
    }
    has_more
    next_cursor
  }
}
```

## Error Codes

List of possible error codes that may be returned by the `rule_executions_by_meeting` query. Full list of error codes can be found [here](/miscellaneous/error-codes).

<Accordion title="paid_required (enterprise)">
  <p>You need to be on an Enterprise plan to query rule execution logs.</p>
</Accordion>

<Accordion title="service_unavailable">
  <p>The rules service is temporarily unavailable. Please try again later.</p>
</Accordion>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Transcripts" icon="link" href="/graphql-api/query/transcripts">
    Querying list of transcripts
  </Card>

  <Card title="Analytics" icon="link" href="/graphql-api/query/analytics">
    Querying meeting analytics
  </Card>
</CardGroup>
