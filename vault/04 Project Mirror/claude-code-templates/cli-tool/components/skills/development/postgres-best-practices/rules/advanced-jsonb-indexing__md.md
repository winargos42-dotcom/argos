---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/postgres-best-practices/rules/advanced-jsonb-indexing.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\postgres-best-practices\rules\advanced-jsonb-indexing.md
source_ext: .md
source_sha256: 9bcbf7da33f6fe6fa9525680ca26d4e3412b534104cffb5f8529596d76631e4f
text_sha256: 24cacf6a8bc35901dd566d24502ce8e57f810a5c196b897e61d52726e521d106
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# advanced-jsonb-indexing.md

- Source: `claude-code-templates/cli-tool/components/skills/development/postgres-best-practices/rules/advanced-jsonb-indexing.md`
- Extract: `text`
- SHA256: `9bcbf7da33f6fe6fa9525680ca26d4e3412b534104cffb5f8529596d76631e4f`

## Content

---
title: Index JSONB Columns for Efficient Querying
impact: MEDIUM
impactDescription: 10-100x faster JSONB queries with proper indexing
tags: jsonb, gin, indexes, json
---

## Index JSONB Columns for Efficient Querying

JSONB queries without indexes scan the entire table. Use GIN indexes for containment queries.

**Incorrect (no index on JSONB):**

```sql
create table products (
  id bigint primary key,
  attributes jsonb
);

-- Full table scan for every query
select * from products where attributes @> '{"color": "red"}';
select * from products where attributes->>'brand' = 'Nike';
```

**Correct (GIN index for JSONB):**

```sql
-- GIN index for containment operators (@>, ?, ?&, ?|)
create index products_attrs_gin on products using gin (attributes);

-- Now containment queries use the index
select * from products where attributes @> '{"color": "red"}';

-- For specific key lookups, use expression index
create index products_brand_idx on products ((attributes->>'brand'));
select * from products where attributes->>'brand' = 'Nike';
```

Choose the right operator class:

```sql
-- jsonb_ops (default): supports all operators, larger index
create index idx1 on products using gin (attributes);

-- jsonb_path_ops: only @> operator, but 2-3x smaller index
create index idx2 on products using gin (attributes jsonb_path_ops);
```

Reference: [JSONB Indexes](https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING)

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
