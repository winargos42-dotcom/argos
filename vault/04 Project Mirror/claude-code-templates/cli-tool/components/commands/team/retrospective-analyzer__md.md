---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/team/retrospective-analyzer.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\team\retrospective-analyzer.md
source_ext: .md
source_sha256: d70ce7fcc9a57bf80d1e8329859be38ed409540b9f4edcd26960ebd24ef0fcea
text_sha256: f7052385bfa8526f0304715debeb18c90913c421b05db9ee174e9dee21a66c9e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# retrospective-analyzer.md

- Source: `claude-code-templates/cli-tool/components/commands/team/retrospective-analyzer.md`
- Extract: `text`
- SHA256: `d70ce7fcc9a57bf80d1e8329859be38ed409540b9f4edcd26960ebd24ef0fcea`

## Content

---
allowed-tools: Read, Write, Bash, Glob
argument-hint: [sprint-identifier] | --metrics | --insights | --action-items | --trends
description: Analyze team retrospectives with quantitative metrics and actionable insights generation
---

# Retrospective Analyzer

Analyze team retrospectives with comprehensive metrics and actionable improvement insights: **$ARGUMENTS**

## Current Retrospective Context

- Sprint period: !`git log --oneline --since='2 weeks ago' | wc -l` commits in recent sprint
- Team activity: Analysis of recent collaboration patterns and productivity metrics
- Linear sprint: Current sprint data and completion metrics from Linear MCP
- Previous retrospectives: Historical retrospective data and improvement tracking

## Task

Execute comprehensive retrospective analysis with quantitative insights and improvement recommendations:

**Analysis Focus**: Use $ARGUMENTS to specify sprint identifier, quantitative metrics, insight generation, action item tracking, or trend analysis

**Retrospective Analysis Framework**:
1. **Sprint Performance Analysis** - Analyze velocity trends, completion rates, cycle time metrics, quality indicators
2. **Team Collaboration Assessment** - Evaluate communication patterns, code review effectiveness, knowledge sharing, pair programming impact
3. **Process Effectiveness** - Assess meeting efficiency, planning accuracy, impediment resolution, workflow optimization
4. **Quality Metrics** - Analyze bug rates, technical debt accumulation, code review quality, testing effectiveness
5. **Individual Contribution** - Evaluate workload distribution, skill development, mentorship activities, cross-training progress
6. **Actionable Insights Generation** - Identify improvement opportunities, prioritize action items, track progress, measure impact

**Advanced Features**: Trend analysis across multiple sprints, predictive performance modeling, team satisfaction correlation, continuous improvement tracking.

**Insight Quality**: Data-driven recommendations, quantified improvement potential, implementation feasibility, success measurement criteria.

**Output**: Comprehensive retrospective analysis with quantitative metrics, actionable insights, prioritized improvements, and progress tracking framework.

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
