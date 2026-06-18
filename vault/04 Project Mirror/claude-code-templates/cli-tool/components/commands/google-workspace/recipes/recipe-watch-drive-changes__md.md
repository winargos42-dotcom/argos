---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-watch-drive-changes.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-watch-drive-changes.md
source_ext: .md
source_sha256: 3ac78a8cffe83731a04d84ffb585a5b806eab9c95a3e28cc1ee8ee2405e95d2b
text_sha256: cbad3f69747bd0caeca763af8e5ed125154bcf0b2964da006d7d46fd2d2ca49d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-watch-drive-changes.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-watch-drive-changes.md`
- Extract: `text`
- SHA256: `3ac78a8cffe83731a04d84ffb585a5b806eab9c95a3e28cc1ee8ee2405e95d2b`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Subscribe to change notifications on a Google Drive file or folder.
---

# Watch Drive Changes

Execute Google Workspace workflow: $ARGUMENTS

# Watch for Drive Changes

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-events`

Subscribe to change notifications on a Google Drive file or folder.

## Steps

1. Create subscription: `gws events subscriptions create --json '{"targetResource": "//drive.googleapis.com/drives/DRIVE_ID", "eventTypes": ["google.workspace.drive.file.v1.updated"], "notificationEndpoint": {"pubsubTopic": "projects/PROJECT/topics/TOPIC"}, "payloadOptions": {"includeResource": true}}'`
2. List active subscriptions: `gws events subscriptions list`
3. Renew before expiry: `gws events +renew --subscription SUBSCRIPTION_ID`

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
**Original Skill**: `recipe-watch-drive-changes`

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
