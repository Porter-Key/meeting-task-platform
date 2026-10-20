<!-- Source: https://docs.fireflies.ai/fundamentals/introspection.md -->
<!-- Title: Introspection -->
<!-- Description: Query generation and API exploration. -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Introspection

> Query generation and API exploration.

## Overview

Introspection is a feature that allows querying a GraphQL server to discover its schema. This capability is crucial for developers to understand available queries, mutations, and the structure of the data they can work with, facilitating seamless API interaction and exploration.

### Requirements

You will need a Fireflies.ai API key to use introspection. For more details, please visit [Authorization](/fundamentals/authorization#acquiring-a-token)

### Introspection using Apollo Sandbox

For introspection using our builtin Apollo Sandbox, visit [api.fireflies.ai/graphql](https://api.fireflies.ai/graphql) and enter your `api_key` in the Headers section as a Bearer token

### Introspection using Postman

Create a new Graphql Request in Postman with the url [api.fireflies.ai/graphql](https://api.fireflies.ai/graphql) and enter your `api_key` in the Headers section as a Bearer token

## Additional Resources

<CardGroup cols={2}>
  <Card title="Concepts" icon="link" href="/fundamentals/concepts">
    Foundational guide to the core aspects of the Fireflies API
  </Card>

  <Card title="Authorization" icon="link" href="/fundamentals/authorization">
    Authenticating your requests with the Fireflies API
  </Card>
</CardGroup>
