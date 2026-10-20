# TaskManagement GraphQL API

Production domain: `https://taskmanage.example.com`

Backend local service: `http://127.0.0.1:8765`

Frontend owns the public reverse proxy. Backend must remain bound to `127.0.0.1`.

## Active endpoints

- `GET /health` — health check.
- `POST /graphql/` — only business API endpoint.
- Django admin may exist for backend operations only.

Old business REST endpoints under `/queries/*` and `/commands/*` are removed. Do not build new UI against them.

## Request shape

```http
POST /graphql/
Content-Type: application/json

{"query":"query { jobs(limit: 1) { id status } }"}
```

GraphQL uses camelCase field names:

- Python `meeting_progress` -> GraphQL `meetingProgress`
- Python `metadata_payload` -> GraphQL `metadataPayload`
- Python `monday_board_schema` -> GraphQL `mondayBoardSchema`
- Python input field `task_date` -> GraphQL `taskDate`
- Python input field `monday_field_values` -> GraphQL `mondayFieldValues`

## Queries

```graphql
query DashboardData {
  meetings(limit: 10) {
    id
    title
    startedAt
    metadataPayload
  }

  jobs(limit: 5) {
    id
    command
    status
    meetingIds
    logs(limit: 5) { id event stage message correlationId }
    progress(limit: 20) {
      status
      percent
      eventCount
      currentEvent
      currentMessage
      events { id event stage message meetingId payload }
    }
  }

  taskMasterlist(limit: 20) {
    id
    title
    action
    context
    priority
    status
    taskDate
    mondayBoardId
    mondayGroupId
    mondayFieldValues
    metadataPayload
    assignees { id email alias relation source confidence }
    externalLinks { id externalSystem externalItemId externalBoardId externalUrl syncStatus error }
  }
}
```

Other query entrypoints:

- `meeting(id: String!)`
- `meetingProgress(meetingId: String!, limit: Int = 100)`
- `job(id: String!)`
- `logs(limit: Int = 100, meetingId: String, correlationId: String)`
- `mondayBoards(activeOnly: Boolean = true, limit: Int = 200)`
- `mondayBoardSchema(boardId: String!, includeArchivedGroups: Boolean = false)`
- `todayReviewBundle(fromDate: String!, toDate: String!, includeArchived: Boolean = false)`

## Today review bundle

Use this single query for the Today review page. It returns tasks grouped as Date → Owner → Meeting → Tasks, includes people referenced by owners, includes only Monday board schemas used by returned tasks, and includes readiness per task.

```graphql
query TodayReviewBundle($fromDate: String!, $toDate: String!) {
  todayReviewBundle(fromDate: $fromDate, toDate: $toDate) {
    fromDate
    toDate
    dates {
      date
      groups {
        email
        aliasId
        resolved
        meetings {
          meetingId
          meetingTitle
          tasks { id title taskDate mondayBoardName mondayGroupTitle mondayFieldValues }
        }
      }
    }
    people { email identityType role isActive }
    mondayBoards {
      boardId
      name
      workspaceName
      groups { mondayGroupId title }
      columns { mondayColumnId title type required writable valueKind options settings schemaPayload }
    }
    readinessByTaskId
  }
}
```

## Monday schema query

Use this to dynamically render board/group/column forms.

```graphql
query MondayBoardSchema($boardId: String!) {
  mondayBoardSchema(boardId: $boardId) {
    board { mondayBoardId name state }
    groups { mondayGroupId title archived deleted }
    columns {
      mondayColumnId
      title
      type
      fieldKey
      required
      writable
      valueKind
      options
      settings
      schemaPayload
    }
    requiredColumns { mondayColumnId title }
    writableColumns { mondayColumnId title valueKind }
  }
}
```

Frontend rules:

- Use `writable=false` to disable a column.
- Use `required=true` for validation hints.
- Use `valueKind`, `options`, `settings`, and `schemaPayload` to render inputs.
- Do not infer business target board/group automatically; let user select.

## Job mutations

Meeting/process mutations create a job and enqueue Celery. Poll `job(id)` or `jobs` afterwards.

```graphql
mutation RunMeetingPipeline($meetingId: String!) {
  triggerMeetingPipeline(meetingId: $meetingId) {
    jobId
    queueTaskId
    command
    status
    meetingIds
  }
}
```

Available job mutations:

- `triggerMeetingPipeline(meetingId: String!)`
- `triggerGenerateEvents(meetingId: String!)`
- `triggerWashMeeting(meetingId: String!)`
- `deleteMeeting(meetingId: String!)`

## Task masterlist mutations

Task masterlist mutations write immediately through Django ORM and return the updated task rows. They do not enqueue Celery by themselves.

Create a task:

```graphql
mutation CreateTask($input: TaskCreateInput!) {
  createTaskMasterlistItem(input: $input) {
    id
    title
    status
    priority
    mondayFieldValues
    assignees { email alias relation }
  }
}
```

Variables:

```json
{
  "input": {
    "taskDate": "2026-05-24",
    "title": "Review marketplace listing",
    "action": "Check PDP images and bullets",
    "context": "Weekly PPC review",
    "priority": "medium",
    "status": "draft",
    "changedBy": "frontend",
    "assignees": [
      { "email": "owner@example.com", "alias": "Jane Doe" }
    ],
    "metadata": { "source": "manual" }
  }
}
```

Update a task:

```graphql
mutation UpdateTask($input: TaskUpdateInput!) {
  updateTaskMasterlistItem(input: $input) {
    id
    title
    status
    priority
    dueDate
    dueNote
    mondayBoardId
    mondayGroupId
    mondayFieldValues
  }
}
```

Set selected Monday target/fields for one or more tasks:

```graphql
mutation SetMondayFields($input: MondayTaskFieldsInput!) {
  setTaskMondayFields(input: $input) {
    id
    mondayBoardId
    mondayGroupId
    mondayFieldValues
  }
}
```

Variables:

```json
{
  "input": {
    "taskIds": ["task_123"],
    "mondayBoardId": "10056827885",
    "mondayBoardName": "PPC",
    "mondayGroupId": "topics",
    "mondayGroupTitle": "TODAY - Focus Group",
    "mondayFieldValues": {
      "status": "Working",
      "priority": "High",
      "due_date": "2026-05-28"
    },
    "changedBy": "frontend"
  }
}
```

Bulk state changes:

```graphql
mutation ArchiveTasks($ids: [String!]!) {
  archiveTaskMasterlistItems(taskIds: $ids, changedBy: "frontend") { id status }
}

mutation RestoreTasks($ids: [String!]!) {
  restoreTaskMasterlistItems(taskIds: $ids, changedBy: "frontend", status: "saved") { id status }
}

mutation SubmitTasks($ids: [String!]!) {
  submitTaskMasterlistItems(taskIds: $ids, changedBy: "frontend") { id status }
}
```

Available task mutations:

- `createTaskMasterlistItem(input: TaskCreateInput!)`
- `updateTaskMasterlistItem(input: TaskUpdateInput!)`
- `setTaskMondayFields(input: MondayTaskFieldsInput!)`
- `archiveTaskMasterlistItems(taskIds: [String!]!, changedBy: String)`
- `restoreTaskMasterlistItems(taskIds: [String!]!, changedBy: String, status: String = "saved")`
- `submitTaskMasterlistItems(taskIds: [String!]!, changedBy: String)`

Frontend rules:

- Use `mondayBoardSchema(boardId)` to render available groups/columns before writing Monday fields.
- Do not infer the target board/group from task content; user selects the target.
- `mondayFieldValues` is stored as JSON using the UI's selected column/value payload.

## People mutations

People directory is global, not meeting-scoped.

```graphql
mutation UpsertPerson {
  upsertPerson(input: {
    email: "owner@example.com"
    identityType: "fireflies"
    role: "admin"
    source: "frontend"
  }) {
    email
    identityType
    role
    isActive
    source
  }
}
```

```graphql
mutation UpsertPersonAlias {
  upsertPersonAlias(input: {
    alias: "Jane Doe"
    email: "owner@example.com"
    source: "frontend"
    confidence: 1.0
  }) {
    id
    alias
    normalizedAlias
    email
    source
    confidence
  }
}
```

```graphql
mutation AddEmailAlias {
  addPersonEmailAlias(
    ownerEmail: "owner@example.com"
    aliasEmail: "janedoe2323@example.com"
    isPrimary: false
    source: "frontend"
  )
}
```

Available people mutations:

- `upsertPerson(input: PersonInput!)`
- `upsertPersonAlias(input: PersonAliasInput!)`
- `addPersonEmailAlias(ownerEmail: String!, aliasEmail: String!, isPrimary: Boolean = false, source: String = "manual", metadata: JSON)`

## Lifecycle model

Meeting lifecycle is recorded as `MeetingPipelineRun` rows and exposed through `meetingProgress`.

Current main stages:

```text
ingested -> washed -> event_generation
```

Jobs have their own status and progress:

```graphql
query JobProgress($id: String!) {
  job(id: $id) {
    id
    status
    progress {
      percent
      currentStage
      currentEvent
      currentMessage
      events { stage event message }
    }
  }
}
```

## Smoke examples

```bash
curl -fsS http://127.0.0.1:8765/health
```

```bash
curl -fsS -X POST http://127.0.0.1:8765/graphql/ \
  -H 'Content-Type: application/json' \
  -H 'Host: taskmanage.example.com' \
  --data '{"query":"{ jobs(limit: 1) { id status progress { percent eventCount } } }"}'
```
