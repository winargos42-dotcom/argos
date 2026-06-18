---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/pac-configure.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\pac-configure.md
source_ext: .md
source_sha256: fe17d75467396d31af80529e5bf2d49cd54ba60591eca464d4fb3abcda79c069
text_sha256: f1f0fe48d29c7306a8d92526ae50c22fcfdf233137b95159404045371a121342
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# pac-configure.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/pac-configure.md`
- Extract: `text`
- SHA256: `fe17d75467396d31af80529e5bf2d49cd54ba60591eca464d4fb3abcda79c069`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [project-name] | --minimal | --epic-name | --owner
description: Initialize Product as Code (PAC) project structure with templates and configuration
---

# Configure PAC Project

Initialize Product as Code (PAC) project structure: **$ARGUMENTS**

## Current Project State

- Git status: !`git status --porcelain | wc -l` uncommitted changes
- PAC structure: !`ls -la .pac/ 2>/dev/null | head -5 || echo "No PAC directory"`
- Existing epics: !`find .pac/epics/ -name "*.yaml" 2>/dev/null | wc -l`

## Task

Configure and initialize PAC project structure for version-controlled product management:

**Setup Process**:
1. **Project Analysis** - Validate git repository and analyze existing PAC structure
2. **Directory Creation** - Create `.pac/` structure with epics, tickets, and templates
3. **Configuration Files** - Generate `pac.config.yaml` with project metadata and defaults
4. **Template Creation** - Create epic and ticket templates following PAC v0.1.0 specification
5. **Initial Content** - Create first epic and ticket based on user input
6. **Integration Setup** - Configure git hooks and validation scripts

**Arguments**: Use --minimal for basic structure, --epic-name for initial epic, --owner for product owner.

**Next Steps**: Use `/project:pac-create-epic` and `/project:pac-create-ticket` to manage product development.

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
