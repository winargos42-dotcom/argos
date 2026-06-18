---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-cancel-and-notify.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-cancel-and-notify.md
source_ext: .md
source_sha256: b3a3b9ad9573fc8d3573161012e7afb416dfb6dc6533c4dcc0bd5c64d028c984
text_sha256: a78d992b8f63d6de46edfceb19efe88654dc4bf368ccdd562775416c905efb78
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-cancel-and-notify.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-cancel-and-notify.md`
- Extract: `text`
- SHA256: `b3a3b9ad9573fc8d3573161012e7afb416dfb6dc6533c4dcc0bd5c64d028c984`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Delete a Google Calendar event and send a cancellation email via Gmail.
---

# Cancel And Notify

Execute Google Workspace workflow: $ARGUMENTS

# Cancel Meeting and Notify Attendees

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-calendar`, `gws-gmail`

Delete a Google Calendar event and send a cancellation email via Gmail.

> [!CAUTION]
> Deleting with sendUpdates sends cancellation emails to all attendees.

## Steps

1. Find the meeting: `gws calendar +agenda --format json` and locate the event ID
2. Delete the event: `gws calendar events delete --params '{"calendarId": "primary", "eventId": "EVENT_ID", "sendUpdates": "all"}'`
3. Send follow-up: `gws gmail +send --to attendees --subject 'Meeting Cancelled: [Title]' --body 'Apologies, this meeting has been cancelled.'`

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
**Original Skill**: `recipe-cancel-and-notify`

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
