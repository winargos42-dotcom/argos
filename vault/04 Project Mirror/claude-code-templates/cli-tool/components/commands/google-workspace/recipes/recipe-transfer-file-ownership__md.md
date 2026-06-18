---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-transfer-file-ownership.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-transfer-file-ownership.md
source_ext: .md
source_sha256: d7f9dd190b9d799adb370028bae775061796826fb4285c9bfd6cee0283af63e7
text_sha256: 3ded8ced0f9d7cada3be482ee7291f89b29dcb449d840e076453c9cfe1d5eeb3
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-transfer-file-ownership.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-transfer-file-ownership.md`
- Extract: `text`
- SHA256: `d7f9dd190b9d799adb370028bae775061796826fb4285c9bfd6cee0283af63e7`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Transfer ownership of Google Drive files from one user to another.
---

# Transfer File Ownership

Execute Google Workspace workflow: $ARGUMENTS

# Transfer File Ownership

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-drive`

Transfer ownership of Google Drive files from one user to another.

> [!CAUTION]
> Transferring ownership is irreversible without the new owner's cooperation.

## Steps

1. List files owned by the user: `gws drive files list --params '{"q": "'\''user@company.com'\'' in owners"}'`
2. Transfer ownership: `gws drive permissions create --params '{"fileId": "FILE_ID", "transferOwnership": true}' --json '{"role": "owner", "type": "user", "emailAddress": "newowner@company.com"}'`

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
**Original Skill**: `recipe-transfer-file-ownership`

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
