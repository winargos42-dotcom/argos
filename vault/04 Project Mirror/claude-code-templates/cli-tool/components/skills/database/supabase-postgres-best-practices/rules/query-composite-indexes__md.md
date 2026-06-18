---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/supabase-postgres-best-practices/rules/query-composite-indexes.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\supabase-postgres-best-practices\rules\query-composite-indexes.md
source_ext: .md
source_sha256: 7e75d1b4d4431cb874ecc28710e95b7d2d7364511daa5d2c8e9d7de7ce1d0054
text_sha256: 73e42424e671f0266e74fdb220db3196790f69fb43e2b19c7b9483eb4971b554
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# query-composite-indexes.md

- Source: `claude-code-templates/cli-tool/components/skills/database/supabase-postgres-best-practices/rules/query-composite-indexes.md`
- Extract: `text`
- SHA256: `7e75d1b4d4431cb874ecc28710e95b7d2d7364511daa5d2c8e9d7de7ce1d0054`

## Content

---
title: Create Composite Indexes for Multi-Column Queries
impact: HIGH
impactDescription: 5-10x faster multi-column queries
tags: indexes, composite-index, multi-column, query-optimization
---

## Create Composite Indexes for Multi-Column Queries

When queries filter on multiple columns, a composite index is more efficient than separate single-column indexes.

**Incorrect (separate indexes require bitmap scan):**

```sql
-- Two separate indexes
create index orders_status_idx on orders (status);
create index orders_created_idx on orders (created_at);

-- Query must combine both indexes (slower)
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**Correct (composite index):**

```sql
-- Single composite index (leftmost column first for equality checks)
create index orders_status_created_idx on orders (status, created_at);

-- Query uses one efficient index scan
select * from orders where status = 'pending' and created_at > '2024-01-01';
```

**Column order matters** - place equality columns first, range columns last:

```sql
-- Good: status (=) before created_at (>)
create index idx on orders (status, created_at);

-- Works for: WHERE status = 'pending'
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
-- Does NOT work for: WHERE created_at > '2024-01-01' (leftmost prefix rule)
```

Reference: [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)

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
