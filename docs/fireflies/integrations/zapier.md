<!-- Source: https://docs.fireflies.ai/integrations/zapier.md -->
<!-- Title: Zapier -->
<!-- Description: Set up webhooks with Zapier to automatically fetch transcripts -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Zapier

> Set up webhooks with Zapier to automatically fetch transcripts

## Overview

Connect Fireflies [webhooks](/graphql-api/webhooks) to Zapier to automatically fetch transcripts when meetings are processed. This guide creates a two-step Zap:

1. **Trigger** — receive a webhook notification when a meeting is transcribed
2. **Action** — use the `meetingId` from the webhook to fetch the transcript via the [GraphQL API](/graphql-api/query/transcript)

## Prerequisites

* A Fireflies.ai account with [webhook access](/graphql-api/webhooks)
* A [Zapier](https://zapier.com) **paid plan** (Professional or above — Webhooks by Zapier is not available on the free tier)
* Your Fireflies [API key](https://app.fireflies.ai/settings)

## Step 1: Create the Zapier webhook trigger

<Steps>
  <Step title="Create a new Zap">
    Log in to [Zapier](https://zapier.com) and click **Create**.
  </Step>

  <Step title="Select trigger">
    Search for **Webhooks by Zapier** → choose **Catch Hook**.
  </Step>

  <Step title="Skip Configure">
    Leave the **Pick off a Child Key** field blank and click **Continue**.
  </Step>

  <Step title="Copy the webhook URL">
    On the **Test** tab, copy the generated URL (e.g. `https://hooks.zapier.com/hooks/catch/123456/abcdef/`). You'll paste this into Fireflies next.
  </Step>
</Steps>

## Step 2: Add the webhook URL in Fireflies

<Steps>
  <Step title="Open Developer settings">
    Go to [Fireflies settings](https://app.fireflies.ai/settings) → **Developer settings** in the left sidebar.
  </Step>

  <Step title="Configure the webhook">
    Under **Webhook**, click **Configure** and fill in:

    * **Webhook URL** — paste the Zapier URL from Step 1
    * **Trigger when transcription is completed** — check this box
  </Step>

  <Step title="Save">
    Click **Save**.
  </Step>
</Steps>

## Step 3: Test the connection

<Steps>
  <Step title="Listen for a test event">
    In Zapier, click **Test trigger**. Then [upload a short audio file](https://app.fireflies.ai/upload) in Fireflies to generate a webhook event.
  </Step>

  <Step title="Verify the payload">
    Zapier should receive a payload like:

    ```json theme={null}
    {
      "meetingId": "ASxwZxCstx",
      "eventType": "Transcription completed"
    }
    ```

    The `meetingId` is the transcript ID you'll use next.
  </Step>
</Steps>

## Step 4: Fetch the transcript

Add a second step to your Zap that calls the Fireflies GraphQL API with the `meetingId`.

<Steps>
  <Step title="Add action">
    Click **+** → search **Webhooks by Zapier** → select **Custom Request**.
  </Step>

  <Step title="Configure the request">
    * **Method**: `POST`
    * **URL**: `https://api.fireflies.ai/graphql`
    * **Headers**:

    | Key           | Value                 |
    | ------------- | --------------------- |
    | Content-Type  | application/json      |
    | Authorization | Bearer YOUR\_API\_KEY |
  </Step>

  <Step title="Set the request body">
    In the **Data** field, enter:

    ```json theme={null}
    {
      "query": "query Transcript($transcriptId: String!) { transcript(id: $transcriptId) { id title date organizer_email participants transcript_url duration summary { overview action_items shorthand_bullet short_summary } sentences { speaker_name text start_time end_time } } }",
      "variables": {
        "transcriptId": "{{meetingId}}"
      }
    }
    ```

    <Note>
      Do **not** type `{{meetingId}}` literally. Use Zapier's **Insert Data** picker to select **Meeting Id** from the trigger step — the field should show a data pill, not raw text.
    </Note>
  </Step>

  <Step title="Test">
    Click **Test step**. You should see the transcript data in the response.
  </Step>
</Steps>

## Step 5: Extend your Zap

With transcript data flowing into Zapier, add more steps to automate your workflow:

* **Slack** — post meeting summaries to a channel
* **Google Sheets** — log meeting details in a spreadsheet
* **Asana / Jira / Trello** — create tasks from action items
* **Email** — send recaps to attendees
* **Salesforce / HubSpot** — push notes to your CRM

## Customizing the query

Modify the GraphQL query in Step 4 to fetch only the fields you need. See the [Transcript schema](/schema/transcript) for all available fields.

Example with speaker analytics and AI filters:

```graphql theme={null}
query Transcript($transcriptId: String!) {
  transcript(id: $transcriptId) {
    id
    title
    summary {
      overview
      action_items
    }
    analytics {
      speakers {
        name
        duration
        words_per_minute
      }
    }
    sentences {
      speaker_name
      text
      ai_filters {
        task
        question
        sentiment
      }
    }
  }
}
```

## Troubleshooting

<AccordionGroup>
  <Accordion title="Zapier is not receiving events">
    * Check the webhook URL is saved in [Developer settings](https://app.fireflies.ai/settings)
    * Ensure **Trigger when transcription is completed** is checked
    * The URL must start with `https://`
    * Try uploading a test file at [app.fireflies.ai/upload](https://app.fireflies.ai/upload)
  </Accordion>

  <Accordion title="Transcript query returns null">
    * Verify you're using the correct `meetingId` from the webhook
    * Check your API key hasn't expired
  </Accordion>

  <Accordion title="Authorization error">
    * Ensure the header is `Bearer YOUR_API_KEY` (with a space after `Bearer`)
    * The API key must belong to the account that owns the webhook
  </Accordion>
</AccordionGroup>

## Resources

<CardGroup cols={2}>
  <Card title="Webhooks" icon="bell" href="/graphql-api/webhooks">
    Webhook events and authentication
  </Card>

  <Card title="Transcript query" icon="file-lines" href="/graphql-api/query/transcript">
    Full query reference
  </Card>

  <Card title="Transcript schema" icon="database" href="/schema/transcript">
    All available fields
  </Card>
</CardGroup>
