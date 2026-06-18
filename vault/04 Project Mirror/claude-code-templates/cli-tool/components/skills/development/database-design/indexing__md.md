---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/database-design/indexing.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\database-design\indexing.md
source_ext: .md
source_sha256: fc215671e11f302f3523a0b2234f1d6b9fe6c7b3f5038ba36fd65fc4652bd03c
text_sha256: eec8ce01e7c1c8ec2aed7a96d260a52b12d90c2996288e32814a8d9cf29cc22a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:38
---

# indexing.md

- Source: `claude-code-templates/cli-tool/components/skills/development/database-design/indexing.md`
- Extract: `text`
- SHA256: `fc215671e11f302f3523a0b2234f1d6b9fe6c7b3f5038ba36fd65fc4652bd03c`

## Content

# Indexing Principles

> When and how to create indexes effectively.

## When to Create Indexes

```
Index these:
├── Columns in WHERE clauses
├── Columns in JOIN conditions
├── Columns in ORDER BY
├── Foreign key columns
└── Unique constraints

Don't over-index:
├── Write-heavy tables (slower inserts)
├── Low-cardinality columns
├── Columns rarely queried
```

## Index Type Selection

| Type | Use For |
|------|---------|
| **B-tree** | General purpose, equality & range |
| **Hash** | Equality only, faster |
| **GIN** | JSONB, arrays, full-text |
| **GiST** | Geometric, range types |
| **HNSW/IVFFlat** | Vector similarity (pgvector) |

## Composite Index Principles

```
Order matters for composite indexes:
├── Equality columns first
├── Range columns last
├── Most selective first
└── Match query pattern
```

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
