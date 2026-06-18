---
argos_import: project_file
source_path: mempalace-develop/website/guide/openclaw.md
source_abs: F:\debug\argoss\mempalace-develop\website\guide\openclaw.md
source_ext: .md
source_sha256: 15ee9945a8b0fd2300171f5d4218e2b20b1965ce0dffdbfdbb4dbcafd58f1be8
text_sha256: 15ee9945a8b0fd2300171f5d4218e2b20b1965ce0dffdbfdbb4dbcafd58f1be8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# openclaw.md

- Source: `mempalace-develop/website/guide/openclaw.md`
- Extract: `text`
- SHA256: `15ee9945a8b0fd2300171f5d4218e2b20b1965ce0dffdbfdbb4dbcafd58f1be8`

## Content

# OpenClaw Skill

MemPalace provides an official skill for [OpenClaw](https://github.com/openclaw/openclaw), making it trivial to give your ClawHub agents complete access to the palace's declarative memory and knowledge graph.

## Installation

The skill is built right into the `integrations/openclaw` directory of MemPalace. 

You can add MemPalace as an MCP server to OpenClaw via the CLI:

```bash
openclaw mcp set mempalace '{"command":"python3","args":["-m","mempalace.mcp_server"]}'
```

Or by directly editing your OpenClaw configuration:

```json
{
  "mcpServers": {
    "mempalace": {
      "command": "python3",
      "args": ["-m", "mempalace.mcp_server"]
    }
  }
}
```

## How It Works

Once connected, OpenClaw agents receive all 19 tools along with the **Memory Protocol**—a strict behavioral guide indicating they should:
1. **Never guess**: Query `mempalace_search` or `mempalace_kg_query` before confidently answering.
2. **Keep an agent diary**: Maintain continuity between sessions by writing to `mempalace_diary_write`.
3. **Manage the Knowledge Graph**: Update declarative facts when things change using `mempalace_kg_add` and `mempalace_kg_invalidate`.

By connecting OpenClaw to MemPalace, you get both autonomous code execution and persistent, high-recall memory in the same workflow.

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
