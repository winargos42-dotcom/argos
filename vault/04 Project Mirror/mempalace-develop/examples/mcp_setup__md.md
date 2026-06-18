---
argos_import: project_file
source_path: mempalace-develop/examples/mcp_setup.md
source_abs: F:\debug\argoss\mempalace-develop\examples\mcp_setup.md
source_ext: .md
source_sha256: 283c780343c8244d284b4e1ba5eeed60433a8432beae76271bf641665aa4983d
text_sha256: 283c780343c8244d284b4e1ba5eeed60433a8432beae76271bf641665aa4983d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# mcp_setup.md

- Source: `mempalace-develop/examples/mcp_setup.md`
- Extract: `text`
- SHA256: `283c780343c8244d284b4e1ba5eeed60433a8432beae76271bf641665aa4983d`

## Content

# MCP Integration — Claude Code

## Setup

Run the MCP server:

```bash
python -m mempalace.mcp_server
```

Or add it to Claude Code:

```bash
claude mcp add mempalace -- python -m mempalace.mcp_server
```

## Available Tools

The server exposes the full MemPalace MCP toolset. Common entry points include:

- **mempalace_status** — palace stats (wings, rooms, drawer counts)
- **mempalace_search** — semantic search across all memories
- **mempalace_list_wings** — list all projects in the palace

## Usage in Claude Code

Once configured, Claude Code can search your memories directly during conversations.

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
