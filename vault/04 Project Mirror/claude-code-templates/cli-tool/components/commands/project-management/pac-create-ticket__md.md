---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/pac-create-ticket.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\pac-create-ticket.md
source_ext: .md
source_sha256: 60423cdf1e829a49216956123d92ab217ef797798c9a0d41487701eb0341892a
text_sha256: 96c41e9205a1cd6216095effc6634429cd0b1cafaab2743b61d20d0f95cf385a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# pac-create-ticket.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/pac-create-ticket.md`
- Extract: `text`
- SHA256: `60423cdf1e829a49216956123d92ab217ef797798c9a0d41487701eb0341892a`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [ticket-name] | --epic | --type | --assignee | --priority
description: Create new PAC ticket within an epic following Product as Code specification
---

# Create PAC Ticket

Create a new ticket within an epic following Product as Code specification: **$ARGUMENTS**

## PAC Configuration Check

- PAC directory: !`ls -la .pac/ 2>/dev/null || echo "No .pac directory found"`
- PAC config: @.pac/pac.config.yaml (if exists)
- Available epics: !`ls -la .pac/epics/ 2>/dev/null | head -10`

## Task

Create a new Product as Code ticket within an existing epic:

**Arguments**:
- Ticket name (required if not using --name flag)
- --epic <epic-id>: Parent epic ID (required)
- --type <type>: Ticket type (feature/bug/task/spike)
- --assignee <assignee>: Assigned developer
- --priority <priority>: Priority level
- --create-branch: Automatically create git branch

**Ticket Creation Process**:
1. Validate PAC configuration exists (suggest `/project:pac-configure` if missing)
2. Select or validate parent epic
3. Generate unique ticket ID and sequence number
4. Create ticket YAML file following PAC v0.1.0 specification in `.pac/tickets/[ticket-id].yaml`
5. Include required metadata: id, name, epic, created timestamp, assignee
6. Add spec with description, type, status, priority, acceptance criteria, tasks
7. Link ticket to parent epic
8. Create git branch if requested

If information is missing, prompt user interactively for ticket details.

**Next Steps**: Use `/project:pac-update-status` to track ticket progress.

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
