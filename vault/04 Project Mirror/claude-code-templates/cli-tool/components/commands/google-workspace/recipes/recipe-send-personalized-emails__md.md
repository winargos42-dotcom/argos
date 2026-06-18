---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-send-personalized-emails.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-send-personalized-emails.md
source_ext: .md
source_sha256: 17578e3d59edb90bf7224eec190e08974cd013423ebc84e9a56bc792ec487aa9
text_sha256: 789391a88bfff455ca53d68807647321160afa434ba56fd0478d5e7c456d0d70
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-send-personalized-emails.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-send-personalized-emails.md`
- Extract: `text`
- SHA256: `17578e3d59edb90bf7224eec190e08974cd013423ebc84e9a56bc792ec487aa9`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Read recipient data from Google Sheets and send personalized Gmail messages to each row.
---

# Send Personalized Emails

Execute Google Workspace workflow: $ARGUMENTS

# Send Personalized Emails from a Sheet

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-sheets`, `gws-gmail`

Read recipient data from Google Sheets and send personalized Gmail messages to each row.

## Steps

1. Read recipient list: `gws sheets +read --spreadsheet-id SHEET_ID --range 'Contacts!A2:C'`
2. For each row, send a personalized email: `gws gmail +send --to recipient@example.com --subject 'Hello, Name' --body 'Hi Name, your report is ready.'`

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
**Original Skill**: `recipe-send-personalized-emails`

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
