---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/sync-issues-to-linear.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\sync-issues-to-linear.md
source_ext: .md
source_sha256: 8f701b90cca145a7b75ad8728be3eac4c9d30b4d209bdc9280276c5b6eb9926c
text_sha256: 232063ad03acf4061e44dcc6d3bf096e95f37dbcbc809c80b9d84830bcf907a1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# sync-issues-to-linear.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/sync-issues-to-linear.md`
- Extract: `text`
- SHA256: `8f701b90cca145a7b75ad8728be3eac4c9d30b4d209bdc9280276c5b6eb9926c`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [sync-scope] | --state | --label | --assignee | --milestone
description: Sync GitHub issues to Linear workspace with comprehensive field mapping and rate limit management
---

# Sync Issues to Linear

Sync GitHub issues to Linear workspace with intelligent field mapping: **$ARGUMENTS**

## Current Repository Context

- Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "No repo context"`
- Issue count: !`gh issue list --state all --limit 1 --json number | jq length 2>/dev/null || echo "Check manually"`
- Linear teams: Available Linear teams and project assignments
- Rate limits: !`gh api rate_limit -q '.rate | "GitHub: \(.remaining)/\(.limit)"' 2>/dev/null`

## Task

Execute comprehensive synchronization of GitHub issues to Linear workspace:

**Sync Scope**: Use $ARGUMENTS to filter by issue state, labels, assignees, milestones, or specific issue sets

**Synchronization Framework**:
1. **Issue Discovery** - Fetch GitHub issues with comprehensive metadata, apply filters, validate requirements
2. **Field Mapping** - Transform GitHub fields to Linear format, map priorities, convert labels, handle assignees
3. **Data Validation** - Check required fields, validate user mappings, ensure data integrity, prevent duplicates
4. **Linear Integration** - Create tasks with proper formatting, apply team assignments, set projects, manage relationships
5. **Rate Limit Management** - Implement exponential backoff, batch operations, monitor API limits, optimize requests
6. **Progress Tracking** - Provide real-time updates, handle errors gracefully, maintain sync state, generate reports

**Advanced Features**: Smart priority inference, intelligent user mapping, incremental sync capabilities, comprehensive error recovery.

**Data Integrity**: Preserve formatting, maintain metadata, create bidirectional references, ensure audit trails.

**Output**: Complete synchronization results with success metrics, error reports, mapping summaries, and comprehensive sync analytics.

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
