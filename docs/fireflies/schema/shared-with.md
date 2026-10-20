<!-- Source: https://docs.fireflies.ai/schema/shared-with.md -->
<!-- Title: SharedWith -->
<!-- Description: Schema for SharedWith -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# SharedWith

> Schema for SharedWith

<ResponseField name="email" type="String">
  Email address of the shared user.
</ResponseField>

<ResponseField name="name" type="String">
  Display name of the shared user.
</ResponseField>

<ResponseField name="photo_url" type="String">
  Profile photo URL of the shared user.
</ResponseField>

<ResponseField name="expires_at" type="String">
  ISO date string when the shared access expires. `null` if the share does not expire.
</ResponseField>
