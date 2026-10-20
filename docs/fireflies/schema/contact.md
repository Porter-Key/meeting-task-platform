<!-- Source: https://docs.fireflies.ai/schema/contact.md -->
<!-- Title: Contact -->
<!-- Description: Schema for Contact -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Contact

> Schema for Contact

<ResponseField name="email" type="String">
  Email address of the contact.
</ResponseField>

<ResponseField name="name" type="String">
  Full name of the contact.
</ResponseField>

<ResponseField name="picture" type="String" nullable>
  URL to the contact's profile picture. May be null if no picture is available.
</ResponseField>

<ResponseField name="last_meeting_date" type="String" nullable>
  The date of the last meeting with this contact in ISO 8601 format (YYYY-MM-DD). May be null if no meeting date is available.
</ResponseField>

## Additional Resources

<CardGroup cols={2}>
  <Card title="Contacts" icon="link" href="/graphql-api/query/contacts">
    Query contacts using the API
  </Card>

  <Card title="Users" icon="link" href="/graphql-api/query/users">
    Query users in your team
  </Card>
</CardGroup>
