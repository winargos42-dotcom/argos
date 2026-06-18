---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/design-database-schema.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\design-database-schema.md
source_ext: .md
source_sha256: d5ab4eeb98eb5d431767ac44f992dc90c226d4575703342e0db2cd9bb8fc87d8
text_sha256: c23f6079a4a9bdfaf45e38732937bc57bd27fb5e26e5246fe956ab14dff4e28a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# design-database-schema.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/design-database-schema.md`
- Extract: `text`
- SHA256: `d5ab4eeb98eb5d431767ac44f992dc90c226d4575703342e0db2cd9bb8fc87d8`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [schema-type] | --relational | --nosql | --hybrid | --normalize
description: Design optimized database schemas with proper relationships, constraints, and performance considerations
---

# Design Database Schema

Design optimized database schemas with comprehensive data modeling: **$ARGUMENTS**

## Current Project Context

- Application type: Based on $ARGUMENTS or codebase analysis
- Data requirements: @requirements/ or project documentation
- Existing schema: @prisma/schema.prisma or @migrations/ or database dumps
- Performance needs: Expected scale, query patterns, and data volume

## Task

Design comprehensive database schema with optimal structure and performance:

**Schema Type**: Use $ARGUMENTS to specify relational, NoSQL, hybrid approach, or normalization level

**Design Framework**:
1. **Requirements Analysis** - Business entities, relationships, data flow, and access patterns
2. **Entity Modeling** - Tables/collections, attributes, primary/foreign keys, constraints
3. **Relationship Design** - One-to-one, one-to-many, many-to-many associations
4. **Normalization Strategy** - Data consistency vs performance trade-offs
5. **Performance Optimization** - Indexing strategy, query optimization, partitioning
6. **Security Design** - Access control, data encryption, audit trails

**Advanced Patterns**: Implement temporal data, soft deletes, JSONB fields, full-text search, audit logging, and scalability patterns.

**Validation**: Ensure referential integrity, data consistency, query performance, and future extensibility.

**Output**: Complete schema design with DDL scripts, ER diagrams, performance analysis, and migration strategy.

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
