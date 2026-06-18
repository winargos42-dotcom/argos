---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/task-from-pr.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\task-from-pr.md
source_ext: .md
source_sha256: 0f1da88b133578403ec3a7d02305adb196c38ea12080a73b28720489f465b42d
text_sha256: 71b8d941d1bac8dbb7b42bf0aafb066158d9456983326fad1a92b5a49058e754
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# task-from-pr.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/task-from-pr.md`
- Extract: `text`
- SHA256: `0f1da88b133578403ec3a7d02305adb196c38ea12080a73b28720489f465b42d`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [pr-number] | --team | --estimate | --batch-process | --auto-create
description: Create Linear tasks from GitHub pull requests with intelligent content extraction and task sizing
---

# Task from PR

Create Linear tasks from GitHub pull requests with intelligent analysis: **$ARGUMENTS**

## Current PR Environment

- Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "No repo context"`
- PR status: Based on $ARGUMENTS PR number or batch processing criteria
- Linear teams: Available teams for task assignment
- User mappings: GitHub username to Linear user correspondence

## Task

Generate Linear tasks from GitHub pull requests with comprehensive content analysis:

**PR Source**: Use $ARGUMENTS to specify PR number, team assignment, size estimation, or batch processing mode

**Task Generation Framework**:
1. **PR Analysis** - Extract comprehensive PR data, parse description structure, identify key components, analyze changes
2. **Content Extraction** - Parse structured sections, extract checklists, identify technical details, capture requirements
3. **Intelligent Sizing** - Estimate task complexity from code changes, file count, review comments, testing requirements
4. **Task Construction** - Build Linear task with proper formatting, preserve PR context, maintain references, structure content
5. **Team Assignment** - Map to appropriate Linear team, assign based on code areas, set priorities from labels
6. **Validation & Creation** - Check for duplicates, validate task structure, create in Linear, establish bidirectional links

**Advanced Features**: Smart content parsing, automated size estimation, intelligent team mapping, comprehensive validation, batch processing.

**Quality Assurance**: Duplicate detection, content validation, proper formatting, relationship maintenance, comprehensive error handling.

**Output**: Successfully created Linear tasks with comprehensive PR context, accurate sizing estimates, proper team assignments, and complete bidirectional linking.

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
