---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/project-to-linear.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\project-to-linear.md
source_ext: .md
source_sha256: 88983c251062d0dc6e9542c375be2fa2ca6acf62927e1cf7a33f5527f5c8d21b
text_sha256: 7489b998ee10f9cf7804dcee995c84271f9ce8043c1a9fe5bcdce9786cdfdc9e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# project-to-linear.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/project-to-linear.md`
- Extract: `text`
- SHA256: `88983c251062d0dc6e9542c375be2fa2ca6acf62927e1cf7a33f5527f5c8d21b`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [project-description] | --team-id | --create-new | --epic-name
description: Sync project structure and requirements to Linear workspace with comprehensive task breakdown
---

# Project to Linear

Sync project structure and requirements to Linear workspace: **$ARGUMENTS**

## Linear Integration Status

- Linear MCP: Check if Linear MCP server is configured
- Workspace access: !`echo "Test Linear connection if MCP available"`
- Project context: @README.md or project documentation
- Requirements: Based on $ARGUMENTS analysis

## Task

Analyze project requirements and create comprehensive Linear task structure:

**Project Analysis Process**:
1. **Requirement Analysis** - Parse project description and identify major components
2. **Task Breakdown** - Create hierarchical task structure with epics and subtasks
3. **Dependency Mapping** - Identify task dependencies and critical path
4. **Linear Integration** - Create project, epics, and tasks in Linear workspace
5. **Validation** - Review created structure and provide project overview

**Task Organization**:
- Epic-level features and major components
- Parent tasks for feature areas
- Detailed subtasks with acceptance criteria
- Proper labeling (frontend, backend, testing, documentation)
- Priority and effort estimates
- Timeline and dependency relationships

**Output**: Complete Linear project structure with organized task hierarchy, clear descriptions, and actionable items.

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
