# Importing items in bulk

Learn how to create and update items in bulk via the platform API using ingest_items, backfill_items, and fetch_job_status

<Callout icon="🚧" theme="warn">
  **Only available in API versions [`2026-07`](https://developer.monday.com/api-reference/docs/release-notes#2026-07) and later**
</Callout>

Using the platform API, you can import large quantities of <Glossary>items</Glossary> into a monday.com board through an asynchronous, three-step workflow:

1. Start an import job ([`ingest_items`](https://developer.monday.com/api-reference/reference/ingest-items-api-reference) or [`backfill_items`](https://developer.monday.com/api-reference/reference/backfill-items-api-reference)) and receive a pre-signed `upload_url` and `job_id`
2. Upload the CSV file to the `upload_url`
3. Poll job status with [`fetch_job_status`](https://developer.monday.com/api-reference/reference/ingest-items-api-reference#fetch-job-status)

The API exposes two ways to start an import. **`ingest_items`** is the default for almost every use case. **`backfill_items`** is intended for a one-time, account-admin-only initial load — for example, seeding a board before it goes into day-to-day use.

***

# Choose how to import

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th />

      <th>`ingest_items` (recommended)</th>
      <th>`backfill_items`</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>**Use for**</td>
      <td>Integrations, recurring imports, creating or updating items as part of normal board activity</td>
      <td>A single large initial setup import before users or agents work in the board day-to-day</td>
    </tr>

    <tr>
      <td>**Maximum rows per job**</td>
      <td>10,000</td>
      <td>20,000</td>
    </tr>

    <tr>
      <td>**Who can call it**</td>
      <td>Any user with board edit access via API (`boards:write`)</td>
      <td>Account admin **and** `boards:write`</td>
    </tr>

    <tr>
      <td>**Update or skip existing items**</td>
      <td>Yes, using `on_match`</td>
      <td>Not supported; always creates new items</td>
    </tr>

    <tr>
      <td>**Hourly item create/update budget**</td>
      <td>Counts toward the 19,000 items per account per hour budget</td>
      <td>Does not consume this budget</td>
    </tr>

    <tr>
      <td>**Side effects on other monday features**</td>
      <td>None — automations and Activity Log behave normally</td>
      <td>Automations are not triggered. Item creation is not logged in the Activity Log.</td>
    </tr>
  </tbody>
</Table>

***

# Supported column types

Both endpoints support the following column types:

* Date
* Dropdown
* Email
* Link
* Long Text
* Number
* People
* Phone
* Status
* Text
* Timeline

Rows that include unsupported column types may fail validation. See [Column type validation](#column-type-validation) for the per-type CSV format.

***

# Limitations

| Category                            | `backfill_items`                 | `ingest_items`                     |
| :---------------------------------- | :------------------------------- | :--------------------------------- |
| Maximum rows per file               | 20,000                           | 10,000                             |
| Maximum file size                   | 150 MB                           | 150 MB                             |
| Upload URL expiration               | 10 minutes                       | 10 minutes                         |
| Report URL expiration               | 10 minutes                       | 10 minutes                         |
| Mutation calls per account per hour | 100 (shared with `ingest_items`) | 100 (shared with `backfill_items`) |
| Item create/update budget per hour  | Not consumed                     | 19,000 items per account           |

**Notes**

* File size is enforced after upload by the import service (not by the upload URL itself). Oversized files are rejected with `failure_reason: FILE_TOO_LARGE`.
* `backfill_items` and `ingest_items` share the same hourly limit on **starting jobs**.
* Cancellation of a running job is not supported.

***

# Getting started

## Pre-requisites

* [API authentication token](https://developer.monday.com/api-reference/docs/authentication)
* CSV file with valid headers and values (see [CSV format](#csv-format))
* Requests must include the `API-Version: 2026-07` [header](https://developer.monday.com/api-reference/docs/api-versioning#using-the-api-version-header-in-an-http-request)

## Step 1: Start the import job

1. Retrieve the `board_id` and `group_id` where you want to import items by querying [`boards`](https://developer.monday.com/api-reference/reference/boards) and [`groups`](https://developer.monday.com/api-reference/reference/groups).
2. Call [`ingest_items`](https://developer.monday.com/api-reference/reference/ingest-items-api-reference#ingest-items) unless you specifically need a one-time admin-only initial load via [`backfill_items`](https://developer.monday.com/api-reference/reference/backfill-items-api-reference#backfill-items).
3. Save the returned `job_id` and `upload_url`. The `upload_url` is only valid for 10 minutes.

**Ingest example (default path)**

```graphql GraphQL
mutation {
  ingest_items(
    board_id: "1234567890"
    group_id: "topics"
    on_match: { behaviour: UPSERT, match_column_id: "email" }
  ) {
    job_id
    upload_url
  }
}
```

**Backfill example (one-time initial load only)**

```graphql GraphQL
mutation {
  backfill_items(board_id: "1234567890", group_id: "topics") {
    job_id
    upload_url
  }
}
```

## Step 2: Upload the CSV file

Upload your CSV to the `upload_url` returned in Step 1.

```http
PUT <upload_url>
Content-Type: text/csv

<CSV file content>
```

A successful upload returns HTTP 200 with an `ETag` header.

```
HTTP/1.1 200 OK
ETag: "abc123def456"
```

## Step 3: Monitor the import status

Poll [`fetch_job_status`](https://developer.monday.com/api-reference/reference/ingest-items-api-reference#fetch-job-status) every \~10 seconds until the job reaches a terminal state (`COMPLETED`, `FAILED`, or `REJECTED`).

```graphql GraphQL
query {
  fetch_job_status(job_id: "7c9e6679-7425-40de-944b-e07fc1f90ae7") {
    ... on ItemsJobStatus {
      status
      counts {
        submitted
        invalid
        skipped
        created
        updated
        failed
      }
      progress_percentage
      failure_reason
      failure_message
      fully_imported
      report_created
      report_url
    }
  }
}
```

When `report_created` is `true`, download `report_url` promptly. The report URL expires after 10 minutes.

***

# Reference

## CSV format

* UTF-8 encoding is required.
* Use comma (`,`) as the column separator.
* Wrap values that contain commas, double quotes, or newlines in double quotes. Escape an embedded double quote by doubling it (`""`).

### Headers

* The first header value must be `name`.
* The remaining header values must be exact board `column_id` values (case-sensitive).
* Query [`columns`](https://developer.monday.com/api-reference/reference/columns) to retrieve the correct column IDs for the target board.

### Rows

* The first value in each row is the item name.
* The remaining values map to the column IDs in the header.
* Empty values are allowed. Whitespace-only values are treated as empty.
* In **UPSERT** mode (`ingest_items` only), an empty cell on a matched row is **ignored** — the existing column value is preserved.
* In **UPSERT** mode, a cell containing exactly the string `<NULL>` **clears** the column value on the matched item.

### Example

```csv
name,text,status,date,email,numeric,dropdown
Task 1,Description text,Working on it,2025-12-31,alice@monday.com,100,"Option A, Option B"
Task 2,Another task,Done,2026-01-15,bob@monday.com,200,Option C
Task 3,Third task,Stuck,2026-02-28,carol@monday.com,300,
Task 4,,,,,,
```

## Column type validation

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>Column type</th>
      <th>CSV value format</th>
      <th>Validation rules</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Date</td>
      <td>Valid date</td>
      <td>ISO format (`YYYY-MM-DD`). Other formats may be normalized.</td>
    </tr>

    <tr>
      <td>Dropdown</td>
      <td>Comma-separated labels</td>
      <td>Each label must already exist on the column and be active. All labels in a comma-separated list must be valid; otherwise the row fails.</td>
    </tr>

    <tr>
      <td>Email</td>
      <td>Valid email or `Name <email>`</td>
      <td>Must be a valid email format.</td>
    </tr>

    <tr>
      <td>Link</td>
      <td>Valid URL or `[Display Text](URL)`</td>
      <td>URL must start with `http://` or `https://`.</td>
    </tr>

    <tr>
      <td>Long Text</td>
      <td>Text string</td>
      <td>Empty values allowed.</td>
    </tr>

    <tr>
      <td>Number</td>
      <td>Numeric string</td>
      <td>Integer or decimal.</td>
    </tr>

    <tr>
      <td>People</td>
      <td>Comma-separated identifiers, each one of: email (`alice@example.com`), `user:<id>` or `user:<name>`, `team:<id>` or `team:<name>`, or a bare name (`Jeremy`) resolved as user or team.</td>
      <td>Each identifier must resolve to exactly one active user or team in the account. Fails on no match, multiple matches, or resolution errors. Duplicate identifiers are deduped. Respects the column's `max_people_allowed` setting.</td>
    </tr>

    <tr>
      <td>Phone</td>
      <td>Phone number string</td>
      <td>Various formats accepted; optional country hints.</td>
    </tr>

    <tr>
      <td>Status</td>
      <td>Label text (exact match)</td>
      <td>Label must already exist on the column and be active. Case-sensitive.</td>
    </tr>

    <tr>
      <td>Text</td>
      <td>Text string</td>
      <td>Empty values allowed.</td>
    </tr>

    <tr>
      <td>Timeline</td>
      <td>`YYYY-MM-DD/YYYY-MM-DD` for a range, or single `YYYY-MM-DD` (sets `from = to = date`)</td>
      <td>Both dates must be valid ISO dates. Other separators (dash with spaces, pipe, JSON) are not accepted.</td>
    </tr>
  </tbody>
</Table>

***

# Best practices

1. **Prefer `ingest_items`** for integrations and any import that should behave like normal board activity.
2. **Use `backfill_items` only** for a planned, one-time initial load.
3. Poll job status about every 10 seconds — not faster.
4. Validate the CSV header against the board schema **before** uploading.
5. Handle GraphQL errors from the API separately from HTTP errors from the file upload step.
6. Download the report as soon as `report_created` is `true`.
7. On `RATE_LIMIT_EXCEEDED`, wait using `extensions.retryAfterMs` instead of retrying immediately.
8. For ingest, spread large volumes across the hour where possible to reduce `ACCOUNT_CAPACITY_EXCEEDED` rejections.

***

# Troubleshooting

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>Issue</th>
      <th>Symptoms</th>
      <th>Resolution</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Upload URL expired</td>
      <td>HTTP 403 on the `PUT` upload (S3 returns "Request has expired")</td>
      <td>Start a new job and upload within 10 minutes.</td>
    </tr>

    <tr>
      <td>Invalid CSV format</td>
      <td>Status `REJECTED`, `failure_reason: INVALID_UPLOAD`</td>
      <td>Verify that the first header is `name`, all column IDs exist on the board, the file is UTF-8, the separator is comma, and embedded quotes are escaped (`""`).</td>
    </tr>

    <tr>
      <td>Items not created</td>
      <td>Status `COMPLETED` with high `counts.invalid` or `counts.failed` and low `counts.created`</td>
      <td>Download the report from `report_url` and inspect per-row errors. Check column ID typos, status/dropdown label spelling and case, date format, and that referenced users or teams exist.</td>
    </tr>

    <tr>
      <td>Status stuck at `UPLOAD_PENDING`</td>
      <td>No progress after uploading the CSV</td>
      <td>Confirm the upload returned HTTP 200 with an `ETag` header. If not, start a new job and re-upload.</td>
    </tr>

    <tr>
      <td>Backfill permission denied</td>
      <td>Status `REJECTED`, `failure_reason: PERMISSION_DENIED`, or a GraphQL error "Only admin users can perform this operation."</td>
      <td>`backfill_items` requires an account admin. Use `ingest_items` instead.</td>
    </tr>

    <tr>
      <td>File too large</td>
      <td>Status `REJECTED`, `failure_reason: FILE_TOO_LARGE`</td>
      <td>Split the file into chunks at or below 150 MB.</td>
    </tr>

    <tr>
      <td>Hourly capacity exceeded (ingest)</td>
      <td>Status `REJECTED`, `failure_reason: ACCOUNT_CAPACITY_EXCEEDED`</td>
      <td>The job's valid row count would exceed the remaining 19,000 items-per-hour budget. Spread the load across the hour or wait for the budget to reset.</td>
    </tr>

    <tr>
      <td>Rate limit on starting jobs</td>
      <td>GraphQL error `RATE_LIMIT_EXCEEDED` (HTTP 429) on `ingest_items` or `backfill_items`</td>
      <td>Honor `extensions.retryAfterMs` before retrying. The 100-call-per-hour limit is shared between `ingest_items` and `backfill_items`.</td>
    </tr>
  </tbody>
</Table>

***

# Related reference pages

* [Ingest items API reference](https://developer.monday.com/api-reference/reference/ingest-items-api-reference) (default)
* [Backfill items API reference](https://developer.monday.com/api-reference/reference/backfill-items-api-reference)
* [Bulk import other types](https://developer.monday.com/api-reference/reference/bulk-import-other-types)

<br />