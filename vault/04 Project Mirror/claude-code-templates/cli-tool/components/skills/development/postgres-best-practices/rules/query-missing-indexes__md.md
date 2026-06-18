---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/postgres-best-practices/rules/query-missing-indexes.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\postgres-best-practices\rules\query-missing-indexes.md
source_ext: .md
source_sha256: 15ddf120c86020612d2713225c850e0e4f022b38021f40f45e5bbe58f245dcc3
text_sha256: 91ad8b0ff4365704b4830a7f077c6f140f7140fd5d3ce5cd0b92b160cf9e25f1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# query-missing-indexes.md

- Source: `claude-code-templates/cli-tool/components/skills/development/postgres-best-practices/rules/query-missing-indexes.md`
- Extract: `text`
- SHA256: `15ddf120c86020612d2713225c850e0e4f022b38021f40f45e5bbe58f245dcc3`

## Content

---
title: Add Indexes on WHERE and JOIN Columns
impact: CRITICAL
impactDescription: 100-1000x faster queries on large tables
tags: indexes, performance, sequential-scan, query-optimization
---

## Add Indexes on WHERE and JOIN Columns

Queries filtering or joining on unindexed columns cause full table scans, which become exponentially slower as tables grow.

**Incorrect (sequential scan on large table):**

```sql
-- No index on customer_id causes full table scan
select * from orders where customer_id = 123;

-- EXPLAIN shows: Seq Scan on orders (cost=0.00..25000.00 rows=100 width=85)
```

**Correct (index scan):**

```sql
-- Create index on frequently filtered column
create index orders_customer_id_idx on orders (customer_id);

select * from orders where customer_id = 123;

-- EXPLAIN shows: Index Scan using orders_customer_id_idx (cost=0.42..8.44 rows=100 width=85)
```

For JOIN columns, always index the foreign key side:

```sql
-- Index the referencing column
create index orders_customer_id_idx on orders (customer_id);

select c.name, o.total
from customers c
join orders o on o.customer_id = c.id;
```

Reference: [Query Optimization](https://supabase.com/docs/guides/database/query-optimization)

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
