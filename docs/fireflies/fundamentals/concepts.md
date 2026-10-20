<!-- Source: https://docs.fireflies.ai/fundamentals/concepts.md -->
<!-- Title: General concepts -->
<!-- Description: Foundational guide to the core aspects of the Fireflies API -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# General concepts

> Foundational guide to the core aspects of the Fireflies API

## Overview

This section serves as a primer on the essential features of the Fireflies API. It covers the requirements to make authenticated requests to the Fireflies API, key GraphQL concepts and a breakdown of core components like queries, mutations, schema and data types.

### Host

The Fireflies API is hosted at [https://api.fireflies.ai](https://api.fireflies.ai)

### Authorization

The Fireflies API requires a valid API key for all requests. Please see [Authorization](/fundamentals/authorization) for more information

## GraphQL API Concepts

Welcome to our GraphQL API! GraphQL is a powerful query language designed for APIs, offering clients the ability to request exactly what they need and nothing more.

### Queries

Queries are used to fetch data in GraphQL. They are akin to the `GET` request in REST.
A basic query might look like this:

<Info>Queries are read-only and won’t modify your data.</Info>

```graphql graphql theme={null}
query {
  user(id: "1") {
    name
    email
  }
}
```

### Mutations

Mutations allow you to modify data – create, update, or delete.

<Warning>Mutations should be used with caution as they change server-side data.</Warning>

```graphql graphql theme={null}
mutation {
  setUserRole(user_id: "1", role: "user") {
    id
    name
  }
}
```

## Schema and Types

### Schema Definition

The schema defines the API's capabilities, including types, queries, mutations, and more.

<Tip>
  <h3>Understanding GraphQL Schema</h3>
  <p>The schema is a contract between client and server, defining how clients can access data.</p>
</Tip>

#### Data Types

**Standard Types:** Int, Float, String, Boolean, ID.

**Custom Types:** Defining complex data structures. Custom types are user-defined and can include combinations of standard types.

#### Best Practices

1. Optimize query performance by requesting for only necessary data.
2. Use variables in queries to enhance readability and flexibility

## Additional Resources

For more in-depth information, visit [GraphQL Documentation](https://graphql.org/learn/).

<CardGroup cols={2}>
  <Card title="Quickstart" icon="link" href="/getting-started/quickstart">
    Make your first request in under 5 minutes
  </Card>

  <Card title="Introspection" icon="link" href="/fundamentals/introspection">
    Query generation and API exploration
  </Card>
</CardGroup>
