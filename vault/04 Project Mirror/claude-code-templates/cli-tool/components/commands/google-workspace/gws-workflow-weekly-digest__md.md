---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/gws-workflow-weekly-digest.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\gws-workflow-weekly-digest.md
source_ext: .md
source_sha256: 8d4491dc12f975eca92c3e55e3369919dd8e900e215a26fa378893d7d82ad809
text_sha256: c6901b96091255e3e740f7329764ed4baecffa1ac627176546665bb5d28dd1d9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# gws-workflow-weekly-digest.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/gws-workflow-weekly-digest.md`
- Extract: `text`
- SHA256: `8d4491dc12f975eca92c3e55e3369919dd8e900e215a26fa378893d7d82ad809`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [resource] [method] [flags]
description: Google Workflow: Weekly summary: this week's meetings + unread email count.
---

# Google Workspace Workflow Weekly Digest

Execute Google Workspace Workflow Weekly Digest operations: $ARGUMENTS

## Prerequisites

- Google Workspace CLI (`gws`) must be installed
- Authentication configured: Run `gws auth status` to verify
- Review `gws workflow-weekly-digest --help` for all available commands

## Available Resources and Methods

# workflow +weekly-digest

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

Weekly summary: this week's meetings + unread email count

## Usage

```bash
gws workflow +weekly-digest
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--format` | — | — | Output format: json (default), table, yaml, csv |

## Examples

```bash
gws workflow +weekly-digest
gws workflow +weekly-digest --format table
```

## Tips

- Read-only — never modifies data.
- Combines calendar agenda (week) with gmail triage summary.

## See Also

- [gws-shared](../gws-shared/SKILL.md) — Global flags and auth
- [gws-workflow](../gws-workflow/SKILL.md) — All cross-service productivity workflows commands

## Usage

```bash
# List available resources and methods
gws workflow-weekly-digest --help

# Inspect method schema before calling
gws schema workflow-weekly-digest.<resource>.<method>

# Execute command with arguments
gws workflow-weekly-digest $ARGUMENTS
```

## Task

Execute the requested Workflow Weekly Digest operation: $ARGUMENTS

1. **Verify Prerequisites**
   - Check `gws` is installed: `gws --version`
   - Verify authentication: `gws auth status`
   - Review available commands: `gws workflow-weekly-digest --help`

2. **Inspect Method Schema**
   - Before calling any method, inspect its parameters
   - Use `gws schema` to understand required fields
   - Review parameter types and constraints

3. **Execute Operation**
   - Build command with appropriate flags
   - Use `--params` for query/path parameters
   - Use `--json` for request body
   - Handle pagination with `--max-results` or `--page-token`

4. **Error Handling**
   - Check command output for errors
   - Review API quotas and rate limits
   - Handle authentication issues
   - Retry transient failures

---

**License**: Apache License 2.0
**Source**: [Google Workspace CLI](https://github.com/googleworkspace/cli)
**Original Skill**: `gws-workflow-weekly-digest`

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
