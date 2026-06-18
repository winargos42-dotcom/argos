---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-search-and-export-emails.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-search-and-export-emails.md
source_ext: .md
source_sha256: 7f20e2bc6ab2901f8b5a0daeec2894012523d48c9a232027aa07f7833ff35444
text_sha256: bdc742e9b404ab44f9ac70dd948bfbedd09ac002129c44863088e19627748f9d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-search-and-export-emails.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-search-and-export-emails.md`
- Extract: `text`
- SHA256: `7f20e2bc6ab2901f8b5a0daeec2894012523d48c9a232027aa07f7833ff35444`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Find Gmail messages matching a query and export them for review.
---

# Search And Export Emails

Execute Google Workspace workflow: $ARGUMENTS

# Search and Export Emails

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-gmail`

Find Gmail messages matching a query and export them for review.

## Steps

1. Search for emails: `gws gmail users messages list --params '{"userId": "me", "q": "from:client@example.com after:2024/01/01"}'`
2. Get full message: `gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'`
3. Export results: `gws gmail users messages list --params '{"userId": "me", "q": "label:project-x"}' --format json > project-emails.json`

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
**Original Skill**: `recipe-search-and-export-emails`

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
