<!-- Source: https://docs.fireflies.ai/getting-started/mcp-configuration.md -->
<!-- Title: MCP Server Configuration -->
<!-- Description: Connect your AI tools directly to your meeting data with Fireflies MCP Server. -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# MCP Server Configuration

> Connect your AI tools directly to your meeting data with Fireflies MCP Server.

### Overview

The Fireflies MCP Server enables AI tools to connect directly to your meeting data without switching platforms or copying transcript excerpts. This integration allows you to ask questions like "What were the main objections in this week's sales calls?" or "Create a summary of all product feedback from user interviews this month" directly from your AI coding tools.

### What is MCP?

Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect to external data sources and tools. With Fireflies MCP Server, your AI tools can access meeting transcripts, summaries, action items, and insights directly from your Fireflies account.

### Getting Started

#### Prerequisites

* Active Fireflies.ai account
* AI tool that supports MCP (such as Claude, OpenAI Connector, Cursor, Devin, or other MCP-compatible applications)

#### Installation

1. **Configure your AI tool**
   Add the Fireflies MCP server to your AI tool's configuration. The remote server URL is [https://api.fireflies.ai/mcp](https://api.fireflies.ai/mcp) which uses OAuth with your Fireflies account. The exact steps depend on your specific AI application.

   For specific AI tools, you can also configure directly through:

   * [Claude Settings](https://claude.ai/settings/connectors)
   * [Devin MCP Marketplace](https://app.devin.ai/settings/mcp-marketplace/setup/fireflies)

2. **Use your Fireflies API key on Claude Desktop** (Optional):
   1. Add this config to your `claude_desktop_config.json` file:
      ```json theme={null}
      {
        "mcpServers": {
          "fireflies": {
            "command": "npx",
            "args": [
              "mcp-remote",
              "https://api.fireflies.ai/mcp",
              "--header",
              "Authorization: Bearer YOUR_API_KEY_HERE"
            ]
          }
        }
      }
      ```
   2. Get your API Key from Fireflies
      * Go to **Settings > Developer Settings** and **Copy your API key**
      * [See how to get your API key →](https://guide.fireflies.ai/hc/en-us/articles/360020249198-How-to-access-the-Fireflies-API-key)
      * Once you have the API key, paste it in your claude\_desktop\_config.json
      * Replace `YOUR_API_KEY_HERE` with your actual API key
   3. Restart Claude Desktop

3. **Start querying your data**
   Once configured, you can ask your AI tool questions about your meeting data directly.

### Use Cases

* **Sales Analysis**: "What were the common objections in this week's sales calls?"
* **Product Feedback**: "Summarize all product feedback from user interviews this month"
* **Meeting Insights**: "What action items were assigned to John across all meetings?"
* **Trend Analysis**: "How has customer sentiment changed over the past quarter?"

### Additional Resources

<CardGroup cols={2}>
  <Card title="MCP Tools" icon="tools" href="/mcp-tools/overview">
    Complete reference for all available MCP tools and their parameters
  </Card>

  <Card title="LLM-based Development" icon="link" href="/getting-started/llm-development">
    Enhance your AI coding experience with LLM readable documentation
  </Card>

  <Card title="Authorization" icon="lock" href="/fundamentals/authorization">
    Authenticating your requests with the Fireflies API
  </Card>
</CardGroup>
