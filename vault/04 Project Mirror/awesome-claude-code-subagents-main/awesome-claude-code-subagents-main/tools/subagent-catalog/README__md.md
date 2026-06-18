---
argos_import: project_file
source_path: awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/README.md
source_abs: F:\debug\argoss\awesome-claude-code-subagents-main\awesome-claude-code-subagents-main\tools\subagent-catalog\README.md
source_ext: .md
source_sha256: 2db957a64f88dc092176532d638e71bc27e28a33aea61252a785f746a97078db
text_sha256: 2db957a64f88dc092176532d638e71bc27e28a33aea61252a785f746a97078db
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:16
---

# README.md

- Source: `awesome-claude-code-subagents-main/awesome-claude-code-subagents-main/tools/subagent-catalog/README.md`
- Extract: `text`
- SHA256: `2db957a64f88dc092176532d638e71bc27e28a33aea61252a785f746a97078db`

## Content

# subagent-catalog

A Claude Code skill for browsing and fetching subagents from the [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) catalog.

## Installation

Copy the `subagent-catalog/` folder to `~/.claude/commands/`:

```bash
cp -r tools/subagent-catalog ~/.claude/commands/
```

## Usage

| Command | Description |
|---------|-------------|
| `/subagent-catalog:search <query>` | Find agents by name, description, or category |
| `/subagent-catalog:fetch <name>` | Get full agent definition |
| `/subagent-catalog:list` | Browse all categories |
| `/subagent-catalog:invalidate` | Clear cache (add `--fetch` to refresh immediately) |

## Examples

**Find security-related agents:**
```
/subagent-catalog:search security
```

**Get the code-reviewer definition:**
```
/subagent-catalog:fetch code-reviewer
```

**Browse all available agents:**
```
/subagent-catalog:list
```

## Features

- **Smart caching**: 12-hour TTL with graceful fallback on network failure
- **Atomic updates**: Uses tmp file + mv pattern to prevent partial writes
- **Cross-platform**: Works on macOS and Linux
- **Best practices**: Follows Anthropic skill authoring guidelines

## Cache

- **Location**: `~/.claude/cache/subagent-catalog.md`
- **TTL**: 12 hours (configurable in `config.sh`)
- **Behavior**: Auto-refreshes when stale, falls back to old cache on network failure

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Stale results | `/subagent-catalog:invalidate --fetch` |
| Network error | Check connection, retry |
| Agent not found | `/subagent-catalog:search <partial-name>` first |

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
