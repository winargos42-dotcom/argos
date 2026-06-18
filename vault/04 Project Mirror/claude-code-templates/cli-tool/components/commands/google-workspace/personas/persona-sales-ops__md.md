---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/personas/persona-sales-ops.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\personas\persona-sales-ops.md
source_ext: .md
source_sha256: a324365401004ed0d5998e04c64a14c2c0e858571c5e97b9f077a67cbaa3f131
text_sha256: 31b9e793e778e67aa52a4ecef15d5810c587af0ab2a194b7b94a549198318bc7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# persona-sales-ops.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/personas/persona-sales-ops.md`
- Extract: `text`
- SHA256: `a324365401004ed0d5998e04c64a14c2c0e858571c5e97b9f077a67cbaa3f131`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-description]
description: Manage sales workflows — track deals, schedule calls, client comms.
---

# Sales Ops Persona

Operate as Sales Ops using Google Workspace tools: $ARGUMENTS

# Sales Operations

> **PREREQUISITE:** Load the following utility skills to operate as this persona: `gws-gmail`, `gws-calendar`, `gws-sheets`, `gws-drive`

Manage sales workflows — track deals, schedule calls, client comms.

## Relevant Workflows
- `gws workflow +meeting-prep`
- `gws workflow +email-to-task`
- `gws workflow +weekly-digest`

## Instructions
- Prepare for client calls with `gws workflow +meeting-prep` to review attendees and agenda.
- Log deal updates in a tracking spreadsheet with `gws sheets +append`.
- Convert follow-up emails into tasks with `gws workflow +email-to-task`.
- Share proposals by uploading to Drive with `gws drive +upload`.
- Get a weekly sales pipeline summary with `gws workflow +weekly-digest`.

## Tips
- Use `gws gmail +triage --query 'from:client-domain.com'` to filter client emails.
- Schedule follow-up calls immediately after meetings to maintain momentum.
- Keep all client-facing documents in a dedicated shared Drive folder.

## Task

Execute the following task as Sales Ops: $ARGUMENTS

1. **Load Required Skills**
   - Ensure all prerequisite GWS skills are available
   - Verify `gws` CLI is installed and authenticated
   - Review persona-specific workflows

2. **Analyze Task**
   - Understand the task requirements
   - Identify which Google Workspace services are needed
   - Plan the workflow steps

3. **Execute Workflow**
   - Use appropriate `gws` commands for each step
   - Follow persona-specific best practices
   - Document actions taken

4. **Review and Verify**
   - Confirm task completion
   - Verify results in Google Workspace
   - Report any issues or blockers

---

**License**: Apache License 2.0
**Source**: [Google Workspace CLI](https://github.com/googleworkspace/cli)
**Original Skill**: `persona-sales-ops`

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
