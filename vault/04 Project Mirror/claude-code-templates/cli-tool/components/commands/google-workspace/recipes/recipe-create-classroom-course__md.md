---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-create-classroom-course.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\recipes\recipe-create-classroom-course.md
source_ext: .md
source_sha256: 8c99990a17fa540b6aba4238ddbd771f1149923dffabfe4069ac7b42e2a1f869
text_sha256: 81f89fcf5bf3485aced0d7cd0da3aeeacd6c7e3495f10324dd83a5b587fbdd04
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# recipe-create-classroom-course.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/recipes/recipe-create-classroom-course.md`
- Extract: `text`
- SHA256: `8c99990a17fa540b6aba4238ddbd771f1149923dffabfe4069ac7b42e2a1f869`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [task-parameters]
description: Create a Google Classroom course and invite students.
---

# Create Classroom Course

Execute Google Workspace workflow: $ARGUMENTS

# Create a Google Classroom Course

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-classroom`

Create a Google Classroom course and invite students.

## Steps

1. Create the course: `gws classroom courses create --json '{"name": "Introduction to CS", "section": "Period 1", "room": "Room 101", "ownerId": "me"}'`
2. Invite a student: `gws classroom invitations create --json '{"courseId": "COURSE_ID", "userId": "student@school.edu", "role": "STUDENT"}'`
3. List enrolled students: `gws classroom courses students list --params '{"courseId": "COURSE_ID"}' --format table`

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
**Original Skill**: `recipe-create-classroom-course`

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
