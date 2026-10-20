# Build on monday.com with AI

Connect AI agents and tools to monday.com through MCP servers, the GraphQL API, and typed SDKs

monday.com provides full headless access to its platform through MCP servers, a GraphQL API, and typed SDKs. Any MCP-compatible AI tool connects natively.

This page covers what the platform exposes, how the pieces connect, and what to know about authentication, rate limits, and agent account creation.

monday.com is a customizable AI work platform covering project management, CRM, dev, and service - used by over 250,000 organizations. The platform is built on a flexible data model of boards, items, and columns, exposes a full [GraphQL API](https://developer.monday.com/api-reference/reference), and includes a native AI layer for agents, workflows, and AI-assisted work.

# Architecture overview

monday.com provides two MCP servers covering different parts of the developer lifecycle, plus direct API access for advanced use cases.

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th />

      <th>Platform MCP</th>
      <th>Apps MCP</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>**Purpose**</td>
      <td>Read and write monday.com data</td>
      <td>Manage monday.com apps</td>
    </tr>

    <tr>
      <td>**Capabilities**</td>
      <td>Query boards, create items, update columns, manage users, execute GraphQL</td>
      <td>Scaffold apps, create features, deploy, promote versions, search developer docs</td>
    </tr>

    <tr>
      <td>**Transport**</td>
      <td>Hosted remote (Streamable HTTP)</td>
      <td>Local via npx</td>
    </tr>

    <tr>
      <td>**Auth**</td>
      <td>OAuth 2.1</td>
      <td>Personal API token</td>
    </tr>

    <tr>
      <td>**Config**</td>
      <td>`"url": "https://mcp.monday.com/mcp"`</td>
      <td>`npx @mondaydotcomorg/monday-api-mcp -t <token> --mode apps`</td>
    </tr>
  </tbody>
</Table>

The **Platform MCP** is the primary integration surface. It wraps the [monday.com GraphQL API](https://developer.monday.com/api-reference/reference) and provides structured tools for common operations. The **Apps MCP** is purpose-built for app development - it manages the app lifecycle and includes semantic search over all [monday.com developer documentation](https://developer.monday.com/apps/docs/intro).

Both can run simultaneously in the same IDE session. Platform MCP handles data; Apps MCP handles code.

## Direct API access

For use cases that need the full API surface - batch operations, complex nested queries, or direct schema introspection - the monday.com [GraphQL API](https://developer.monday.com/api-reference/reference) is available directly:

```shell Terminal
curl -X POST https://api.monday.com/v2 \
  -H "Authorization: <your_token>" \
  -H "Content-Type: application/json" \
  -H "API-Version: 2026-07" \
  -d '{"query": "{ boards (limit: 5) { id name } }"}'
```

The Platform MCP also supports raw GraphQL execution through its `all_monday_api` tool, with API version control via MCP config headers.

***

# Connect to monday.com

## Connect external agents

You can bring your own agent into monday.com as a first-class participant. Connected agents authenticate with their own API token and operate within the permission scope granted by the account admin.

Supported connection modes:

**Managed provider (e.g. Claude Managed Agent)** - Provide your API key and agent ID. monday.com orchestrates calls to the provider and gives the agent access to platform tools (boards, items, updates, etc.) - the same capabilities available to built-in agents.

**Custom agent (webhook)** - Provide a callback URL. monday.com posts event payloads to your endpoint to trigger the agent (via automation or assignment). Your agent processes the payload and responds with actions.

Connected agents:

* Can be assigned to items and mentioned in updates
* Have admin-configurable access to workspaces and boards
* Consume AI credits tracked under the account's usage dashboard
* Are governed by account-level permissions that admins control

## Platform MCP

The hosted Platform MCP requires no local setup. Add the server URL and authenticate via OAuth when prompted.

* **Server URL:** `https://mcp.monday.com/mcp`
* **Transport:** Streamable HTTP
* **Auth:** OAuth 2.1 (or Bearer token with a [personal API token](https://developer.monday.com/api-reference/docs/authentication))

For per-client setup instructions, see the [MCP overview](https://developer.monday.com/api-reference/docs/mondaycom-mcp) which includes configuration for Cursor, Claude, VS Code, ChatGPT, Copilot Studio, Mistral, Gemini CLI, Perplexity, and Figma Make.

## Apps MCP (local)

To add app development capabilities, run the Apps MCP alongside the Platform MCP:

```json
{
  "mcpServers": {
    "monday-apps-mcp": {
      "command": "npx",
      "args": ["@mondaydotcomorg/monday-api-mcp", "-t", "<your_token>", "--mode", "apps"]
    }
  }
}
```

See the [Apps MCP documentation](https://developer.monday.com/apps/docs/monday-apps-mcp) for the full tool reference.

***

# Platform capabilities

## Data model

monday.com organizes work as: **Workspaces > Boards > Groups > Items > Subitems**, with typed **Column Values** on each item. The API and MCP tools operate across this hierarchy.

## Platform MCP tools

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>Domain</th>
      <th>Operations</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>**Boards**</td>
      <td>Create, query, duplicate, get schema (columns, groups, settings)</td>
    </tr>

    <tr>
      <td>**Items**</td>
      <td>Create, update column values, move between groups, query with filters</td>
    </tr>

    <tr>
      <td>**Columns**</td>
      <td>Create, get type info (JSON schema and validation rules)</td>
    </tr>

    <tr>
      <td>**Users and teams**</td>
      <td>List, query permissions</td>
    </tr>

    <tr>
      <td>**Documents**</td>
      <td>Create, read, update workdocs</td>
    </tr>

    <tr>
      <td>**Search**</td>
      <td>Find boards, documents, folders across the account</td>
    </tr>

    <tr>
      <td>**Notifications**</td>
      <td>Create notifications for users</td>
    </tr>

    <tr>
      <td>**Updates**</td>
      <td>Post and read item updates (comments)</td>
    </tr>

    <tr>
      <td>**Workspaces**</td>
      <td>Create, list, manage</td>
    </tr>

    <tr>
      <td>**GraphQL**</td>
      <td>Execute arbitrary queries/mutations via `all_monday_api` tool</td>
    </tr>
  </tbody>
</Table>

Column values use typed JSON. For unfamiliar types, the `get_column_type_info` tool returns the expected schema and validation rules. See the [column types reference](https://developer.monday.com/api-reference/docs/supported-column-types) for full documentation.

For the full tool catalog, see <a href="https://support.monday.com/hc/en-us/articles/32364501317906" target="_blank">monday MCP available tools</a>.

## Apps MCP tools

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>Domain</th>
      <th>Operations</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>**App management**</td>
      <td>Create apps, list apps, get versions</td>
    </tr>

    <tr>
      <td>**Features**</td>
      <td>Create features ([board views, widgets, integrations, custom columns, workflow blocks](https://developer.monday.com/apps/docs/app-features))</td>
    </tr>

    <tr>
      <td>**Deployment**</td>
      <td>Check deployment status, promote versions</td>
    </tr>

    <tr>
      <td>**Environment**</td>
      <td>Set and list environment variables</td>
    </tr>

    <tr>
      <td>**Storage**</td>
      <td>Search and export app storage data</td>
    </tr>

    <tr>
      <td>**Documentation**</td>
      <td>Semantic search across all developer docs - app features, OAuth, SDK, [Vibe Design System](https://developer.monday.com/apps/docs/vibe-design-system), monday-code, workflow blocks</td>
    </tr>
  </tbody>
</Table>

***

# Agent account creation

External agents can create monday.com accounts programmatically via a dedicated signup API - no browser required.

The full specification is published as an agent skill: <a href="https://monday.com/.well-known/agent-skills/signup-for-agents/SKILL.md" target="_blank">monday.com agent signup skill</a>

## Flow overview

```
Step 1: POST /signup-logic/agent-captcha/challenge/v1  -> get challengeToken
Step 2: POST /signup-logic/agent-captcha/verify/v1     -> solve challenge, get verificationToken
Step 3: POST /signup-logic/agent-signup/account/v1     -> create account, receive api_token
Step 4: Use api_token with monday.com API              -> create boards, items, invite members
```

**Base URL:** `https://signup-logic.monday.com`

## Key mechanics

* **HATCHA captcha** - Agent-friendly challenges (binary-to-ASCII, string reversal, counting, sorting, math). Solvable programmatically in under 30 seconds.
* **Terms acceptance** - `agreed_to_terms: true` is required. Returns error with TC link if omitted.
* **Email handling** - Omit email to get an auto-generated `@monday-agent.com` address (account immediately active). Provide a real email to trigger confirmation flow.
* **Response** includes `api_token` (JWT, `me:write` scope), `account_url`, `board_id` for the auto-created board, and a `skill_url` pointing to API usage instructions.
* **User kind** - Accounts are tagged `agent_signup_user`, enabling differentiated policies and analytics.

## Rate limits (signup)

15 requests per 60 seconds per IP address on the account creation endpoint.

## After account creation

The agent receives an API token and can immediately:

* Create boards and items via the [GraphQL API](https://developer.monday.com/api-reference/reference)
* Invite human collaborators via `invite_users` / `add_subscribers_to_board` mutations
* Connect to the [Platform MCP](https://developer.monday.com/api-reference/docs/mondaycom-mcp) for structured tool access

***

# Machine-readable documentation

## /llms.txt

A structured index of all developer documentation: <a href="https://developer.monday.com/llms.txt" target="_blank">developer.monday.com/llms.txt</a>. AI tools use this to discover API pages, guides, and references without crawling.

## Plain-text markdown

Append `.md` to any documentation URL to get clean markdown output:

```
https://developer.monday.com/api-reference/docs/build-on-monday-with-ai.md
```

## Semantic search via Apps MCP

The `get_development_context` tool provides AI-powered search across all monday.com developer documentation. Covers [app features](https://developer.monday.com/apps/docs/app-features), [OAuth scopes](https://developer.monday.com/apps/docs/oauth), SDK reference, [monday-code](https://developer.monday.com/apps/docs/monday-code-intro), Vibe Design System, [workflow blocks](https://developer.monday.com/apps/docs/workflows-triggers), and troubleshooting patterns.

***

# Authentication and security

## OAuth 2.1

The Platform MCP uses OAuth 2.0 Authorization Code Grant. monday.com is the identity provider.

1. MCP client redirects to `https://auth.monday.com/oauth2/authorize`
2. User approves requested [permission scopes](https://developer.monday.com/apps/docs/oauth#set-up-permission-scopes)
3. Client exchanges the authorization code for an access token

All MCP tool calls execute in the context of the authenticated user - scoped to that user's platform permissions. No privilege elevation is possible.

## Token strategy

* **Personal tokens** mirror your UI permissions. Use for individual development.
* **App tokens** have explicit permission scopes (e.g., `boards:read`, `boards:write`). Use for production apps and agents that should have minimum required access.
* Token lifecycle management (storage, rotation, revocation) is the developer's responsibility.

## Security model

All communication over TLS. Per-user session isolation prevents cross-tenant context leakage. MCP tools are defined and controlled by monday.com - not modifiable by clients. The MCP server does not store or log OAuth tokens. See the [MCP security overview](https://developer.monday.com/api-reference/docs/monday-mcp-security-overview) for full details.

***

# Rate limits

The monday.com platform enforces the following [rate limits](https://developer.monday.com/api-reference/docs/rate-limits).

## Limits by plan

<Table align={["left","left","left","left"]}>
  <thead>
    <tr>
      <th>Limit</th>
      <th>Free</th>
      <th>Pro</th>
      <th>Enterprise</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Complexity</td>
      <td>5M points/min</td>
      <td>5M points/min</td>
      <td>5M points/min</td>
    </tr>

    <tr>
      <td>Complexity for agents</td>
      <td>20M points/min</td>
      <td>20M points/min</td>
      <td>20M points/min</td>
    </tr>

    <tr>
      <td>Daily calls</td>
      <td>1,000</td>
      <td>10,000</td>
      <td>25,000\*</td>
    </tr>

    <tr>
      <td>Queries/minute</td>
      <td>1,000</td>
      <td>2,500</td>
      <td>5,000</td>
    </tr>

    <tr>
      <td>Concurrency</td>
      <td>40</td>
      <td>100</td>
      <td>250</td>
    </tr>

    <tr>
      <td>IP rate</td>
      <td>5,000 req/10s</td>
      <td>5,000 req/10s</td>
      <td>5,000 req/10s</td>
    </tr>
  </tbody>
</Table>

\* Daily call limits are soft - agents exceeding them are not blocked on Enterprise plans.

Reads and writes have separate complexity budgets. Complexity resets on a sliding 60-second window.

Agents may benefit from higher thresholds than standard API access - contact support if your use case requires it.

## Complexity in practice

A typical `items` query with 10 columns across 50 items costs a few thousand complexity points - well under the 5M/minute ceiling. Add the `complexity` field to any query to see exact costs:

```graphql GraphQL
mutation {
  complexity {
    query
    before
    after
  }
  create_item(board_id: 1234567890, item_name: "test item") {
    id
  }
}
```

## SDK auto-retry

Both the [JavaScript SDK](https://developer.monday.com/api-reference/docs/javascript-sdk) (`@mondaydotcomorg/api`) and [Python SDK](https://developer.monday.com/api-reference/docs/python-sdk) (`monday-api-python-sdk`) handle rate limits automatically:

* HTTP 429: backs off and retries
* Complexity exceptions: waits and retries
* Configurable max retries (Python default: 4)
* Respects `Retry-After` headers