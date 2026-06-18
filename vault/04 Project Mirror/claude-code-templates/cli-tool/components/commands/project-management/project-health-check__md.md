---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/project-health-check.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\project-health-check.md
source_ext: .md
source_sha256: 416067e36d3c41782673caaec7f97729c4e42065cfb118f704ff90cf940e0d3b
text_sha256: cc9c9e39c52f976394d0cbbc873b2cba7bb71997c79f89f398b1326a710f4d04
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# project-health-check.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/project-health-check.md`
- Extract: `text`
- SHA256: `416067e36d3c41782673caaec7f97729c4e42065cfb118f704ff90cf940e0d3b`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [evaluation-period] | --30-days | --sprint | --quarter
description: Analyze overall project health and generate comprehensive metrics report
---

# Project Health Check

Analyze overall project health and metrics: **$ARGUMENTS**

## Current Project State

- Git activity: !`git log --oneline --since="30 days ago" | wc -l`
- Contributors: !`git shortlog -sn --since="30 days ago" | head -5`
- Branch status: !`git branch -r | wc -l` remote branches
- Code changes: !`git diff --stat HEAD~30 2>/dev/null || echo "Not enough history"`
- Dependencies: @package.json or @requirements.txt or @Cargo.toml (if exists)

## Task

Generate a comprehensive project health report analyzing:

**Evaluation Period**: Use $ARGUMENTS or default to last 30 days

**Health Dimensions**:
1. **Code Quality Metrics**
   - Test coverage and trends
   - Code complexity analysis
   - Security vulnerabilities (run npm audit or equivalent)
   - Technical debt indicators

2. **Delivery Performance**
   - Sprint velocity trends (if task management tools available)
   - Cycle time analysis
   - Bug vs feature ratio
   - On-time delivery metrics

3. **Team Health Indicators**
   - PR review turnaround time
   - Commit frequency distribution
   - Work distribution balance
   - Knowledge concentration risk

4. **Dependency Health**
   - Outdated packages assessment
   - Security audit results
   - License compliance check
   - External service dependencies

**Health Report Format**:
- Overall health score (0-100) with color-coded status
- Executive summary with key findings
- Detailed metrics tables with current vs target values
- Trend analysis and risk assessment
- Actionable recommendations prioritized by impact

**Output**: Generate markdown report with charts, metrics tables, and specific action items for improving project health.

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
