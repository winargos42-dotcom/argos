---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/team/standup-report.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\team\standup-report.md
source_ext: .md
source_sha256: 268c4e7ec13c2e53fccb7fd54f93f1c07b64acbe91a2789fb11543de47671fd7
text_sha256: 5e0486c54cab5427be250f44a86dc585bbfec59460a5bc48f8d0413ca715d6af
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# standup-report.md

- Source: `claude-code-templates/cli-tool/components/commands/team/standup-report.md`
- Extract: `text`
- SHA256: `268c4e7ec13c2e53fccb7fd54f93f1c07b64acbe91a2789fb11543de47671fd7`

## Content

---
allowed-tools: Read, Bash, Glob, Grep
argument-hint: [time-range] | --yesterday | --last-24h | --since-friday | --custom-range
description: Generate comprehensive daily standup reports with team activity analysis and progress tracking
---

# Standup Report

Generate comprehensive daily standup reports with team activity and progress analysis: **$ARGUMENTS**

## Current Standup Context

- Linear connection: Linear MCP server status and task synchronization
- Time range: !`date -d 'yesterday' '+%Y-%m-%d'` to !`date '+%Y-%m-%d'` analysis period
- Team members: !`git log --format='%ae' --since='1 day ago' | sort -u | wc -l` active contributors
- Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "No repo context"`

## Task

Generate comprehensive standup report with team activity analysis and progress insights:

**Time Range**: Use $ARGUMENTS to specify yesterday, last 24 hours, since Friday, or custom date range for analysis

**Standup Report Framework**:
1. **Git Activity Analysis** - Extract commit activity, analyze code changes, identify contributors, assess impact scope
2. **Linear Task Progress** - Query task updates, analyze completion status, track sprint progress, identify blockers
3. **Pull Request Activity** - Review PR submissions, analyze review activity, track merge status, assess collaboration patterns
4. **Team Collaboration** - Analyze pair programming, code review participation, knowledge sharing, mentorship activities
5. **Progress Tracking** - Calculate velocity metrics, assess goal completion, identify trends, predict sprint outcomes
6. **Blockers & Impediments** - Identify stuck tasks, analyze delay patterns, assess resource needs, recommend solutions

**Advanced Features**: Automated activity categorization, progress visualization, trend analysis, predictive insights, team health scoring.

**Report Quality**: Actionable insights, clear progress indicators, obstacle identification, team coordination support, meeting efficiency optimization.

**Output**: Comprehensive standup report with team activity summary, progress metrics, blocker identification, and actionable next steps.

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
