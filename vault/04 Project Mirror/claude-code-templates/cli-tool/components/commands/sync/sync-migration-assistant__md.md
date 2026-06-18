---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/sync-migration-assistant.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\sync-migration-assistant.md
source_ext: .md
source_sha256: 6e21dff56ac9de743fa92ece7c92fac14f711fb4f550c0b27e4b45ba10f90b49
text_sha256: 665b95ab6a25fe29f982da812b6c814180327aee7a4dbf52f498ac08deb6380b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# sync-migration-assistant.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/sync-migration-assistant.md`
- Extract: `text`
- SHA256: `6e21dff56ac9de743fa92ece7c92fac14f711fb4f550c0b27e4b45ba10f90b49`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [migration-type] | --github-to-linear | --linear-to-github | --bidirectional | --validate
description: Comprehensive migration assistant for large-scale GitHub-Linear data transitions with validation and rollback
---

# Sync Migration Assistant

Execute comprehensive data migration between GitHub and Linear with enterprise-grade capabilities: **$ARGUMENTS**

## Current Migration Environment

- Source system: !`gh --version 2>/dev/null && echo "GitHub CLI available" || echo "GitHub CLI needed"`
- Target system: Linear MCP server connectivity and authentication status
- Migration scope: Analysis of data volume and complexity for planning
- Infrastructure: Database, queue services, and processing capacity assessment

## Task

Implement large-scale data migration with comprehensive validation and enterprise features:

**Migration Type**: Use $ARGUMENTS to specify GitHub-to-Linear, Linear-to-GitHub, bidirectional setup, or validation mode

**Migration Framework**:
1. **Pre-Migration Assessment** - Data volume analysis, dependency mapping, risk assessment, resource planning
2. **Migration Planning** - Phased approach design, rollback strategy, validation checkpoints, timeline estimation
3. **Data Extraction** - Comprehensive data harvesting, relationship preservation, metadata capture, error handling
4. **Transformation Engine** - Field mapping, format conversion, validation rules, data enrichment
5. **Migration Execution** - Batch processing, progress tracking, error recovery, quality assurance
6. **Post-Migration Validation** - Data integrity verification, relationship validation, performance testing, rollback readiness

**Enterprise Features**: Large-scale batch processing, comprehensive error recovery, detailed audit trails, rollback capabilities, performance optimization.

**Quality Assurance**: Multi-stage validation, data integrity checks, relationship verification, comprehensive testing, enterprise monitoring.

**Output**: Complete migration system with phased execution, comprehensive validation, detailed reporting, and enterprise-grade reliability for large-scale data transitions.

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
