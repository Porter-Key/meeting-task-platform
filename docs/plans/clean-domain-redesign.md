# Clean Domain Redesign Plan

Status: proposed architecture plan. No backward compatibility. No ambiguous legacy semantics.

## Core rules

- `people` is a special canonical database object.
- `people.email` is the only person identity.
- Human names, speaker labels, LLM owner text, and nicknames are aliases, not people.
- `meetings` only represents canonical meeting events.
- Provider payloads, transcripts, pipeline status, people links, topics, conclusions, and task origins do not live on `meetings`.
- `task_origins` is the initialization source for work items.
- `task_masterlist` is Reviewer's saved working task list.
- Monday or any future external push reads only from `task_masterlist`.
- All person relationships use link tables. Do not put `person_name`, `display_name`, `person_id`, or `assignee_email` on master objects.

## Delete / replace legacy concepts

Remove these semantics, not just hide them:

- `people.id`
- `people.display_name`
- `people.aliases`
- `daily_tasks`
- `daily_task_versions`
- `meeting_people_tasks`
- `meeting_people_task_versions`
- `daily_tasks.person_id`
- `daily_tasks.person_name`
- `meetings.source`
- `meetings.date_string`
- `meetings.raw_payload`
- `meetings.raw_summary`
- `meetings.transcript_url`
- `meeting_lifecycles`

Replace with:

- `people`
- `person_aliases`
- `meetings`
- `meeting_sources`
- `meeting_transcripts`
- `meeting_chunks`
- `meeting_person_links`
- `meeting_pipeline_runs`
- `meeting_topics`
- `meeting_conclusions`
- `task_origins`
- `task_masterlist`
- `task_assignee_links`
- `task_versions`
- `task_external_links`

## People schema

### `people`

```sql
people (
  email text primary key,
  role text null,
  is_active boolean not null default true,
  source text not null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

### `person_aliases`

```sql
person_aliases (
  id text primary key,
  alias text not null,
  normalized_alias text not null unique,
  email text null references people(email),
  source text not null,
  confidence double precision not null default 1,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

Rules:

- `email is null` means unresolved alias.
- Unresolved aliases never become `people` rows.
- LLM output may create aliases, but may not create canonical people unless an email is present.
- No fuzzy merge unless explicitly added later as a separate manual workflow.

## Meeting schema

### `meetings`

```sql
meetings (
  id text primary key,
  title text not null,
  started_at timestamptz null,
  ended_at timestamptz null,
  duration_seconds int null,
  timezone text null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

### `meeting_sources`

```sql
meeting_sources (
  id text primary key,
  meeting_id text not null references meetings(id) on delete cascade,
  provider text not null,
  provider_record_id text not null,
  provider_url text null,
  raw_payload jsonb not null default '{}',
  sync_status text not null,
  synced_at timestamptz null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  unique(provider, provider_record_id)
)
```

Provider examples: `fireflies`, `zoom`, `google_meet`, `manual_import`.

### `meeting_transcripts`

```sql
meeting_transcripts (
  id text primary key,
  meeting_id text not null references meetings(id) on delete cascade,
  source_id text null references meeting_sources(id),
  format text not null,
  content text null,
  segments jsonb null,
  language text null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

### `meeting_chunks`

```sql
meeting_chunks (
  id text primary key,
  meeting_id text not null references meetings(id) on delete cascade,
  transcript_id text null references meeting_transcripts(id),
  chunk_index int not null,
  speaker_alias_id text null references person_aliases(id),
  text text not null,
  start_ms int null,
  end_ms int null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  unique(meeting_id, chunk_index)
)
```

### `meeting_person_links`

```sql
meeting_person_links (
  id text primary key,
  meeting_id text not null references meetings(id) on delete cascade,
  email text null references people(email),
  alias_id text null references person_aliases(id),
  relation text not null,
  source text not null,
  confidence double precision not null default 1,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  check (email is not null or alias_id is not null)
)
```

Allowed `relation` values:

```text
host
organizer
participant
speaker
mentioned
```

### `meeting_pipeline_runs`

```sql
meeting_pipeline_runs (
  id text primary key,
  meeting_id text not null references meetings(id) on delete cascade,
  pipeline_name text not null,
  stage text not null,
  status text not null,
  job_id text null references application_jobs(id),
  started_at timestamptz null,
  finished_at timestamptz null,
  error text null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

Pipeline state is derived from latest runs. Do not store lifecycle on `meetings`.

### `meeting_topics`

```sql
meeting_topics (
  id text primary key,
  meeting_id text not null references meetings(id) on delete cascade,
  topic_index int not null,
  title text not null,
  summary text not null,
  source_chunk_indexes jsonb not null default '[]',
  confidence double precision not null default 0,
  payload jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  unique(meeting_id, topic_index)
)
```

### `meeting_conclusions`

```sql
meeting_conclusions (
  id text primary key,
  meeting_id text not null references meetings(id) on delete cascade,
  title text not null,
  summary text not null,
  one_sentence_summary text null,
  tl_dr jsonb not null default '[]',
  source_topic_indexes jsonb not null default '[]',
  source_chunk_indexes jsonb not null default '[]',
  confidence double precision not null default 0,
  payload jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

## Task schema

### `task_origins`

```sql
task_origins (
  id text primary key,
  origin_type text not null,
  meeting_id text null references meetings(id),
  conclusion_id text null references meeting_conclusions(id),
  title text not null,
  action text not null,
  context text not null,
  priority text not null,
  owner_alias_id text null references person_aliases(id),
  assignment_reason text null,
  source_topic_indexes jsonb not null default '[]',
  source_chunk_indexes jsonb not null default '[]',
  source_quote text null,
  payload jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

Allowed `origin_type` values:

```text
meeting_conclusion
manual
import
api
```

Rules:

- `task_origins` is source material for initialization.
- `task_origins` is not the frontend working list.
- Reviewer edits do not mutate `task_origins`.
- Monday or other external sync never reads from `task_origins`.

### `task_masterlist`

```sql
task_masterlist (
  id text primary key,
  task_date date not null,
  title text not null,
  action text not null,
  context text not null,
  priority text not null,
  status text not null,
  origin_id text null references task_origins(id),
  origin_type text not null,
  version int not null default 1,
  saved_by text null,
  saved_at timestamptz null,
  submitted_by text null,
  submitted_at timestamptz null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

Rules:

- `task_masterlist` is the frontend UI save target.
- Initial rows are created from `meeting_conclusions -> task_origins`.
- Reviewer edits and saves `task_masterlist`.
- Monday or future external systems push from `task_masterlist` only.
- Do not store assignee/person/external fields directly on `task_masterlist`.

Allowed `status` values:

```text
draft
saved
submitted
rejected
archived
```

### `task_assignee_links`

```sql
task_assignee_links (
  id text primary key,
  masterlist_task_id text not null references task_masterlist(id) on delete cascade,
  email text null references people(email),
  alias_id text null references person_aliases(id),
  relation text not null,
  source text not null,
  confidence double precision not null default 1,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  check (email is not null or alias_id is not null)
)
```

Allowed `relation` values:

```text
assignee
collaborator
reviewer
mentioned
```

### `task_versions`

```sql
task_versions (
  id text primary key,
  masterlist_task_id text not null references task_masterlist(id) on delete cascade,
  version int not null,
  change_type text not null,
  changed_by text null,
  changed_at timestamptz not null,
  snapshot jsonb not null default '{}',
  patch jsonb not null default '{}'
)
```

Allowed `change_type` values:

```text
initialized
saved
submitted
rejected
archived
```

### `task_external_links`

```sql
task_external_links (
  id text primary key,
  masterlist_task_id text not null references task_masterlist(id) on delete cascade,
  external_system text not null,
  external_item_id text null,
  external_board_id text null,
  external_url text null,
  sync_status text not null,
  last_synced_at timestamptz null,
  error text null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  unique(masterlist_task_id, external_system)
)
```

Allowed `sync_status` values:

```text
pending
pushed
failed
```

## Data flow

```text
Fireflies ingest
  -> meetings
  -> meeting_sources
  -> meeting_transcripts
  -> people / person_aliases
  -> meeting_person_links

Wash
  -> meeting_chunks

Generate
  -> meeting_topics
  -> meeting_conclusions
  -> task_origins
  -> task_masterlist initial draft rows
  -> task_assignee_links
  -> task_versions initialized

Frontend Save
  -> task_masterlist
  -> task_assignee_links
  -> task_versions saved

Push to Monday / other
  -> read task_masterlist
  -> task_external_links
  -> task_masterlist.status = submitted
  -> task_versions submitted
```

## API plan

### People

```http
GET  /queries/people
POST /commands/people
GET  /queries/person-aliases/resolve
POST /commands/person-aliases/map
```

### Meetings

```http
GET /queries/meetings
GET /queries/meetings/{meeting_id}
GET /queries/meetings/{meeting_id}/sources
GET /queries/meetings/{meeting_id}/transcripts
GET /queries/meetings/{meeting_id}/chunks
GET /queries/meetings/{meeting_id}/topics
GET /queries/meetings/{meeting_id}/conclusions
GET /queries/meetings/{meeting_id}/person-links
GET /queries/meetings/{meeting_id}/pipeline-runs
GET /queries/meetings/{meeting_id}/task-origins
```

`GET /queries/meetings` is always PSQL-only. Fireflies refresh is only by scheduled Beat or explicit ingest command.

### Task masterlist

```http
GET    /queries/task-masterlist?date=YYYY-MM-DD
GET    /queries/task-masterlist/{task_id}
POST   /commands/task-masterlist
POST   /commands/task-masterlist/from-origin
POST   /commands/task-masterlist/{task_id}/save
POST   /commands/task-masterlist/{task_id}/submit
POST   /commands/task-masterlist/{task_id}/assignees
DELETE /commands/task-masterlist/{task_id}/assignees/{link_id}
GET    /queries/task-masterlist/{task_id}/versions
GET    /queries/task-masterlist/{task_id}/external-links
```

## Package placement

```text
app/
  HTTP routes only

orchestration/
  Celery task orchestration only

src/application/people/
  people commands, resolver, alias mapping

src/application/meeting/
  ingest, transcript, wash/chunk, generated artifacts

src/application/task_masterlist/
  origin -> masterlist initialization, save, submit, assignment

src/application/query/
  read-only query composition

src/application/repo/psql/
  table-specific persistence repos
```

## Migration strategy

Because no compatibility is desired:

1. Add new ORM/table definitions.
2. Replace repos and routes to use only new names.
3. Replace generate pipeline persistence to write `task_origins` and `task_masterlist`.
4. Replace frontend task query/save/submit routes.
5. Replace Fireflies ingest persistence to write `meeting_sources`, `meeting_transcripts`, and links.
6. Run real-data migration or clear/rebuild local generated data.
7. Delete old ORM classes, old repos, old routes, old docs.

Do not dual-write old and new tables.

## Current implementation status

Updated: 2026-05-13

Done in current rewrite:

- Clean ORM definitions exist for people, meeting source/transcript/chunk/link/run artifacts, `task_origins`, `task_masterlist`, assignee/version/external-link tables.
- Fireflies ingest writes canonical `meetings`, `meeting_sources`, and `meeting_transcripts`.
- Wash writes `meeting_chunks`.
- Generate writes `meeting_topics`, `meeting_conclusions`, `task_origins`, and initializes `task_masterlist`.
- Query API now exposes:
  - `GET /queries/meetings/{meeting_id}/sources`
  - `GET /queries/meetings/{meeting_id}/transcripts`
  - `GET /queries/meetings/{meeting_id}/person-links`
  - `GET /queries/meetings/{meeting_id}/pipeline-runs`
  - `GET /queries/meetings/{meeting_id}/task-origins`
  - `GET /queries/task-masterlist?date=YYYY-MM-DD`
  - `GET /queries/task-masterlist/range?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD`
  - `GET /queries/task-masterlist/archive?date=YYYY-MM-DD`
  - `GET /queries/task-masterlist/{task_id}`
  - `GET /queries/task-masterlist/{task_id}/versions`
  - `GET /queries/task-masterlist/{task_id}/external-links`
- Command API now exposes clean task-masterlist routes:
  - `POST /commands/task-masterlist/create`
  - `POST /commands/task-masterlist/update`
  - `POST /commands/task-masterlist/bind-due-date`
  - `POST /commands/task-masterlist/clear-due-date`
  - `POST /commands/task-masterlist/archive`
  - `POST /commands/task-masterlist/restore`
  - `POST /commands/task-masterlist/submit`
- `task_masterlist.due_date` is a nullable deadline return/display field only; it does not change the row's primary `task_date` masterlist ownership. `due_note` is optional.
- Real HTTP + Celery E2E passed on a previously unprocessed meeting:
  - Meeting `01KQCVENNR5RA3A8VS6RAWWVR0` / `Weekly PPC Meeting`
  - Before: `chunks=0`, `topics=0`, `conclusions=0`, `task_origins=0`
  - After: `chunks=549`, `topics=25`, `conclusions=1`, `task_origins=10`, `task_masterlist.created=10`
  - Final tested task `6a76c4cd-d21f-42fe-8100-9373e7e4a0de` reached `submitted`, version `3`, with one external link.

Known remaining cleanup:

- Meeting person links are queryable but ingest/person extraction still needs final clean link-writing pass.
