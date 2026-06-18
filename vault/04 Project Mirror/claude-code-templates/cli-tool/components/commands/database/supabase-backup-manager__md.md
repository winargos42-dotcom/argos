---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/database/supabase-backup-manager.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\database\supabase-backup-manager.md
source_ext: .md
source_sha256: 1a23591ba0ed70da6a40d04a935c31ff028ab82eac1d68069fb11c9af36f6da5
text_sha256: ec273263b9e6c7080a48874046720b87abc8f792480b061602d288fe2ab528d9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# supabase-backup-manager.md

- Source: `claude-code-templates/cli-tool/components/commands/database/supabase-backup-manager.md`
- Extract: `text`
- SHA256: `1a23591ba0ed70da6a40d04a935c31ff028ab82eac1d68069fb11c9af36f6da5`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [operation] | --backup | --restore | --schedule | --validate | --cleanup
description: Manage Supabase database backups with automated scheduling and recovery procedures
---

# Supabase Backup Manager

Manage comprehensive Supabase database backups with automated scheduling and recovery validation: **$ARGUMENTS**

## Current Backup Context

- Supabase project: MCP integration for backup operations and status monitoring
- Backup storage: Current backup configuration and storage capacity
- Recovery testing: Last backup validation and recovery procedure verification
- Automation status: !`find . -name "*.yml" -o -name "*.json" | xargs grep -l "backup\|cron" 2>/dev/null | head -3` scheduled backup configuration

## Task

Execute comprehensive backup management with automated procedures and recovery validation:

**Backup Operation**: Use $ARGUMENTS to specify backup creation, data restoration, schedule management, backup validation, or cleanup procedures

**Backup Management Framework**:
1. **Backup Strategy** - Design backup schedules, implement retention policies, configure incremental backups, optimize storage usage
2. **Automated Backup** - Create database snapshots, export schema and data, validate backup integrity, monitor backup completion
3. **Recovery Procedures** - Test restore processes, validate data integrity, implement point-in-time recovery, optimize recovery time
4. **Schedule Management** - Configure automated backup schedules, implement backup monitoring, setup failure notifications, optimize backup windows
5. **Storage Optimization** - Manage backup storage, implement compression strategies, archive old backups, monitor storage costs
6. **Disaster Recovery** - Plan disaster recovery procedures, test recovery scenarios, document recovery processes, validate business continuity

**Advanced Features**: Automated backup validation, recovery time optimization, cross-region backup replication, backup encryption, compliance reporting.

**Monitoring Integration**: Backup success monitoring, failure alerting, storage usage tracking, recovery time measurement, compliance reporting.

**Output**: Complete backup management system with automated schedules, recovery procedures, validation reports, and disaster recovery planning.

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
