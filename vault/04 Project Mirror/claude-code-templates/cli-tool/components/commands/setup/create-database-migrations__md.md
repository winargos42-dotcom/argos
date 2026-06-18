---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/create-database-migrations.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\create-database-migrations.md
source_ext: .md
source_sha256: 1feddcf22fc44feffca6d46ed5b4e978d6ab95761e99c98ff6ea1478c5692d2e
text_sha256: 73c999c12efada2e36c446f032e1643ade40339e97667a47254d80c19d53f58f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# create-database-migrations.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/create-database-migrations.md`
- Extract: `text`
- SHA256: `1feddcf22fc44feffca6d46ed5b4e978d6ab95761e99c98ff6ea1478c5692d2e`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [migration-name] | --create-table | --add-column | --alter-table
description: Create and manage database migrations with proper versioning and rollback support
---

# Create Database Migrations

Create and manage database migrations: **$ARGUMENTS**

## Current Database State

- ORM detection: @package.json or @requirements.txt (detect Sequelize, Prisma, Alembic, etc.)
- Migration files: !`find . -name "*migration*" -type f | head -5`
- Database config: @config/database.* or @prisma/schema.prisma
- Current schema: !`ls migrations/ 2>/dev/null | wc -l` migrations found

## Task

Create comprehensive database migrations with proper versioning and rollback capabilities:

**Migration Types**: Use $ARGUMENTS to specify table creation, column addition, table alteration, or data migration

**Migration Framework**:
1. **Migration Planning** - Analyze schema changes, dependencies, and data impact
2. **Migration Generation** - Create timestamped migration files with up/down methods
3. **Schema Updates** - Table creation, column modifications, index management
4. **Data Migrations** - Safe data transformations and backfills
5. **Rollback Strategy** - Implement reliable rollback procedures for each change
6. **Testing** - Validate migrations in development and staging environments

**Best Practices**: Follow database-specific conventions, maintain referential integrity, handle large datasets efficiently, and ensure zero-downtime deployments.

**Output**: Production-ready migration files with comprehensive rollback support, proper indexing, and data safety measures.

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
