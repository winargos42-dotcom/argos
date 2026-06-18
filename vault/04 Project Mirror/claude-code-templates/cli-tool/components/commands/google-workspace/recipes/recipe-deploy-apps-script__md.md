---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-deploy-apps-script.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-deploy-apps-script.md
source_ext: .md
source_sha256: d3fbfce448994b33b75a2ef0e030007c28e464ff01b5c19c478ebbb40408baac
text_sha256: 8631e87e521908e9a4f56ecd3f516d882748734fd2a706024cd551a34729c82d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-deploy-apps-script.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-deploy-apps-script.md`
- Extract: `text`
- SHA256: `d3fbfce448994b33b75a2ef0e030007c28e464ff01b5c19c478ebbb40408baac`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Push local files to a Google Apps Script project.
---

# Deploy Apps Script

Execute Google Workspace workflow: $ARGUMENTS

# Deploy an Apps Script Project

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-apps-script`

Push local files to a Google Apps Script project.

## Steps

1. List existing projects: `gws apps-script projects list --format table`
2. Get project content: `gws apps-script projects getContent --params '{"scriptId": "SCRIPT_ID"}'`
3. Update content: `gws apps-script projects updateContent --params '{"scriptId": "SCRIPT_ID"}' --json '{"files": [{"name": "Code", "type": "SERVER_JS", "source": "function main() { ... }"}]}'`
4. Create a new version: `gws apps-script projects versions create --params '{"scriptId": "SCRIPT_ID"}' --json '{"description": "v2 release"}'`

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
**Original Skill**: `recipe-deploy-apps-script`

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
