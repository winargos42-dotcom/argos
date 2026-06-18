---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/bulk-import-issues.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\bulk-import-issues.md
source_ext: .md
source_sha256: 2e56adbf1f9f7b596e5f1eb5ab278bc3154bc64b42aaa2ea65aaee2ea053d838
text_sha256: 1e2a2acd0a2900b46c9259ed9f5a3caf1dfdff715b1173202d3d7a83241a2d4c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# bulk-import-issues.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/bulk-import-issues.md`
- Extract: `text`
- SHA256: `2e56adbf1f9f7b596e5f1eb5ab278bc3154bc64b42aaa2ea65aaee2ea053d838`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [import-scope] | --state | --label | --milestone | --batch-size
description: Bulk import GitHub issues to Linear with comprehensive progress tracking and error handling
---

# Bulk Import Issues

Bulk import GitHub issues to Linear with advanced processing capabilities: **$ARGUMENTS**

## Current Import Context

- Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "No repo context"`
- Issue count: !`gh api repos/{owner}/{repo}/issues?state=all --paginate | jq length 2>/dev/null || echo "Check manually"`
- Linear teams: Check available Linear teams and projects for import mapping
- Rate limits: !`gh api rate_limit -q '.rate | "GitHub: \(.remaining)/\(.limit)"' 2>/dev/null || echo "Check GitHub rate limit"`

## Task

Execute efficient bulk import of GitHub issues to Linear with comprehensive management:

**Import Scope**: Use $ARGUMENTS to filter by state, labels, milestones, or configure batch processing parameters

**Import Pipeline**:
1. **Pre-Import Analysis** - Issue discovery, duplicate detection, import estimation, resource planning
2. **Batch Configuration** - Dynamic batch sizing, rate limit management, progress tracking, error handling
3. **Data Transformation** - Field mapping, priority inference, user mapping, content enhancement
4. **Import Execution** - Parallel processing, retry logic, transaction management, progress reporting
5. **Error Recovery** - Failed item handling, retry mechanisms, partial import recovery, validation
6. **Post-Import Actions** - Cross-reference creation, GitHub updates, mapping files, notifications

**Advanced Features**: Dynamic batch adjustment, intelligent rate limiting, duplicate detection, comprehensive error recovery, progress visualization.

**Quality Assurance**: Pre-import validation, post-import verification, data integrity checks, comprehensive audit trails.

**Output**: Complete import results with success metrics, failed item reports, mapping documentation, and performance analytics for large-scale issue migration.

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
