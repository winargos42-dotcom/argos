---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/using-neon/references/devtools.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\using-neon\references\devtools.md
source_ext: .md
source_sha256: 58ba2c57bc1ce11e2d221ddb910b36773933343d1b5304d057d6194f5cdc1583
text_sha256: a4d4121fe2b65a6b9f171ffb9b603ed75b8640968eb6a904ad2e0ea237f768e0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# devtools.md

- Source: `claude-code-templates/cli-tool/components/skills/database/using-neon/references/devtools.md`
- Extract: `text`
- SHA256: `58ba2c57bc1ce11e2d221ddb910b36773933343d1b5304d057d6194f5cdc1583`

## Content

# Neon Developer Tools

Neon provides developer tools to enhance your local development workflow, including a VSCode extension and MCP server for AI-assisted development.

## Quick Setup with neon init

The fastest way to set up all Neon developer tools:

```bash
npx neon init
```

This command:

- Installs the Neon VSCode extension
- Configures the Neon MCP server for AI assistants
- Sets up your local environment for Neon development

For full CLI reference:

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/reference/cli-init
```

## VSCode Extension

The Neon VSCode extension provides:

- **Database Explorer**: Browse projects, branches, tables, and data
- **SQL Editor**: Write and execute queries with IntelliSense
- **Branch Management**: Create, switch, and manage database branches
- **Connection String Access**: Quick copy of connection strings

**Install from VSCode:**

1. Open Extensions (Cmd/Ctrl+Shift+X)
2. Search "Neon"
3. Install "Neon" by Neon

**Or via command line:**

```bash
code --install-extension neon.neon-vscode
```

For detailed documentation:

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/local/vscode-extension
```

## Neon MCP Server

The Neon MCP (Model Context Protocol) server enables AI assistants like Claude, Cursor, and GitHub Copilot to interact with your Neon databases directly.

### Capabilities

The MCP server provides AI assistants with:

- **Project Management**: List, create, describe, and delete projects
- **Branch Operations**: Create branches, compare schemas, reset from parent
- **SQL Execution**: Run queries and transactions
- **Schema Operations**: Describe tables, get database structure
- **Migrations**: Prepare and complete database migrations with safety checks
- **Query Tuning**: Analyze and optimize slow queries
- **Neon Auth**: Provision authentication for your branches

### Setup

**Option 1: Via neon init (Recommended)**

```bash
npx neon init
```

**Option 2: Manual Configuration**

Add to your AI assistant's MCP configuration:

```json
{
  "mcpServers": {
    "neon": {
      "command": "npx",
      "args": ["-y", "@neondatabase/mcp-server-neon"],
      "env": {
        "NEON_API_KEY": "your-api-key"
      }
    }
  }
}
```

Get your API key from: https://console.neon.tech/app/settings/api-keys

### Common MCP Operations

| Operation                    | What It Does                  |
| ---------------------------- | ----------------------------- |
| `list_projects`              | Show all Neon projects        |
| `create_project`             | Create a new project          |
| `run_sql`                    | Execute SQL queries           |
| `get_connection_string`      | Get database connection URL   |
| `create_branch`              | Create a database branch      |
| `prepare_database_migration` | Safely prepare schema changes |
| `provision_neon_auth`        | Set up Neon Auth              |

For full MCP server documentation:

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/ai/neon-mcp-server
```

## Documentation Resources

| Topic              | URL                                           |
| ------------------ | --------------------------------------------- |
| CLI Init Command   | https://neon.tech/docs/reference/cli-init     |
| VSCode Extension   | https://neon.tech/docs/local/vscode-extension |
| MCP Server         | https://neon.tech/docs/ai/neon-mcp-server     |
| Neon CLI Reference | https://neon.tech/docs/reference/neon-cli     |

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
