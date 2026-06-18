---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/gws-workflow-standup-report.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\gws-workflow-standup-report.md
source_ext: .md
source_sha256: b85c32a49532377f48f89b0574167296259457bb60a431bb1f14707bc501a88a
text_sha256: a1ec8682bbe67e94e18cf40f80895f07cbed50e69ab5636eec00adebe31128bc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# gws-workflow-standup-report.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/gws-workflow-standup-report.md`
- Extract: `text`
- SHA256: `b85c32a49532377f48f89b0574167296259457bb60a431bb1f14707bc501a88a`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [resource] [method] [flags]
description: Google Workflow: Today's meetings + open tasks as a standup summary.
---

# Google Workspace Workflow Standup Report

Execute Google Workspace Workflow Standup Report operations: $ARGUMENTS

## Prerequisites

- Google Workspace CLI (`gws`) must be installed
- Authentication configured: Run `gws auth status` to verify
- Review `gws workflow-standup-report --help` for all available commands

## Available Resources and Methods

# workflow +standup-report

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

Today's meetings + open tasks as a standup summary

## Usage

```bash
gws workflow +standup-report
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--format` | — | — | Output format: json (default), table, yaml, csv |

## Examples

```bash
gws workflow +standup-report
gws workflow +standup-report --format table
```

## Tips

- Read-only — never modifies data.
- Combines calendar agenda (today) with tasks list.

## See Also

- [gws-shared](../gws-shared/SKILL.md) — Global flags and auth
- [gws-workflow](../gws-workflow/SKILL.md) — All cross-service productivity workflows commands

## Usage

```bash
# List available resources and methods
gws workflow-standup-report --help

# Inspect method schema before calling
gws schema workflow-standup-report.<resource>.<method>

# Execute command with arguments
gws workflow-standup-report $ARGUMENTS
```

## Task

Execute the requested Workflow Standup Report operation: $ARGUMENTS

1. **Verify Prerequisites**
   - Check `gws` is installed: `gws --version`
   - Verify authentication: `gws auth status`
   - Review available commands: `gws workflow-standup-report --help`

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
**Original Skill**: `gws-workflow-standup-report`

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
