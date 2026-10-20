<!-- Source: https://docs.fireflies.ai/getting-started/docs-mcp-server.md -->
<!-- Title: Docs MCP Server -->
<!-- Description: Connect your AI tools to Fireflies documentation using MCP for instant access to API references, guides, and code examples. -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireflies.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Docs MCP Server

> Connect your AI tools to Fireflies documentation using MCP for instant access to API references, guides, and code examples.

### Overview

The Fireflies Documentation MCP Server enables AI tools to search and retrieve information directly from the Fireflies documentation. This allows you to ask questions about the Fireflies API, find code examples, understand features, and get implementation guidance without leaving your development environment.

### What is MCP?

Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect to external data sources and tools. With the Fireflies Documentation MCP Server, your AI tools can search across all Fireflies documentation including API references, guides, and code examples.

### Server Details

The Fireflies Documentation MCP Server is available at:

```
https://docs.fireflies.ai/mcp
```

This server provides a `SearchFireflies` tool that searches across the Fireflies knowledge base to find relevant information, code examples, API references, and guides.

### Configuration by Platform

<Tabs>
  <Tab title="Claude">
    Claude supports MCP servers through its Connectors feature. To connect Fireflies documentation:

    1. Open [Claude Settings](https://claude.ai/settings/connectors)
    2. Click **Add Connector**
    3. Enter the server URL: `https://docs.fireflies.ai/mcp`
    4. Save and start asking questions about Fireflies

    Once connected, Claude can search the Fireflies documentation to answer your questions about the API, implementation patterns, and best practices.
  </Tab>

  <Tab title="Claude Desktop">
    For Claude Desktop, add the following configuration to your `claude_desktop_config.json` file:

    **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

    **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

    **Linux:** `~/.config/Claude/claude_desktop_config.json`

    ```json theme={null}
    {
      "mcpServers": {
        "fireflies-docs": {
          "command": "npx",
          "args": [
            "mcp-remote",
            "https://docs.fireflies.ai/mcp"
          ]
        }
      }
    }
    ```

    After saving the configuration, restart Claude Desktop. You can then ask Claude questions about Fireflies documentation directly.
  </Tab>

  <Tab title="VS Code">
    VS Code supports MCP servers through GitHub Copilot. Create a `.vscode/mcp.json` file in your project:

    ```json theme={null}
    {
      "servers": {
        "fireflies-docs": {
          "type": "http",
          "url": "https://docs.fireflies.ai/mcp"
        }
      }
    }
    ```

    After configuration, use Copilot Chat in agent mode to query Fireflies documentation.
  </Tab>

  <Tab title="Cursor">
    Cursor supports MCP servers through its settings. To configure:

    1. Open Cursor Settings (Cmd/Ctrl + ,)
    2. Navigate to **Features > MCP Servers**
    3. Click **Add New MCP Server**
    4. Configure with the following details:
       * **Name:** `fireflies-docs`
       * **Type:** `url`
       * **Server URL:** `https://docs.fireflies.ai/mcp`

    Alternatively, add to your `~/.cursor/mcp.json` file:

    ```json theme={null}
    {
      "mcpServers": {
        "fireflies-docs": {
          "url": "https://docs.fireflies.ai/mcp"
        }
      }
    }
    ```

    After configuration, you can ask Cursor's AI assistant questions about Fireflies documentation.
  </Tab>

  <Tab title="Windsurf">
    Windsurf supports MCP servers through its configuration. Add the following to your `~/.codeium/windsurf/mcp_config.json` file:

    ```json theme={null}
    {
      "mcpServers": {
        "fireflies-docs": {
          "serverUrl": "https://docs.fireflies.ai/mcp"
        }
      }
    }
    ```

    After saving, restart Windsurf to enable the Fireflies documentation search.
  </Tab>
</Tabs>

### Available Tool

The server provides one tool for searching documentation:

<ParamField path="SearchFireflies" type="Tool">
  **Description:** Search across the Fireflies knowledge base to find relevant information, code examples, API references, and guides.

  **Parameters:**

  * `query` (string, required) - A query to search the content with

  **Example:**

  ```json theme={null}
  {
    "query": "how to upload audio files"
  }
  ```

  **Returns:** Contextual content with titles and direct links to the documentation pages.
</ParamField>

### Example Queries

Once configured, you can ask your AI tool questions like:

* "How do I authenticate with the Fireflies API?"
* "Show me an example of uploading audio for transcription"
* "What fields are available in the transcript query?"
* "How do I set up webhooks for Fireflies?"
* "What are the rate limits for the API?"
* "How do I search transcripts by date range?"

### Troubleshooting

**Server not connecting:**

* For Claude Desktop: Ensure you have Node.js installed (required for `npx mcp-remote`)
* Check that the URL is exactly `https://docs.fireflies.ai/mcp`
* Restart your AI application after configuration changes

**No results returned:**

* Try rephrasing your query with different keywords
* Be specific about what you're looking for (e.g., "GraphQL mutation for uploading audio" instead of just "upload")

### Additional Resources

<CardGroup cols={2}>
  <Card title="MCP Server Configuration" icon="plug" href="/getting-started/mcp-configuration">
    Connect AI tools to your meeting data with the Fireflies MCP Server
  </Card>

  <Card title="MCP Tools Reference" icon="tools" href="/mcp-tools/overview">
    Complete reference for all available MCP tools for meeting data
  </Card>
</CardGroup>
