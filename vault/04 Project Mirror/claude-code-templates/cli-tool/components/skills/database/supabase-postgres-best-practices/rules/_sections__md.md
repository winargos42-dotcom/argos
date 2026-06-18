---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/supabase-postgres-best-practices/rules/_sections.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\supabase-postgres-best-practices\rules\_sections.md
source_ext: .md
source_sha256: ad2d6f6b0938ff844f7f8971153ab6d08a03ef6511b02fb9cee9336c7b209e93
text_sha256: c9e992612b422c7122de0b7542ebc2450db283edaab08cfe86c6d657fcccccd5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# _sections.md

- Source: `claude-code-templates/cli-tool/components/skills/database/supabase-postgres-best-practices/rules/_sections.md`
- Extract: `text`
- SHA256: `ad2d6f6b0938ff844f7f8971153ab6d08a03ef6511b02fb9cee9336c7b209e93`

## Content

# Section Definitions

This file defines the rule categories for Postgres best practices. Rules are automatically assigned to sections based on their filename prefix.

Take the examples below as pure demonstrative. Replace each section with the actual rule categories for Postgres best practices.

---

## 1. Query Performance (query)
**Impact:** CRITICAL
**Description:** Slow queries, missing indexes, inefficient query plans. The most common source of Postgres performance issues.

## 2. Connection Management (conn)
**Impact:** CRITICAL
**Description:** Connection pooling, limits, and serverless strategies. Critical for applications with high concurrency or serverless deployments.

## 3. Security & RLS (security)
**Impact:** CRITICAL
**Description:** Row-Level Security policies, privilege management, and authentication patterns.

## 4. Schema Design (schema)
**Impact:** HIGH
**Description:** Table design, index strategies, partitioning, and data type selection. Foundation for long-term performance.

## 5. Concurrency & Locking (lock)
**Impact:** MEDIUM-HIGH
**Description:** Transaction management, isolation levels, deadlock prevention, and lock contention patterns.

## 6. Data Access Patterns (data)
**Impact:** MEDIUM
**Description:** N+1 query elimination, batch operations, cursor-based pagination, and efficient data fetching.

## 7. Monitoring & Diagnostics (monitor)
**Impact:** LOW-MEDIUM
**Description:** Using pg_stat_statements, EXPLAIN ANALYZE, metrics collection, and performance diagnostics.

## 8. Advanced Features (advanced)
**Impact:** LOW
**Description:** Full-text search, JSONB optimization, PostGIS, extensions, and advanced Postgres features.

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
