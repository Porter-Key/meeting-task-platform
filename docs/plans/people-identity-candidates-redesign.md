# People Identity, Alias, Anonymous, and AI Candidate Plan

Status: accepted implementation plan. No compatibility requirement for legacy `person_name`, `display_name`, or `person_id` semantics.

## Goals

- Preserve Fireflies-derived emails as immutable facts.
- Use email as the only persisted owner/assignee key.
- Support manually managed alias emails and primary alias selection.
- Support generated anonymous emails for AI-discovered people that are not yet in the database.
- Give the AI a numbered people candidate list from the fact layer; AI must select `owner_ref` and must not invent emails.
- Make human cleanup possible through HTTP people commands.

## Identity model

### `people`

`people.email` remains the primary key. Add identity semantics:

```sql
people (
  email text primary key,
  identity_type text not null, -- fireflies | alias | anonymous
  role text null,
  source text not null,        -- fireflies_ingest | manual | anonymous_generated | import
  is_active boolean not null default true,
  metadata_payload jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

Rules:

- `identity_type=fireflies`: immutable Fireflies identity. Do not mutate the email value. A correction creates an alias, not an update.
- `identity_type=alias`: manually managed alias email.
- `identity_type=anonymous`: temporary/generated identity such as `alex-lee@anonymous.local`.
- Anonymous emails use `.anonymous.local`, not a public real domain.

### `person_aliases`

Human names, speaker labels, nicknames, and LLM owner strings map to an email identity.

```sql
person_aliases (
  id text primary key,
  alias text not null,
  normalized_alias text unique not null,
  email text null references people(email),
  source text not null,
  confidence float not null default 1.0,
  metadata_payload jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null
)
```

Examples:

- `"jane doe" -> owner@example.com`
- `"Alex Lee" -> alex-lee@anonymous.local`

### `person_email_aliases`

Email identities can have email aliases. One owner can have multiple alias emails and one primary alias.

```sql
person_email_aliases (
  id text primary key,
  owner_email text not null references people(email),
  alias_email text not null references people(email),
  is_primary boolean not null default false,
  source text not null, -- manual | anonymous_generated | import
  metadata_payload jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  unique(owner_email, alias_email)
)
```

Rules:

- `owner_email` is the durable identity being aliased. It may be Fireflies, alias, or anonymous.
- `alias_email` must exist in `people`; create it first if needed.
- Setting `is_primary=true` unsets other primary aliases for that `owner_email`.
- Removing an alias relation does not delete either people row.

### `meeting_people_candidates`

The fact layer snapshots numbered owner candidates per meeting/run for AI owner selection.

```sql
meeting_people_candidates (
  id text primary key,
  meeting_id text not null references meetings(id) on delete cascade,
  pipeline_run_id text null references meeting_pipeline_runs(id),
  ref text not null, -- P1, P2, P3...
  email text not null references people(email),
  alias_id text null references person_aliases(id),
  identity_type text not null, -- fireflies | alias | anonymous
  display_label text not null,
  sources jsonb not null default '[]',
  confidence float not null default 1.0,
  metadata_payload jsonb not null default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  unique(meeting_id, ref),
  unique(meeting_id, email)
)
```

Candidate sources include:

- Fireflies participants, host, organizer.
- Speaker labels from transcript.
- `person_aliases` matches.
- Primary `person_email_aliases` for Fireflies identities.
- Existing anonymous identities.
- Newly generated anonymous identities for unresolved speaker names or AI owner strings.

## Resolution rules

Given owner input from transcript/fact/AI:

1. If input is an email:
   - Upsert `people` by email.
   - If from Fireflies ingest, use `identity_type=fireflies`.
   - If manual/API, use `identity_type=alias` unless explicitly anonymous.
2. If input is a name/speaker label:
   - Normalize and look up `person_aliases.normalized_alias`.
   - If alias resolves to email, use that email.
   - If the email is a Fireflies identity and has a primary alias, use the primary alias email for task ownership.
3. If unresolved and anonymous creation is allowed:
   - Generate stable email from normalized name: `<slug>@anonymous.local`.
   - Upsert `people(identity_type=anonymous, source=anonymous_generated)`.
   - Map `person_aliases(alias -> anonymous_email)`.
4. If still unresolved:
   - Return unresolved state; do not create fake canonical people.

Task ownership persistence:

```text
task_assignee_links.email = resolved effective email
task_assignee_links.alias_id = matched alias id when available
task_assignee_links.metadata.owner_ref = Pn when selected through fact candidates
```

## Fact layer and AI contract

Before task extraction/owner assignment, build and persist candidates:

```json
{
  "people_candidates": [
    {
      "ref": "P1",
      "email": "owner@example.com",
      "identity_type": "alias",
      "is_primary_alias": true,
      "owner_email": "janedoe2323@example.com",
      "aliases": ["jane doe", "Jane Doe"],
      "sources": ["fireflies_organizer", "person_email_aliases"],
      "confidence": 1.0
    },
    {
      "ref": "P2",
      "email": "alex-lee@anonymous.local",
      "identity_type": "anonymous",
      "aliases": ["Alex Lee", "Liza"],
      "sources": ["speaker_name", "person_aliases"],
      "confidence": 0.7
    }
  ]
}
```

AI prompt rule:

```text
Choose task owners only from PEOPLE_CANDIDATES by owner_ref.
Do not output email as owner.
Do not invent people or emails.
If no candidate fits, set owner_ref=null and unknown_owner_text to the exact phrase from the transcript.
```

AI output shape:

```json
{
  "people_tasks": [
    {
      "owner_ref": "P2",
      "unknown_owner_text": null,
      "assignment_reason": "...",
      "tasks": []
    }
  ]
}
```

Post-processing:

```text
if owner_ref exists:
  candidate = meeting_people_candidates[owner_ref]
  owner_email = candidate.email
else if unknown_owner_text exists:
  owner_email = resolve_or_create_anonymous(unknown_owner_text)
```

AI must never provide the canonical email directly.

## HTTP APIs

### Queries

#### `GET /queries/people`

```http
GET /queries/people?identity_type=fireflies|alias|anonymous&include_inactive=false&limit=200
```

Returns people with alias summaries and primary alias email.

#### `GET /queries/people/{email}`

Returns one identity, email aliases, and name aliases.

#### `GET /queries/people/resolve?value=...`

Read-only resolution. Does not create anonymous identities.

#### `GET /queries/meetings/{meeting_id}/people-candidates`

Returns persisted `meeting_people_candidates` for debug/frontend inspection.

### Commands

#### `POST /commands/people/upsert-fireflies-email`

Create/update an immutable Fireflies identity.

```json
{"email":"janedoe2323@example.com","role":null,"metadata":{}}
```

#### `POST /commands/people/upsert-alias-email`

Create/update a manual alias email identity.

```json
{"email":"owner@example.com","role":"Owner","metadata":{}}
```

#### `POST /commands/people/upsert-anonymous`

Create an anonymous identity and optional name aliases.

```json
{"name":"Alex Lee","email":null,"aliases":["Liza"],"metadata":{}}
```

#### `POST /commands/people/map-name-alias`

Map a human name/speaker label to an email identity and optionally backfill tasks.

```json
{"alias":"jane doe","email":"owner@example.com","source":"manual","confidence":1.0,"backfill_tasks":true}
```

#### `POST /commands/people/add-email-alias`

Attach an alias email to an owner email.

```json
{"owner_email":"janedoe2323@example.com","alias_email":"owner@example.com","is_primary":true,"metadata":{}}
```

#### `POST /commands/people/set-primary-email-alias`

```json
{"owner_email":"janedoe2323@example.com","alias_email":"owner@example.com"}
```

#### `POST /commands/people/remove-email-alias`

```json
{"owner_email":"janedoe2323@example.com","alias_email":"owner@example.com"}
```

#### `POST /commands/people/resolve-or-create`

Command-side resolution for AI post-processing; may create anonymous.

```json
{"value":"Alex Lee","meeting_id":"01K...","allow_anonymous":true}
```

#### `POST /commands/people/merge-anonymous`

```json
{"anonymous_email":"alex-lee@anonymous.local","target_email":"liza@example.com","mode":"merge"}
```

Modes:

- `alias`: keep anonymous identity and attach it as an alias email.
- `merge`: rewrite references to target and deactivate anonymous.

#### `POST /commands/people/deactivate`

```json
{"email":"old@anonymous.local","reason":"merged"}
```

## Implementation phases

1. Schema:
   - Add `people.identity_type`.
   - Add `person_email_aliases`.
   - Add `meeting_people_candidates`.
   - Add owner fields to `task_origins` if not stored only in payload: `owner_ref`, `owner_email`, `owner_alias_id`, `unknown_owner_text`.
2. Repo:
   - Expand `PersonRepo` for identity type, anonymous generation, name alias mapping, email alias management, merge/deactivate.
   - Add candidate builder repo/service.
   - Update task sync to use resolved effective email.
3. HTTP:
   - Add query and command endpoints listed above.
4. Fact/AI pipeline:
   - Build and persist candidates before AI task owner assignment.
   - Prompt AI to choose `owner_ref` only.
   - Post-process `owner_ref` into `task_origins.owner_email` and `task_assignee_links.email`.
5. Backfill:
   - Map known aliases such as `jane doe`.
   - For unresolved aliases in existing task links, create anonymous identities or wait for manual mapping.
6. Verification:
   - `PYTHONPATH=src:. uv run python -m compileall app orchestration src utils`
   - `PYTHONPATH=src:. uv run python utils/ensure_schema.py`
   - `uv run pytest -q`
   - Real HTTP E2E on one unprocessed meeting.

## Non-goals

- Do not mutate Fireflies email identities.
- Do not let AI invent emails.
- Do not use names as task owner primary keys.
- Do not expose clear-all-databases over HTTP.
