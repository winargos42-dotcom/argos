---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-batch-rename-files.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-batch-rename-files.md
source_ext: .md
source_sha256: bc9d351bcfd8dcd80a6f29368600ebf279a9ad0db37eedb8593c1481f0a270c6
text_sha256: bdfc657e9ff8f259e4c19b3264fbd67415b55db71f54846dbadc866678301c1e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-batch-rename-files.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-batch-rename-files.md`
- Extract: `text`
- SHA256: `bc9d351bcfd8dcd80a6f29368600ebf279a9ad0db37eedb8593c1481f0a270c6`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Rename multiple Google Drive files matching a pattern to follow a consistent naming convention.
---

# Batch Rename Files

Execute Google Workspace workflow: $ARGUMENTS

# Batch Rename Google Drive Files

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-drive`

Rename multiple Google Drive files matching a pattern to follow a consistent naming convention.

## Steps

1. Find files to rename: `gws drive files list --params '{"q": "name contains '\''Report'\''"}' --format table`
2. Rename a file: `gws drive files update --params '{"fileId": "FILE_ID"}' --json '{"name": "2025-Q1 Report - Final"}'`
3. Verify the rename: `gws drive files get --params '{"fileId": "FILE_ID", "fields": "name"}'`

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
**Original Skill**: `recipe-batch-rename-files`

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
