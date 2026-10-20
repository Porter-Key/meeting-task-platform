<!-- Source: https://docs.fireflies.ai/schema/user-groups.md -->
<!-- Title: UserGroups -->
<!-- Description: Schema for UserGroups -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# UserGroups

> Schema for UserGroups

<ResponseField name="id" type="String">
  Unique ID for the user group
</ResponseField>

<ResponseField name="name" type="String">
  Name of the user group.
</ResponseField>

<ResponseField name="handle" type="String">
  Unique identifier or handle for the user group.
</ResponseField>

<ResponseField name="members" type="[UserGroupMember]" nullable="true">
  List of members in the user group. See [UserGroupMember](/schema/user-group-member)
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="User" icon="link" href="/schema/user">
    Schema for User
  </Card>

  <Card title="UserGroupMember" icon="link" href="/schema/user-group-member">
    Schema for UserGroupMember
  </Card>
</CardGroup>
