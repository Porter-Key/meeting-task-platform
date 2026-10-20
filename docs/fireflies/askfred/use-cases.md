<!-- Source: https://docs.fireflies.ai/askfred/use-cases.md -->
<!-- Title: Use Cases -->
<!-- Description: Common use cases and example questions for AskFred - meeting summaries, action items, decisions, and more -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Cases

> Common use cases and example questions for AskFred - meeting summaries, action items, decisions, and more

## Overview

AskFred can help you extract insights from your meetings across a wide range of use cases. This page provides practical examples of questions you can ask for different scenarios.

## Common Use Cases

<AccordionGroup>
  <Accordion title="Meeting Summaries" icon="file-lines">
    Extract quick overviews and highlights from your meetings.

    **Example Questions:**

    * "Provide a brief summary of this meeting"
    * "What were the key takeaways?"
    * "Give me the highlights in 3 bullet points"
    * "Summarize the discussion about the product launch"
    * "What was the meeting about in one sentence?"

    **Best for:**

    * Daily standups
    * Client meetings
    * Team retrospectives
    * Board meetings
  </Accordion>

  <Accordion title="Action Item Tracking" icon="list-check">
    Identify tasks, responsibilities, and deliverables.

    **Example Questions:**

    * "What action items were assigned?"
    * "What are my action items from this week's meetings?"
    * "Who is responsible for the product roadmap?"
    * "List all open tasks and their owners"
    * "What are the deadlines mentioned in this meeting?"
    * "What tasks were assigned to the engineering team?"

    **Best for:**

    * Sprint planning
    * Project kickoffs
    * Weekly team syncs
    * Customer success calls
  </Accordion>

  <Accordion title="Decision Documentation" icon="gavel">
    Track important decisions and their rationale.

    **Example Questions:**

    * "What decisions were made about the budget?"
    * "What was decided regarding the new feature?"
    * "List all decisions with their rationales"
    * "What was the outcome of the pricing discussion?"
    * "Who made the final decision on the launch date?"
    * "What alternatives were considered before the decision?"

    **Best for:**

    * Strategy meetings
    * Leadership discussions
    * Product planning
    * Architecture reviews
  </Accordion>

  <Accordion title="Participant Insights" icon="users">
    Understand individual contributions and perspectives.

    **Example Questions:**

    * "What did John contribute to the discussion?"
    * "What concerns did the customer raise?"
    * "Summarize the CEO's main points"
    * "What feedback did the design team provide?"
    * "What questions did stakeholders ask?"
    * "Who disagreed with the proposal and why?"

    **Best for:**

    * Performance reviews
    * Client feedback analysis
    * Team collaboration assessment
    * Stakeholder management
  </Accordion>

  <Accordion title="Cross-Meeting Analysis" icon="chart-line">
    Identify patterns and trends across multiple meetings.

    **Example Questions:**

    * "How has customer sentiment changed over the last month?"
    * "What topics have been discussed most frequently?"
    * "Track the progress of Project X across all meetings"
    * "What are recurring issues in sprint retrospectives?"
    * "How has the team's velocity changed this quarter?"
    * "What concerns keep coming up in client calls?"

    **Best for:**

    * Quarterly reviews
    * Customer health monitoring
    * Team performance tracking
    * Product roadmap planning
  </Accordion>

  <Accordion title="Information Extraction" icon="filter">
    Pull specific data points and details from meetings.

    **Example Questions:**

    * "Extract all mentioned dates and deadlines"
    * "List all metrics and KPIs discussed"
    * "What tools or technologies were mentioned?"
    * "Find all budget figures discussed"
    * "What email addresses or contact information was shared?"
    * "What URLs or resources were mentioned?"

    **Best for:**

    * Meeting notes compilation
    * Documentation updates
    * Contact management
    * Resource tracking
  </Accordion>
</AccordionGroup>

## Industry-Specific Examples

<Accordion title="Sales Use Cases" icon="hand shake">
  **Discovery Calls:**

  * "What pain points did the prospect mention?"
  * "What is their current solution and why are they looking to change?"
  * "What is their timeline for making a decision?"

  **Deal Reviews:**

  * "What objections were raised during the demo?"
  * "Who are the decision-makers mentioned?"
  * "What competitive solutions are they considering?"

  **Pipeline Analysis:**

  * "What deals progressed this week?"
  * "What common objections are we seeing across calls?"
  * "Which prospects mentioned budget concerns?"
</Accordion>

<Accordion title="Product Use Cases" icon="box">
  **Feature Discussions:**

  * "What user problems are we trying to solve?"
  * "What alternatives did we consider?"
  * "What were the technical constraints mentioned?"

  **Roadmap Planning:**

  * "What features were prioritized for next quarter?"
  * "What customer feedback influenced our decisions?"
  * "What dependencies were identified?"

  **User Research:**

  * "What frustrations did users mention?"
  * "What features did users request most?"
  * "How do users currently solve this problem?"
</Accordion>

<Accordion title="Customer Success Use Cases" icon="headset">
  **Onboarding:**

  * "What questions did the customer ask during onboarding?"
  * "What features are they most interested in?"
  * "What integration requirements did they mention?"

  **Health Monitoring:**

  * "What concerns has the customer raised recently?"
  * "How has their sentiment changed over time?"
  * "What success metrics are they tracking?"

  **Escalations:**

  * "What issues were reported in the last month?"
  * "How quickly were problems resolved?"
  * "What patterns exist in customer complaints?"
</Accordion>

<Accordion title="Engineering Use Cases" icon="code">
  **Technical Planning:**

  * "What technical decisions were made?"
  * "What are the architectural concerns?"
  * "What dependencies block this feature?"

  **Sprint Retrospectives:**

  * "What went well this sprint?"
  * "What blockers did the team face?"
  * "What process improvements were suggested?"

  **Code Reviews:**

  * "What security concerns were raised?"
  * "What performance considerations were discussed?"
  * "What refactoring opportunities were identified?"
</Accordion>

## Advanced Query Patterns

### Time-Based Analysis

```graphql theme={null}
mutation TimeBasedQuery {
  createAskFredThread(input: {
    query: "How have customer satisfaction levels changed since last quarter?",
    filters: {
      start_time: "2024-01-01T00:00:00Z",
      end_time: "2024-03-31T23:59:59Z"
    }
  }) {
    message { answer }
  }
}
```

### Participant-Focused Queries

```graphql theme={null}
mutation ParticipantQuery {
  createAskFredThread(input: {
    query: "What feedback has the executive team provided on our product strategy?",
    filters: {
      participants: ["ceo@company.com", "cto@company.com"],
      start_time: "2024-03-01T00:00:00Z"
    }
  }) {
    message { answer }
  }
}
```

### Topic Tracking

```graphql theme={null}
mutation TopicTracking {
  createAskFredThread(input: {
    query: "Track all discussions about the new pricing model",
    filters: {
      start_time: "2024-01-01T00:00:00Z"
    }
  }) {
    message { answer suggested_queries }
  }
}
```

## Additional Resources

<CardGroup cols={2}>
  <Card title="AskFred Overview" icon="circle-info" href="/askfred/overview">
    Learn about AskFred's key capabilities
  </Card>

  <Card title="API Reference" icon="book" href="/graphql-api/mutation/create-askfred-thread">
    Explore all available parameters and options
  </Card>
</CardGroup>
