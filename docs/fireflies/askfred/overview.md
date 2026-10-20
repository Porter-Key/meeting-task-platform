<!-- Source: https://docs.fireflies.ai/askfred/overview.md -->
<!-- Title: Overview -->
<!-- Description: Use AI to intelligently query and analyze your meeting transcripts with natural language -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Overview

> Use AI to intelligently query and analyze your meeting transcripts with natural language

## What is AskFred?

AskFred is Fireflies' AI-powered meeting assistant that lets you ask natural language questions about your meeting transcripts. Query individual meetings or search across multiple meetings to get intelligent, context-aware answers.

<Note>
  **AI Credits Required** — Using AskFred through the API (including `createAskFredThread` and `continueAskFredThread`) requires AI credits. If your account does not have AI credits, you will receive a `require_ai_credits` error. Visit [Upgrade](https://app.fireflies.ai/upgrade) to add AI credits to your plan.
</Note>

### Key Capabilities

**Intelligent Q\&A** - Ask questions in natural language and receive comprehensive answers with smart follow-up suggestions

**Contextual Threads** - Maintain conversations where follow-up questions preserve context from previous exchanges

**Multi-Meeting Analysis** - Query across meetings using filters to identify patterns and aggregate insights

## API Operations

AskFred provides a comprehensive set of GraphQL operations:

### Queries

* [askfred\_threads](/graphql-api/query/askfred-threads) - List all conversation threads
* [askfred\_thread](/graphql-api/query/askfred-thread) - Get specific thread with full history

### Mutations

* [createAskFredThread](/graphql-api/mutation/create-askfred-thread) - Start a new conversation
* [continueAskFredThread](/graphql-api/mutation/continue-askfred-thread) - Add follow-up questions
* [deleteAskFredThread](/graphql-api/mutation/delete-askfred-thread) - Remove threads

## Next Steps

<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="/askfred/quickstart">
    Create your first thread and start querying meetings
  </Card>

  <Card title="Use Cases" icon="lightbulb" href="/askfred/use-cases">
    Example questions and industry-specific scenarios
  </Card>
</CardGroup>
