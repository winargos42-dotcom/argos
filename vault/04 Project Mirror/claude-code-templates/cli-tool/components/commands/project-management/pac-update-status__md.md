---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/project-management/pac-update-status.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\project-management\pac-update-status.md
source_ext: .md
source_sha256: 9e19db85bf5153866263e9d4927d5f78baaa48235a84448e6ecca6edebeaa000
text_sha256: 5e04668d1f38c54ed8a28e4db6c3d17e677c8715e246d721aa923f32eb3f51ea
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# pac-update-status.md

- Source: `claude-code-templates/cli-tool/components/commands/project-management/pac-update-status.md`
- Extract: `text`
- SHA256: `9e19db85bf5153866263e9d4927d5f78baaa48235a84448e6ecca6edebeaa000`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [ticket-id] | --status | --assignee | --comment
description: Update PAC ticket status and track progress in Product as Code workflow
---

# Update PAC Ticket Status

Update ticket status and track progress in Product as Code workflow: **$ARGUMENTS**

## PAC Environment Check

- PAC directory: !`ls -la .pac/ 2>/dev/null || echo "No .pac directory found"`
- Active tickets: !`find .pac/tickets/ -name "*.yaml" 2>/dev/null | wc -l`
- Recent updates: !`find .pac/tickets/ -name "*.yaml" -mtime -7 2>/dev/null | wc -l`

## Task

Update PAC ticket status and track development progress:

**Arguments**:
- --ticket <ticket-id>: Ticket ID to update (or select interactively)
- --status <status>: New status (backlog/in-progress/review/blocked/done/cancelled)
- --assignee <assignee>: Update assignee
- --comment <comment>: Add progress comment
- --epic <epic-id>: Filter tickets by epic for selection

**Status Update Process**:
1. Validate PAC environment and locate ticket
2. Load current ticket state and validate status transitions
3. Update ticket YAML with new status and timestamp
4. Handle status-specific actions (branch creation, PR suggestions)
5. Update parent epic with ticket progress
6. Generate status update summary with next actions

**Valid Status Transitions**: backlog→in-progress→review→done, with blocked/cancelled as intermediate states.

**Git Integration**: Suggests branch creation for in-progress, PR creation for review, and merge for done status.

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
