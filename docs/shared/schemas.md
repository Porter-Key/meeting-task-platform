# GraphQL Schemas

This file summarizes the frontend-facing GraphQL objects. Exact schema introspection is available from `/graphql/`.

GraphQL fields are camelCase.

## JobAccepted

Returned by mutations.

```graphql
type JobAcceptedType {
  jobId: String!
  queueTaskId: String
  command: String!
  status: String!
  meetingIds: [String!]!
}
```

## ApplicationJob

```graphql
type ApplicationJobType {
  id: String!
  queueTaskId: String
  command: String!
  status: String!
  meetingIds: [String!]!
  payload: JSON!
  result: JSON!
  error: String
  createdAt: DateTime
  updatedAt: DateTime
  startedAt: DateTime
  finishedAt: DateTime
  logs(limit: Int = 100): [ApplicationLogType!]!
  progress(limit: Int = 100): JobProgressType!
}
```

## JobProgress

```graphql
type JobProgressType {
  status: String!
  currentStage: String
  currentEvent: String
  currentMessage: String
  currentMeetingId: String
  totalMeetings: Int
  completedMeetings: Int!
  percent: Int
  startedAt: DateTime
  finishedAt: DateTime
  error: String
  events: [JobProgressEventType!]!
  eventCount: Int!
  hasEvents: Boolean!
  isStale: Boolean!
}
```

## Meeting

```graphql
type MeetingType {
  id: String!
  title: String!
  startedAt: DateTime
  endedAt: DateTime
  durationSeconds: Int
  timezone: String
  metadataPayload: JSON!
  createdAt: DateTime
  updatedAt: DateTime
}
```

Progress rows:

```graphql
type MeetingPipelineRunType {
  id: String!
  meetingId: String!
  pipelineName: String!
  stage: String!
  status: String!
  jobId: String
  startedAt: DateTime
  finishedAt: DateTime
  error: String
  metadataPayload: JSON!
}
```

## TaskMasterlist

```graphql
type TaskMasterlistType {
  id: String!
  taskDate: Date
  title: String!
  action: String!
  context: String!
  priority: String!
  status: String!
  originId: String
  originType: String!
  version: Int!
  dueDate: Date
  dueNote: String
  mondayBoardId: String
  mondayGroupId: String
  mondayFieldValues: JSON!
  metadataPayload: JSON!
  assignees: [TaskAssigneeLinkType!]!
  externalLinks: [TaskExternalLinkType!]!
}
```

## Task mutation inputs

```graphql
input TaskAssigneeInput {
  email: String = null
  alias: String = null
  aliasId: String = null
  relation: String! = "assignee"
  confidence: Float! = 1.0
  metadata: JSON = null
}

input TaskCreateInput {
  taskDate: String!
  title: String!
  action: String! = ""
  context: String! = ""
  priority: String! = "medium"
  status: String! = "draft"
  changedBy: String = null
  assignees: [TaskAssigneeInput!] = null
  metadata: JSON = null
}

input TaskUpdateInput {
  taskId: String!
  title: String = null
  action: String = null
  context: String = null
  priority: String = null
  status: String = null
  dueDate: String = null
  dueNote: String = null
  mondayBoardId: String = null
  mondayBoardName: String = null
  mondayGroupId: String = null
  mondayGroupTitle: String = null
  mondaySchemaVersion: String = null
  mondayFieldValues: JSON = null
  assignees: [TaskAssigneeInput!] = null
  changedBy: String = null
}

input MondayTaskFieldsInput {
  taskIds: [String!]!
  mondayBoardId: String = null
  mondayBoardName: String = null
  mondayGroupId: String = null
  mondayGroupTitle: String = null
  mondayFieldValues: JSON = null
  changedBy: String = null
}
```

Task mutation outputs are `TaskMasterlistType` or `[TaskMasterlistType!]!`.

Nested links:

```graphql
type TaskAssigneeLinkType {
  id: String!
  masterlistTaskId: String!
  email: String
  alias: String
  relation: String!
  source: String!
  confidence: Float!
  metadataPayload: JSON!
}

type TaskExternalLinkType {
  id: String!
  masterlistTaskId: String!
  externalSystem: String!
  externalItemId: String
  externalBoardId: String
  externalUrl: String
  syncStatus: String!
  lastSyncedAt: DateTime
  error: String
  metadataPayload: JSON!
}
```

## Monday board schema

```graphql
type MondayBoardSchemaType {
  board: MondayBoardType!
  groups: [MondayGroupType!]!
  columns: [MondayColumnSchemaType!]!
  requiredColumns: [MondayColumnSchemaType!]!
  writableColumns: [MondayColumnSchemaType!]!
}
```

Column schema:

```graphql
type MondayColumnSchemaType {
  id: String!
  mondayBoardId: String!
  mondayColumnId: String!
  title: String!
  type: String
  settingsStr: String
  fieldKey: String
  required: Boolean!
  writable: Boolean!
  valueKind: String!
  options: JSON!
  schemaPayload: JSON!
  settings: JSON!
  rawPayload: JSON!
}
```

Frontend should use `required`, `writable`, `valueKind`, `options`, and `settings` for dynamic form rendering.

## People

People are global identities. `email` is the canonical key for `PersonType`; aliases may optionally attach to an email.

```graphql
type PersonType {
  email: String!
  identityType: String!
  role: String
  isActive: Boolean!
  source: String!
  metadataPayload: JSON!
}

type PersonAliasType {
  id: String!
  alias: String!
  normalizedAlias: String!
  email: String
  source: String!
  confidence: Float!
  metadataPayload: JSON!
}
```

People mutation inputs:

```graphql
input PersonInput {
  email: String!
  identityType: String! = "alias"
  role: String = null
  isActive: Boolean! = true
  source: String! = "manual"
  metadata: JSON = null
}

input PersonAliasInput {
  alias: String!
  email: String = null
  source: String! = "manual"
  confidence: Float! = 1.0
  metadata: JSON = null
}
```

`addPersonEmailAlias(...)` returns JSON from the persisted email-alias row.
