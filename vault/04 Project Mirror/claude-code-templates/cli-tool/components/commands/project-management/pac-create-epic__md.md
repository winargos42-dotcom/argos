---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/pac-create-epic.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\pac-create-epic.md
source_ext: .md
source_sha256: b29620cd10c5cc5eac2c05f66895176d1a3688bee1671341307f802a556d3a9f
text_sha256: e467fc24a4711671f11ea71c04ddfdd393c48a5511653ec3b263c3595fa0f41d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# pac-create-epic.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/pac-create-epic.md`
- Extract: `text`
- SHA256: `b29620cd10c5cc5eac2c05f66895176d1a3688bee1671341307f802a556d3a9f`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [epic-name] | --name | --description | --owner
description: Create new PAC epic following Product as Code specification
---

# Create PAC Epic

Create a new epic following the Product as Code specification with guided workflow: **$ARGUMENTS**

## PAC Configuration Check

- PAC directory: !`ls -la .pac/ 2>/dev/null || echo "No .pac directory found"`
- PAC config: @.pac/pac.config.yaml (if exists)
- Existing epics: !`ls -la .pac/epics/ 2>/dev/null | head -10`

## Task

Create a new Product as Code epic:

**Arguments**: 
- Epic name (required if not using --name flag)
- --name <name>: Epic name
- --description <desc>: Epic description  
- --owner <owner>: Epic owner
- --scope <scope>: Scope definition

**Epic Creation Process**:
1. Validate PAC configuration exists (suggest `/project:pac-configure` if missing)
2. Generate epic ID from name (format: epic-[kebab-case-name])
3. Create epic YAML file following PAC v0.1.0 specification in `.pac/epics/[epic-id].yaml`
4. Include required metadata: id, name, created timestamp, owner
5. Add spec with description, scope, success criteria, constraints, dependencies
6. Create epic directory structure: `.pac/epics/[epic-id]/`
7. Update PAC index if `.pac/index.yaml` exists
8. Create git branch `pac/[epic-id]` if in git repository

If information is missing, prompt user interactively for epic details.

**Next Steps**: Use `/project:pac-create-ticket --epic [epic-id]` to add tickets to this epic.

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
