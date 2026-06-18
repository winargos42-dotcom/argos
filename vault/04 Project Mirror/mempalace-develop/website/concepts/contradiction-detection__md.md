---
argos_import: project_file
source_path: mempalace-develop/website/concepts/contradiction-detection.md
source_abs: F:\debug\argoss\mempalace-develop\website\concepts\contradiction-detection.md
source_ext: .md
source_sha256: 8a28392ff8cb52501d0ec9e97da90e5d861c74dfd24128ae0313142353bcf8bf
text_sha256: 8a28392ff8cb52501d0ec9e97da90e5d861c74dfd24128ae0313142353bcf8bf
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# contradiction-detection.md

- Source: `mempalace-develop/website/concepts/contradiction-detection.md`
- Extract: `text`
- SHA256: `8a28392ff8cb52501d0ec9e97da90e5d861c74dfd24128ae0313142353bcf8bf`

## Content

# Contradiction Detection

::: warning Experimental
Contradiction detection is a planned capability, not a shipped end-to-end feature in the current MCP workflow. The examples below show the intended behavior rather than a fully integrated command path.
:::

## What It Does

Checks assertions against entity facts in the knowledge graph. When enabled, it catches contradictions like:

```
Input:  "Soren finished the auth migration"
Output: 🔴 AUTH-MIGRATION: attribution conflict — Maya was assigned, not Soren

Input:  "Kai has been here 2 years"
Output: 🟡 KAI: wrong_tenure — records show 3 years (started 2023-04)

Input:  "The sprint ends Friday"
Output: 🟡 SPRINT: stale_date — current sprint ends Thursday (updated 2 days ago)
```

## How It Works

Facts are checked against the knowledge graph:
- **Attribution conflicts** — the wrong person credited for a task
- **Temporal errors** — wrong dates, tenures, or durations
- **Stale information** — facts that have been superseded

Ages, dates, and tenures are calculated dynamically from the entity's recorded facts — not hardcoded.

## Status

The current codebase includes the temporal knowledge graph primitives needed for this direction, but not a complete contradiction-checking tool exposed through the CLI or MCP server.

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
