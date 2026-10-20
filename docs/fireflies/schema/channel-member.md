<!-- Source: https://docs.fireflies.ai/schema/channel-member.md -->
<!-- Title: ChannelMember -->
<!-- Description: Schema for ChannelMember -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# ChannelMember

> Schema for ChannelMember

<ResponseField name="user_id" type="String">
  Unique identifier for the channel member.
</ResponseField>

<ResponseField name="email" type="String">
  Email address of the channel member.
</ResponseField>

<ResponseField name="name" type="String">
  Display name of the channel member.
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Channel" icon="link" href="/schema/channel">
    Schema for Channel
  </Card>

  <Card title="Channels Query" icon="link" href="/graphql-api/query/channels">
    Query list of channels
  </Card>
</CardGroup>
