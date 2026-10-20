<!-- Source: https://docs.fireflies.ai/schema/input/create-live-action-item-input.md -->
<!-- Title: CreateLiveActionItemInput -->
<!-- Description: Schema for CreateLiveActionItemInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# CreateLiveActionItemInput

> Schema for CreateLiveActionItemInput

<ParamField path="meeting_id" type="ID!" required>
  The ID of the live meeting to create the action item for
</ParamField>

<ParamField path="prompt" type="String!" required>
  Natural language description of the action item to create. Fred will interpret this prompt and create the appropriate action item.

  Min / max of 5 / 255 characters.
</ParamField>
