---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/automation/act.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\automation\act.md
source_ext: .md
source_sha256: d6d7e6b187732207683e4e8dc045f13a226e03c00e584ba4a07a886d1d0a1126
text_sha256: 15e66bc165a2d5b7bd0b65efa022f412aa893998970f319127e97645eee2695c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# act.md

- Source: `claude-code-templates/cli-tool/components/commands/automation/act.md`
- Extract: `text`
- SHA256: `d6d7e6b187732207683e4e8dc045f13a226e03c00e584ba4a07a886d1d0a1126`

## Content

---
allowed-tools: Read, Edit, Bash
argument-hint: [workflow-name]
description: Execute GitHub Actions locally using act
---

# Act - GitHub Actions Local Execution

Execute GitHub Actions workflows locally using act: $ARGUMENTS

## Current Workflows

- Available workflows: !`find .github/workflows -name "*.yml" -o -name "*.yaml" | head -10`
- Act configuration: @.actrc (if exists)
- Docker status: !`docker --version`

## Task

Execute GitHub Actions workflow locally:

1. **Setup Verification**
   - Ensure act is installed: `act --version`
   - Verify Docker is running
   - Check available workflows in `.github/workflows/`

2. **Workflow Selection**
   - If workflow specified: Run specific workflow `$ARGUMENTS`
   - If no workflow: List all available workflows
   - Check workflow triggers and events

3. **Local Execution**
   - Run workflow with appropriate flags
   - Use secrets from `.env` or `.secrets`
   - Handle platform-specific runners
   - Monitor execution and logs

4. **Debugging Support**
   - Use `--verbose` for detailed output
   - Use `--dry-run` for testing
   - Use `--list` to show available actions

## Example Commands

```bash
# List all workflows
act --list

# Run specific workflow
act workflow_dispatch -W .github/workflows/$ARGUMENTS.yml

# Run with secrets
act --secret-file .env

# Debug mode
act --verbose --dry-run
```

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
