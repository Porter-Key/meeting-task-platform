<!-- Source: https://docs.fireflies.ai/fundamentals/super-admin.md -->
<!-- Title: Super Admin -->
<!-- Description: Fireflies Super Admin with advanced capabilities for querying your data -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Super Admin

> Fireflies Super Admin with advanced capabilities for querying your data

## Overview

The Super Admin API offers advanced features such as team-wide webhooks and privacy setting bypass, providing enhanced control and flexibility for managing your data. This is only available on the enterprise tier for company admins - [learn more](https://guide.fireflies.ai/hc/en-us/articles/30453010621585-Learn-about-the-Super-Admin-role).

## Super Admin Webhooks

The Super Admin webhook notifies you of all team meetings owned by your team, allowing you to automate workflows, integrate with other tools, and maintain an overview of your team's meetings with a single webhook.

### Setting up Super Admin Webhooks

Follow the steps below to set up the Super Admin webhook:

<Steps>
  <Step>Visit the [Fireflies.ai dashboard settings](https://app.fireflies.ai/settings)</Step>
  <Step>Navigate to the Developer settings tab</Step>
  <Step>Enter a valid https URL in the webhooks field and save</Step>
</Steps>

<Warning>
  It is highly suggested to use [webhook auth](/graphql-api/webhooks) to secure your servers.
</Warning>

### Privacy Settings Bypass

The Super Admin functionality allows you to bypass your team's privacy settings, allowing you to query all data in your team's account.

### Requirements

Super Admin API is only available to teams on the Enterprise plan. [Learn more here](https://guide.fireflies.ai/hc/en-us/articles/30453010621585-Learn-about-the-Super-Admin-role) and reach out to us with questions

## Additional Resources

<CardGroup cols={2}>
  <Card title="Webhooks" icon="link" href="/graphql-api/webhooks">
    Create notifications using webhooks
  </Card>

  <Card title="Authorization" icon="link" href="/fundamentals/authorization">
    Authenticating your requests with the Fireflies API
  </Card>
</CardGroup>
