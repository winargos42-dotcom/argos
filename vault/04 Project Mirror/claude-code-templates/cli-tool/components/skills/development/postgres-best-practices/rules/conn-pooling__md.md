---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/postgres-best-practices/rules/conn-pooling.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\postgres-best-practices\rules\conn-pooling.md
source_ext: .md
source_sha256: 60cd5f7942c44bdf6d8622a49a2e9f0f7fd01daf8e62bd1bd66b195cd6942975
text_sha256: 88cf086bf98ba865d2e9d0579974e1366b14157619d6a93e7da77be91084e4a5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# conn-pooling.md

- Source: `claude-code-templates/cli-tool/components/skills/development/postgres-best-practices/rules/conn-pooling.md`
- Extract: `text`
- SHA256: `60cd5f7942c44bdf6d8622a49a2e9f0f7fd01daf8e62bd1bd66b195cd6942975`

## Content

---
title: Use Connection Pooling for All Applications
impact: CRITICAL
impactDescription: Handle 10-100x more concurrent users
tags: connection-pooling, pgbouncer, performance, scalability
---

## Use Connection Pooling for All Applications

Postgres connections are expensive (1-3MB RAM each). Without pooling, applications exhaust connections under load.

**Incorrect (new connection per request):**

```sql
-- Each request creates a new connection
-- Application code: db.connect() per request
-- Result: 500 concurrent users = 500 connections = crashed database

-- Check current connections
select count(*) from pg_stat_activity;  -- 487 connections!
```

**Correct (connection pooling):**

```sql
-- Use a pooler like PgBouncer between app and database
-- Application connects to pooler, pooler reuses a small pool to Postgres

-- Configure pool_size based on: (CPU cores * 2) + spindle_count
-- Example for 4 cores: pool_size = 10

-- Result: 500 concurrent users share 10 actual connections
select count(*) from pg_stat_activity;  -- 10 connections
```

Pool modes:

- **Transaction mode**: connection returned after each transaction (best for most apps)
- **Session mode**: connection held for entire session (needed for prepared statements, temp tables)

Reference: [Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)

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
