---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/sync-linear-to-issues.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\sync-linear-to-issues.md
source_ext: .md
source_sha256: f4c4fe42dcd9ffad5c49310c2d7aed81e6594611be3ffab54e6a22fc73101913
text_sha256: 41e6e8bc022cd4cb9a3d24eebef6add65c1316fc9eb7ba4840f504b9bdc1758a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# sync-linear-to-issues.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/sync-linear-to-issues.md`
- Extract: `text`
- SHA256: `f4c4fe42dcd9ffad5c49310c2d7aed81e6594611be3ffab54e6a22fc73101913`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [sync-scope] | --team | --project | --priority | --states
description: Sync Linear tasks to GitHub issues with state mapping and attachment handling
---

# Sync Linear to Issues

Sync Linear tasks to GitHub issues with comprehensive state and field mapping: **$ARGUMENTS**

## Current Linear Context

- Linear teams: Available teams and project assignments
- Task count: Linear task query to determine scope
- Target repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "No repo context"`
- User mappings: Linear email to GitHub username correspondence

## Task

Execute comprehensive synchronization of Linear tasks to GitHub issues:

**Sync Scope**: Use $ARGUMENTS to filter by Linear team, project, priority levels, or task states

**Synchronization Framework**:
1. **Task Discovery** - Query Linear tasks with filters, extract metadata, validate requirements, prioritize sync
2. **State Mapping** - Transform Linear states to GitHub equivalents, handle priority conversion, map project assignments
3. **Content Transformation** - Build GitHub issue body, preserve formatting, handle attachments, maintain structure
4. **GitHub Integration** - Create issues with proper labels, assign users, set milestones, manage relationships
5. **Attachment Migration** - Download Linear attachments, upload to GitHub, update references, maintain accessibility
6. **Comment Synchronization** - Transfer comments with attribution, preserve context, handle mentions, maintain threading

**Advanced Features**: Intelligent state mapping, attachment handling, comment threading, user mention translation, comprehensive validation.

**Data Fidelity**: Preserve Linear formatting, maintain task relationships, keep timestamps, ensure reference integrity.

**Output**: Complete synchronization results with created issues, attachment migrations, comment transfers, and comprehensive sync reporting.

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
