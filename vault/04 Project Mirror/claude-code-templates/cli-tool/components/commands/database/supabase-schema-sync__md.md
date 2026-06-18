---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/database/supabase-schema-sync.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\database\supabase-schema-sync.md
source_ext: .md
source_sha256: 5b486c124ce1daa4679eb5fdc2673a04df77464365abfeb8d74fe6ba0c21c190
text_sha256: 86db634b5dfc2a6e7f875c5513445142d4cd7f701d0669bfe463330ed96142ee
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# supabase-schema-sync.md

- Source: `claude-code-templates/cli-tool/components/commands/database/supabase-schema-sync.md`
- Extract: `text`
- SHA256: `5b486c124ce1daa4679eb5fdc2673a04df77464365abfeb8d74fe6ba0c21c190`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [action] | --pull | --push | --diff | --validate
description: Synchronize database schema with Supabase using MCP integration
---

# Supabase Schema Sync

Synchronize database schema between local and Supabase with comprehensive validation: **$ARGUMENTS**

## Current Supabase Context

- MCP connection: Supabase MCP server with read-only access configured
- Local schema: !`find . -name "schema.sql" -o -name "migrations" -type d | head -3` local database files
- Project config: !`find . -name "supabase" -type d -o -name ".env*" | grep -v node_modules | head -3` configuration files
- Git status: !`git status --porcelain | grep -E "\\.sql$|\\.ts$" | head -5` database-related changes

## Task

Execute comprehensive schema synchronization with Supabase integration:

**Sync Action**: Use $ARGUMENTS to specify pull from remote, push to remote, diff comparison, or schema validation

**Schema Synchronization Framework**:
1. **MCP Integration** - Connect to Supabase via MCP server, authenticate with project credentials, validate connection status
2. **Schema Analysis** - Compare local vs remote schema, identify structural differences, analyze migration requirements, assess breaking changes
3. **Sync Operations** - Execute pull/push operations, apply schema migrations, handle conflict resolution, validate data integrity
4. **Validation Process** - Verify schema consistency, validate foreign key constraints, check index performance, test query compatibility
5. **Migration Management** - Generate migration scripts, track version history, implement rollback procedures, optimize execution order
6. **Safety Checks** - Backup critical data, validate permissions, check production impact, implement dry-run mode

**Advanced Features**: Automated conflict resolution, schema version control, performance impact analysis, team collaboration workflows, CI/CD integration.

**Quality Assurance**: Schema validation, data integrity checks, performance optimization, rollback readiness, team synchronization.

**Output**: Complete schema sync with validation reports, migration scripts, conflict resolution, and team collaboration updates.

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
