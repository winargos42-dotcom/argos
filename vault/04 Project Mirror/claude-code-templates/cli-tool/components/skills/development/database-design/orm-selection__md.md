---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/database-design/orm-selection.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\database-design\orm-selection.md
source_ext: .md
source_sha256: d00d3c70aa077ebcaaaafa4cce867c8febd7a74655bb9b1cde23acd02b67f5a4
text_sha256: 11ece2e816949e26a7019b84004e240a9f9ab0b38c4f454bd522dd251c5dac97
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:38
---

# orm-selection.md

- Source: `claude-code-templates/cli-tool/components/skills/development/database-design/orm-selection.md`
- Extract: `text`
- SHA256: `d00d3c70aa077ebcaaaafa4cce867c8febd7a74655bb9b1cde23acd02b67f5a4`

## Content

# ORM Selection (2025)

> Choose ORM based on deployment and DX needs.

## Decision Tree

```
What's the context?
│
├── Edge deployment / Bundle size matters
│   └── Drizzle (smallest, SQL-like)
│
├── Best DX / Schema-first
│   └── Prisma (migrations, studio)
│
├── Maximum control
│   └── Raw SQL with query builder
│
└── Python ecosystem
    └── SQLAlchemy 2.0 (async support)
```

## Comparison

| ORM | Best For | Trade-offs |
|-----|----------|------------|
| **Drizzle** | Edge, TypeScript | Newer, less examples |
| **Prisma** | DX, schema management | Heavier, not edge-ready |
| **Kysely** | Type-safe SQL builder | Manual migrations |
| **Raw SQL** | Complex queries, control | Manual type safety |

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
