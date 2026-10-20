<!-- Source: https://docs.fireflies.ai/schema/channel.md -->
<!-- Title: Channel -->
<!-- Description: Schema for Channel -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Channel

> Schema for Channel

<ResponseField name="id" type="ID">
  Unique identifier of the Channel.
</ResponseField>

<ResponseField name="title" type="String">
  Title of the Channel.
</ResponseField>

<ResponseField name="is_private" type="Boolean">
  Whether the channel is private. Private channels are only visible to their members.
</ResponseField>

<ResponseField name="created_by" type="String">
  Email of the user who created the channel.
</ResponseField>

<ResponseField name="created_at" type="String">
  Timestamp when the channel was created.
</ResponseField>

<ResponseField name="updated_at" type="String">
  Timestamp when the channel was last updated.
</ResponseField>

<ResponseField name="members" type="[ChannelMember]">
  List of members of this channel. See [ChannelMember](/schema/channel-member) for available fields.
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Channels Query" icon="link" href="/graphql-api/query/channels">
    Query list of channels
  </Card>

  <Card title="Channel Query" icon="link" href="/graphql-api/query/channel">
    Query a single channel by ID
  </Card>
</CardGroup>
