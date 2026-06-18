---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/postgres-best-practices/rules/schema-partitioning.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\postgres-best-practices\rules\schema-partitioning.md
source_ext: .md
source_sha256: d940ee09551e970f97c629e816502989c37f7dcea1df94b4b52f79f6eefc9971
text_sha256: 541e13fbeaf4bb1485c9059d4c9417dbdb766cf16f4237cd63a04ada7ec45b90
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# schema-partitioning.md

- Source: `claude-code-templates/cli-tool/components/skills/development/postgres-best-practices/rules/schema-partitioning.md`
- Extract: `text`
- SHA256: `d940ee09551e970f97c629e816502989c37f7dcea1df94b4b52f79f6eefc9971`

## Content

---
title: Partition Large Tables for Better Performance
impact: MEDIUM-HIGH
impactDescription: 5-20x faster queries and maintenance on large tables
tags: partitioning, large-tables, time-series, performance
---

## Partition Large Tables for Better Performance

Partitioning splits a large table into smaller pieces, improving query performance and maintenance operations.

**Incorrect (single large table):**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz,
  data jsonb
);

-- 500M rows, queries scan everything
select * from events where created_at > '2024-01-01';  -- Slow
vacuum events;  -- Takes hours, locks table
```

**Correct (partitioned by time range):**

```sql
create table events (
  id bigint generated always as identity,
  created_at timestamptz not null,
  data jsonb
) partition by range (created_at);

-- Create partitions for each month
create table events_2024_01 partition of events
  for values from ('2024-01-01') to ('2024-02-01');

create table events_2024_02 partition of events
  for values from ('2024-02-01') to ('2024-03-01');

-- Queries only scan relevant partitions
select * from events where created_at > '2024-01-15';  -- Only scans events_2024_01+

-- Drop old data instantly
drop table events_2023_01;  -- Instant vs DELETE taking hours
```

When to partition:

- Tables > 100M rows
- Time-series data with date-based queries
- Need to efficiently drop old data

Reference: [Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)

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
