---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/agent-memory-mcp/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\agent-memory-mcp\SKILL.md
source_ext: .md
source_sha256: 01069cf8beb3984b27053322729d95c1be5d03b2136326d10a4c86c53f7eebda
text_sha256: 87f7692450db90f0ca101040873f431862dad1f8a71b41824a810eaa176c0897
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/agent-memory-mcp/SKILL.md`
- Extract: `text`
- SHA256: `01069cf8beb3984b27053322729d95c1be5d03b2136326d10a4c86c53f7eebda`

## Content

---
name: agent-memory-mcp
author: Amit Rathiesh
description: A hybrid memory system that provides persistent, searchable knowledge management for AI agents (Architecture, Patterns, Decisions).
---

# Agent Memory Skill

This skill provides a persistent, searchable memory bank that automatically syncs with project documentation. It runs as an MCP server to allow reading/writing/searching of long-term memories.

## Prerequisites

- Node.js (v18+)

## Setup

1. **Clone the Repository**:
   Clone the `agentMemory` project into your agent's workspace or a parallel directory:

   ```bash
   git clone https://github.com/webzler/agentMemory.git .agent/skills/agent-memory
   ```

2. **Install Dependencies**:

   ```bash
   cd .agent/skills/agent-memory
   npm install
   npm run compile
   ```

3. **Start the MCP Server**:
   Use the helper script to activate the memory bank for your current project:

   ```bash
   npm run start-server <project_id> <absolute_path_to_target_workspace>
   ```

   _Example for current directory:_

   ```bash
   npm run start-server my-project $(pwd)
   ```

## Capabilities (MCP Tools)

### `memory_search`

Search for memories by query, type, or tags.

- **Args**: `query` (string), `type?` (string), `tags?` (string[])
- **Usage**: "Find all authentication patterns" -> `memory_search({ query: "authentication", type: "pattern" })`

### `memory_write`

Record new knowledge or decisions.

- **Args**: `key` (string), `type` (string), `content` (string), `tags?` (string[])
- **Usage**: "Save this architecture decision" -> `memory_write({ key: "auth-v1", type: "decision", content: "..." })`

### `memory_read`

Retrieve specific memory content by key.

- **Args**: `key` (string)
- **Usage**: "Get the auth design" -> `memory_read({ key: "auth-v1" })`

### `memory_stats`

View analytics on memory usage.

- **Usage**: "Show memory statistics" -> `memory_stats({})`

## Dashboard

This skill includes a standalone dashboard to visualize memory usage.

```bash
npm run start-dashboard <absolute_path_to_target_workspace>
```

Access at: `http://localhost:3333`

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
