---
argos_import: project_file
source_path: mempalace-develop/.claude-plugin/README.md
source_abs: F:\debug\argoss\mempalace-develop\.claude-plugin\README.md
source_ext: .md
source_sha256: 2aba52269f97160e89a8ac4d5bd413a6e0afee71049328a441b4633508e89157
text_sha256: 2aba52269f97160e89a8ac4d5bd413a6e0afee71049328a441b4633508e89157
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# README.md

- Source: `mempalace-develop/.claude-plugin/README.md`
- Extract: `text`
- SHA256: `2aba52269f97160e89a8ac4d5bd413a6e0afee71049328a441b4633508e89157`

## Content

# MemPalace Claude Code Plugin

A Claude Code plugin that gives your AI a persistent memory system. Mine projects and conversations into a searchable palace backed by ChromaDB, with 19 MCP tools, auto-save hooks, and 5 guided skills.

## Prerequisites

- Python 3.9+

## Installation

### Claude Code Marketplace

```bash
claude plugin marketplace add milla-jovovich/mempalace
claude plugin install --scope user mempalace
```

### Local Clone

```bash
claude plugin add /path/to/mempalace
```

## Post-Install Setup

After installing the plugin, run the init command to complete setup (pip install, MCP configuration, etc.):

```
/mempalace:init
```

## Available Slash Commands

| Command | Description |
|---------|-------------|
| `/mempalace:help` | Show available tools, skills, and architecture |
| `/mempalace:init` | Set up MemPalace -- install, configure MCP, onboard |
| `/mempalace:search` | Search your memories across the palace |
| `/mempalace:mine` | Mine projects and conversations into the palace |
| `/mempalace:status` | Show palace overview -- wings, rooms, drawer counts |

## Hooks

MemPalace registers two hooks that run automatically:

- **Stop** -- Saves conversation context every 15 messages.
- **PreCompact** -- Preserves important memories before context compaction.

Set the `MEMPAL_DIR` environment variable to a directory path to automatically run `mempalace mine` on that directory during each save trigger.

## MCP Server

The plugin automatically configures a local MCP server with 19 tools for storing, searching, and managing memories. No manual MCP setup is required -- `/mempalace:init` handles everything.

## Full Documentation

See the main [README](../README.md) for complete documentation, architecture details, and advanced usage.

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
