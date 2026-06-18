---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/team/issue-triage.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\team\issue-triage.md
source_ext: .md
source_sha256: f8f29b7bf28a3fe71fa8e58688371f849c9450504073f0f05a466e3fa12595b1
text_sha256: ecb2b1b585270dfcb595bd01cfcd401ea5be2c1dbd768804cb7bff48a9b0a07e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# issue-triage.md

- Source: `claude-code-templates/cli-tool/components/commands/team/issue-triage.md`
- Extract: `text`
- SHA256: `f8f29b7bf28a3fe71fa8e58688371f849c9450504073f0f05a466e3fa12595b1`

## Content

---
allowed-tools: Read, Write, Bash
argument-hint: [scope] | --github-issues | --linear-tasks | --priority-analysis | --team-assignment
description: Intelligent issue triage with automatic categorization, prioritization, and team assignment
---

# Issue Triage

Intelligently triage and prioritize issues with automated routing and team assignment: **$ARGUMENTS**

## Current Triage Context

- Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "No repo context"`
- Open issues: !`gh issue list --state open --limit 1 --json number | jq length 2>/dev/null || echo "Check manually"`
- Linear teams: Available Linear teams and project assignments for routing
- Triage backlog: Current volume and age of untriaged issues

## Task

Execute intelligent issue analysis with automated triage and priority assignment:

**Triage Scope**: Use $ARGUMENTS to focus on GitHub issues, Linear tasks, priority analysis, or team assignment optimization

**Triage Framework**:
1. **Issue Analysis** - Extract issue metadata, analyze content patterns, assess severity indicators, evaluate impact scope
2. **Category Classification** - Identify issue type (bug, feature, documentation), assess complexity level, determine urgency factors
3. **Priority Assessment** - Calculate priority score using severity, impact, effort, and business value metrics
4. **Team Routing** - Match issue skills to team expertise, balance workload distribution, consider current sprint capacity
5. **Label Management** - Apply consistent labeling scheme, maintain taxonomy standards, enable filtering and reporting
6. **SLA Assignment** - Set response time expectations, establish resolution targets, track performance metrics

**Advanced Features**: Automated severity detection, intelligent team matching, workload balancing, SLA monitoring, escalation workflows.

**Quality Assurance**: Consistency validation, triage accuracy tracking, team satisfaction monitoring, process optimization feedback.

**Output**: Complete issue triage with priority assignments, team routing recommendations, SLA targets, and process improvement insights.

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
