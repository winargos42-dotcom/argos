---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/database-design/database-selection.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\database-design\database-selection.md
source_ext: .md
source_sha256: 710557db56c0e594f292f2221f0aa6e9a2466e3ab57818ebbd7bb69c2ab95ba6
text_sha256: 3655cdd3a38a9ca1ae8408be8057ea628b08bf9ab22460b1bc571228dd2ba6c6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:38
---

# database-selection.md

- Source: `claude-code-templates/cli-tool/components/skills/development/database-design/database-selection.md`
- Extract: `text`
- SHA256: `710557db56c0e594f292f2221f0aa6e9a2466e3ab57818ebbd7bb69c2ab95ba6`

## Content

# Database Selection (2025)

> Choose database based on context, not default.

## Decision Tree

```
What are your requirements?
│
├── Full relational features needed
│   ├── Self-hosted → PostgreSQL
│   └── Serverless → Neon, Supabase
│
├── Edge deployment / Ultra-low latency
│   └── Turso (edge SQLite)
│
├── AI / Vector search
│   └── PostgreSQL + pgvector
│
├── Simple / Embedded / Local
│   └── SQLite
│
└── Global distribution
    └── PlanetScale, CockroachDB, Turso
```

## Comparison

| Database | Best For | Trade-offs |
|----------|----------|------------|
| **PostgreSQL** | Full features, complex queries | Needs hosting |
| **Neon** | Serverless PG, branching | PG complexity |
| **Turso** | Edge, low latency | SQLite limitations |
| **SQLite** | Simple, embedded, local | Single-writer |
| **PlanetScale** | MySQL, global scale | No foreign keys |

## Questions to Ask

1. What's the deployment environment?
2. How complex are the queries?
3. Is edge/serverless important?
4. Vector search needed?
5. Global distribution required?

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
