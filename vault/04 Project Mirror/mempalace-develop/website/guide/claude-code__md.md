---
argos_import: project_file
source_path: mempalace-develop/website/guide/claude-code.md
source_abs: F:\debug\argoss\mempalace-develop\website\guide\claude-code.md
source_ext: .md
source_sha256: 0965d0a894e73bee3e98bbcbeeac73e957fd9310b81e80cd290bbf92b7ab92a0
text_sha256: 0965d0a894e73bee3e98bbcbeeac73e957fd9310b81e80cd290bbf92b7ab92a0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# claude-code.md

- Source: `mempalace-develop/website/guide/claude-code.md`
- Extract: `text`
- SHA256: `0965d0a894e73bee3e98bbcbeeac73e957fd9310b81e80cd290bbf92b7ab92a0`

## Content

# Claude Code Plugin

The recommended way to use MemPalace with Claude Code — native marketplace install.

## Installation

```bash
claude plugin marketplace add milla-jovovich/mempalace
claude plugin install --scope user mempalace
```

Restart Claude Code, then type `/skills` to verify "mempalace" appears.

## How It Works

With the plugin installed, Claude Code automatically:
- Starts the MemPalace MCP server on launch
- Has access to all 19 tools
- Learns the AAAK dialect and memory protocol from the `mempalace_status` response
- Searches the palace before answering questions about past work

No manual configuration needed. Just ask:

> *"What did we decide about auth last month?"*

## Alternative: Manual MCP

If you prefer manual setup over the marketplace plugin:

```bash
claude mcp add mempalace -- python -m mempalace.mcp_server
```

Both approaches give identical functionality. The plugin approach handles server lifecycle automatically.

## Hooks

Set up [auto-save hooks](/guide/hooks) to ensure memories are saved automatically during long conversations.

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
