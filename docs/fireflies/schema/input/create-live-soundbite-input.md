<!-- Source: https://docs.fireflies.ai/schema/input/create-live-soundbite-input.md -->
<!-- Title: CreateLiveSoundbiteInput -->
<!-- Description: Schema for CreateLiveSoundbiteInput -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# CreateLiveSoundbiteInput

> Schema for CreateLiveSoundbiteInput

<ParamField path="meeting_id" type="ID!" required>
  The ID of the live meeting to create the soundbite for
</ParamField>

<ParamField path="prompt" type="String!" required>
  Natural language description of the soundbite to create. Fred will interpret this prompt and create the appropriate soundbite.

  Min / max of 5 / 255 characters.
</ParamField>
