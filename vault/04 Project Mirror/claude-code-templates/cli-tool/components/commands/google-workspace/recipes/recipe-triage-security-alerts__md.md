---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-triage-security-alerts.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-triage-security-alerts.md
source_ext: .md
source_sha256: 64c7a50ad88c7da87251a3f27a28f16a8c4d093cbabca8952832ffe2cc33e2a1
text_sha256: e0bab73d7c274e05513986f20f4a5497cdf6c7807448586399e07530ff074eb5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-triage-security-alerts.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-triage-security-alerts.md`
- Extract: `text`
- SHA256: `64c7a50ad88c7da87251a3f27a28f16a8c4d093cbabca8952832ffe2cc33e2a1`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: List and review Google Workspace security alerts from Alert Center.
---

# Triage Security Alerts

Execute Google Workspace workflow: $ARGUMENTS

# Triage Google Workspace Security Alerts

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-alertcenter`

List and review Google Workspace security alerts from Alert Center.

## Steps

1. List active alerts: `gws alertcenter alerts list --format table`
2. Get alert details: `gws alertcenter alerts get --params '{"alertId": "ALERT_ID"}'`
3. Acknowledge an alert: `gws alertcenter alerts undelete --params '{"alertId": "ALERT_ID"}'`

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
**Original Skill**: `recipe-triage-security-alerts`

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
