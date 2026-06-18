---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-batch-reply-to-emails.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-batch-reply-to-emails.md
source_ext: .md
source_sha256: 6ca2d80037a70340e061938d14fd64cce1a7ff7f9a0f7b7a332e2d208b682303
text_sha256: 6742eb52e8fa52406a4b01203c59f3ec1b51db37f579f4247954edd638b05545
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-batch-reply-to-emails.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-batch-reply-to-emails.md`
- Extract: `text`
- SHA256: `6ca2d80037a70340e061938d14fd64cce1a7ff7f9a0f7b7a332e2d208b682303`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Find Gmail messages matching a query and send a standard reply to each one.
---

# Batch Reply To Emails

Execute Google Workspace workflow: $ARGUMENTS

# Batch Reply to Similar Gmail Messages

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-gmail`

Find Gmail messages matching a query and send a standard reply to each one.

## Steps

1. Find messages needing replies: `gws gmail users messages list --params '{"userId": "me", "q": "is:unread from:customers label:support"}' --format table`
2. Read a message: `gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'`
3. Send a reply: `gws gmail +send --to sender@example.com --subject 'Re: Your Request' --body 'Thank you for reaching out. We have received your request and will respond within 24 hours.'`
4. Mark as read: `gws gmail users messages modify --params '{"userId": "me", "id": "MSG_ID"}' --json '{"removeLabelIds": ["UNREAD"]}'`

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
**Original Skill**: `recipe-batch-reply-to-emails`

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
