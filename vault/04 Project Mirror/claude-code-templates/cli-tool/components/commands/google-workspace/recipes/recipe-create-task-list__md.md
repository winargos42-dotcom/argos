---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-create-task-list.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-create-task-list.md
source_ext: .md
source_sha256: feb9db73fc2c4db25088f1e93e1058aa1337804ff751142fd46682068bd5ae81
text_sha256: 94cac0a6c3d4f0ae00aa4b742a84e21a399be75888acaa7087a0e007c23a2998
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-create-task-list.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-create-task-list.md`
- Extract: `text`
- SHA256: `feb9db73fc2c4db25088f1e93e1058aa1337804ff751142fd46682068bd5ae81`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Set up a new Google Tasks list with initial tasks.
---

# Create Task List

Execute Google Workspace workflow: $ARGUMENTS

# Create a Task List and Add Tasks

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-tasks`

Set up a new Google Tasks list with initial tasks.

## Steps

1. Create task list: `gws tasks tasklists insert --json '{"title": "Q2 Goals"}'`
2. Add a task: `gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{"title": "Review Q1 metrics", "notes": "Pull data from analytics dashboard", "due": "2024-04-01T00:00:00Z"}'`
3. Add another task: `gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{"title": "Draft Q2 OKRs"}'`
4. List tasks: `gws tasks tasks list --params '{"tasklist": "TASKLIST_ID"}' --format table`

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
**Original Skill**: `recipe-create-task-list`

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
