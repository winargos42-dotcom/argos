---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/milestone-tracker.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\milestone-tracker.md
source_ext: .md
source_sha256: 77b4cfaf47489824153ebf1d36a3c3bc705f02d3cb42f9a998f86ff3a633355c
text_sha256: 724d117c6df02434b86be1b6fe4ce5a4f129acd71e354366394779bf60560e4e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# milestone-tracker.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/milestone-tracker.md`
- Extract: `text`
- SHA256: `77b4cfaf47489824153ebf1d36a3c3bc705f02d3cb42f9a998f86ff3a633355c`

## Content

---
allowed-tools: Bash, Read, Grep, Glob
argument-hint: [time-period] | --sprint | --quarter | --all
description: Track and analyze project milestone progress with predictive analytics
---

# Milestone Tracker

Track and monitor project milestone progress with comprehensive analytics: **$ARGUMENTS**

## Current Project Context

- Project activity: !`git log --oneline --since="30 days ago" | wc -l` commits
- Active branches: !`git branch -r | wc -l` remote branches
- Recent releases: !`git tag -l --sort=-creatordate | head -5`
- Milestone data: @.github/milestones/ or Linear integration

## Task

Generate comprehensive milestone tracking report analyzing project delivery progress:

**Time Period**: Use $ARGUMENTS or default to current sprint/quarter

**Analysis Dimensions**:
1. **Milestone Progress Tracking**
   - Current milestone completion rates
   - Velocity trends and burn-down analysis
   - Critical path identification
   - Dependency mapping and risk assessment

2. **Predictive Analytics**
   - Completion date predictions with confidence intervals
   - Risk-adjusted timeline recommendations
   - Resource allocation optimization
   - Scenario planning (what-if analysis)

3. **Health Indicators**
   - Schedule adherence metrics
   - Team capacity utilization
   - Blocker identification and impact
   - Quality vs delivery balance

**Output**: Interactive milestone dashboard with visual progress indicators, predictive analytics, risk assessments, and actionable recommendations for milestone delivery optimization.

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
