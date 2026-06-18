---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-create-events-from-sheet.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-create-events-from-sheet.md
source_ext: .md
source_sha256: abf72f6b07e6aa9090a9300d6800667cdf3c19cd85387a366530be71ba19f8f2
text_sha256: e785f48369531c45702f25c16e37e890c8999259af91eac8e7efd744cfab8a67
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-create-events-from-sheet.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-create-events-from-sheet.md`
- Extract: `text`
- SHA256: `abf72f6b07e6aa9090a9300d6800667cdf3c19cd85387a366530be71ba19f8f2`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Read event data from a Google Sheets spreadsheet and create Google Calendar entries for each row.
---

# Create Events From Sheet

Execute Google Workspace workflow: $ARGUMENTS

# Create Google Calendar Events from a Sheet

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-sheets`, `gws-calendar`

Read event data from a Google Sheets spreadsheet and create Google Calendar entries for each row.

## Steps

1. Read event data: `gws sheets +read --spreadsheet-id SHEET_ID --range 'Events!A2:D'`
2. For each row, create a calendar event: `gws calendar +insert --summary 'Team Standup' --start '2025-01-20T09:00' --duration 30 --attendees alice@company.com,bob@company.com`

## Task

Execute this workflow with the following parameters: $ARGUMENTS

1. **Prerequisites Check**
   - Verify `gws` CLI is installed: `gws --version`
   - Confirm authentication: `gws auth status`
   - Load required GWS skills (check PREREQUISITE section above)

2. **Parameter Preparation**
   - Parse task parameters from $ARGUMENTS
   - Validate required inputs
   - Prepare JSON payloads and flags

3. **Execute Workflow Steps**
   - Follow the steps outlined above
   - Replace placeholder IDs with actual values
   - Handle errors and retries
   - Log progress and results

4. **Verify Results**
   - Confirm each step completed successfully
   - Verify changes in Google Workspace
   - Report final status and any issues

## Tips

- Use `--dry-run` flag when available to preview changes
- Always inspect API schemas before calling: `gws schema <service>.<resource>.<method>`
- Check command help for all flags: `gws <service> <resource> <method> --help`

---

**License**: Apache License 2.0
**Source**: [Google Workspace CLI](https://github.com/googleworkspace/cli)
**Original Skill**: `recipe-create-events-from-sheet`

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
