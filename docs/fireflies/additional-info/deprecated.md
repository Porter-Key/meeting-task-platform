<!-- Source: https://docs.fireflies.ai/additional-info/deprecated.md -->
<!-- Title: Deprecated -->
<!-- Description: Fields marked for removal -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Deprecated

> Fields marked for removal

## Overview

This page lists all the fields that have been deprecated. Deprecated fields are fields that are no longer recommended for use and may be removed in future versions.

<Warning>
  Please note that using deprecated fields can lead to compatibility issues in future releases.
</Warning>

The following fields have been deprecated:

### [Transcript](/schema/transcript)

`host_email`: Use `organizer_email` instead.

### [Transcripts](/graphql-api/query/transcripts)

`date`: Use `fromDate` and `toDate` to query a time range.
`title`: Use `keyword` and `scope` instead of `title`
`organizer_email`: Use the `organizers` array field to filter by one or more organizer email addresses.
`participant_email`: Use the `participants` array field to filter by one or more participant email addresses.
