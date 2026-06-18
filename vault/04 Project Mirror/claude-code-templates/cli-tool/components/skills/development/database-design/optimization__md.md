---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/database-design/optimization.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\database-design\optimization.md
source_ext: .md
source_sha256: f6103c5e6c1dc063fc1a6703c6911b70b767f85fb42ecbd310408735beef41c9
text_sha256: 10a6f484fdae9973957030d8ef47bad4ffba9f7709e9c824883a97f92925a722
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:38
---

# optimization.md

- Source: `claude-code-templates/cli-tool/components/skills/development/database-design/optimization.md`
- Extract: `text`
- SHA256: `f6103c5e6c1dc063fc1a6703c6911b70b767f85fb42ecbd310408735beef41c9`

## Content

# Query Optimization

> N+1 problem, EXPLAIN ANALYZE, optimization priorities.

## N+1 Problem

```
What is N+1?
├── 1 query to get parent records
├── N queries to get related records
└── Very slow!

Solutions:
├── JOIN → Single query with all data
├── Eager loading → ORM handles JOIN
├── DataLoader → Batch and cache (GraphQL)
└── Subquery → Fetch related in one query
```

## Query Analysis Mindset

```
Before optimizing:
├── EXPLAIN ANALYZE the query
├── Look for Seq Scan (full table scan)
├── Check actual vs estimated rows
└── Identify missing indexes
```

## Optimization Priorities

1. **Add missing indexes** (most common issue)
2. **Select only needed columns** (not SELECT *)
3. **Use proper JOINs** (avoid subqueries when possible)
4. **Limit early** (pagination at database level)
5. **Cache** (when appropriate)

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
