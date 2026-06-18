---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/issue-to-linear-task.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\issue-to-linear-task.md
source_ext: .md
source_sha256: 306cb1aa33696f709b5452db4701e6c597127e0de721826ba5676630e3eb6671
text_sha256: edc7296b5c02b42114b6ee2e1b0996780800ba84953f78c34a36c45c88d74740
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# issue-to-linear-task.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/issue-to-linear-task.md`
- Extract: `text`
- SHA256: `306cb1aa33696f709b5452db4701e6c597127e0de721826ba5676630e3eb6671`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [issue-number] | --team | --project | --close-github | --skip-comments
description: Convert individual GitHub issues to Linear tasks with comprehensive data preservation
---

# Issue to Linear Task

Convert GitHub issues to Linear tasks with comprehensive field mapping: **$ARGUMENTS**

## Current Conversion Context

- Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "No repo context"`
- Issue details: Based on $ARGUMENTS issue number or selection criteria
- Linear teams: Available Linear teams and project assignments
- User mappings: @user-mappings.json or GitHub-Linear user correspondence

## Task

Execute precise conversion of individual GitHub issues to Linear tasks:

**Issue Target**: Use $ARGUMENTS to specify issue number, conversion options, team assignment, or processing preferences

**Conversion Framework**:
1. **Issue Analysis** - Fetch complete issue data, extract metadata, analyze content structure, infer priorities
2. **Data Transformation** - Map fields accurately, convert formats, preserve relationships, enhance descriptions
3. **Linear Integration** - Create task with proper formatting, assign team/project, set priorities, manage labels
4. **Content Migration** - Import comments with attribution, handle attachments, preserve formatting, maintain threading
5. **Reference Management** - Create bidirectional links, update sync database, maintain cross-references, enable navigation
6. **Validation & Confirmation** - Verify conversion accuracy, confirm field mappings, validate relationships, provide preview

**Advanced Features**: Smart priority inference, intelligent user mapping, attachment handling, comment threading, comprehensive validation.

**Data Fidelity**: Preserve original formatting, maintain all metadata, keep comment attribution, ensure relationship integrity.

**Output**: Successfully converted Linear task with complete data preservation, accurate field mappings, bidirectional references, and comprehensive conversion summary.

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
