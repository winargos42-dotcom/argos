---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/linear-task-to-issue.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\linear-task-to-issue.md
source_ext: .md
source_sha256: 59f6608c9e9de2139e34403f6feade665d44ee1751d1558f5b00061d8da10886
text_sha256: db5ec1dcec4cf8abf25106f6b966547f431404d1eee35dd5bbed27c67f26e606
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# linear-task-to-issue.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/linear-task-to-issue.md`
- Extract: `text`
- SHA256: `59f6608c9e9de2139e34403f6feade665d44ee1751d1558f5b00061d8da10886`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [task-id] | --repo | --milestone | --close-linear | --skip-attachments
description: Convert Linear tasks to GitHub issues with relationship preservation and metadata mapping
---

# Linear Task to Issue

Convert Linear tasks to GitHub issues with comprehensive relationship mapping: **$ARGUMENTS**

## Current Task Context

- Task details: Based on $ARGUMENTS task identifier or selection criteria
- Target repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "No repo context"`
- User mappings: Linear email to GitHub username correspondence
- Attachment handling: Linear attachment access and GitHub upload capabilities

## Task

Execute precise conversion of Linear tasks to GitHub issues:

**Task Target**: Use $ARGUMENTS to specify task identifier, target repository, milestone mapping, or processing preferences

**Conversion Framework**:
1. **Task Analysis** - Fetch complete Linear task data, extract relationships, analyze content structure, identify priorities
2. **Content Transformation** - Build GitHub issue body, map Linear fields, preserve formatting, handle rich content
3. **GitHub Integration** - Create issue with proper structure, apply labels, assign users, set milestones, manage relationships
4. **Attachment Migration** - Download Linear attachments, upload to GitHub, update references, maintain accessibility
5. **Comment Import** - Transfer comments with attribution, preserve timestamps, maintain context, handle mentions
6. **Cross-Reference Setup** - Create bidirectional links, update Linear task, maintain sync database, enable navigation

**Advanced Features**: Rich content conversion, attachment handling, relationship mapping, user mention translation, comprehensive validation.

**Relationship Management**: Preserve parent-child relationships, maintain team context, map project associations, handle dependencies.

**Output**: Successfully created GitHub issue with complete data migration, accurate field mappings, preserved relationships, and comprehensive conversion report.

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
