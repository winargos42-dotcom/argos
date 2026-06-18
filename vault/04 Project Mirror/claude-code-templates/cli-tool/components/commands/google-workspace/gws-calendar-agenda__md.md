---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/gws-calendar-agenda.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\gws-calendar-agenda.md
source_ext: .md
source_sha256: dd6a2e06df334179579304d5f5b0dae0d57b92ea342cbcba7b1dac89d06b84e8
text_sha256: fb7aac802ea27f890834e3b6e27b8707ec6e537eab80fe852d1fb67ba35773ff
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# gws-calendar-agenda.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/gws-calendar-agenda.md`
- Extract: `text`
- SHA256: `dd6a2e06df334179579304d5f5b0dae0d57b92ea342cbcba7b1dac89d06b84e8`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [resource] [method] [flags]
description: Google Calendar: Show upcoming events across all calendars.
---

# Google Workspace Calendar Agenda

Execute Google Workspace Calendar Agenda operations: $ARGUMENTS

## Prerequisites

- Google Workspace CLI (`gws`) must be installed
- Authentication configured: Run `gws auth status` to verify
- Review `gws calendar-agenda --help` for all available commands

## Available Resources and Methods

# calendar +agenda

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

Show upcoming events across all calendars

## Usage

```bash
gws calendar +agenda
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--today` | — | — | Show today's events |
| `--tomorrow` | — | — | Show tomorrow's events |
| `--week` | — | — | Show this week's events |
| `--days` | — | — | Number of days ahead to show |
| `--calendar` | — | — | Filter to specific calendar name or ID |

## Examples

```bash
gws calendar +agenda
gws calendar +agenda --today
gws calendar +agenda --week --format table
gws calendar +agenda --days 3 --calendar 'Work'
```

## Tips

- Read-only — never modifies events.
- Queries all calendars by default; use --calendar to filter.

## See Also

- [gws-shared](../gws-shared/SKILL.md) — Global flags and auth
- [gws-calendar](../gws-calendar/SKILL.md) — All manage calendars and events commands

## Usage

```bash
# List available resources and methods
gws calendar-agenda --help

# Inspect method schema before calling
gws schema calendar-agenda.<resource>.<method>

# Execute command with arguments
gws calendar-agenda $ARGUMENTS
```

## Task

Execute the requested Calendar Agenda operation: $ARGUMENTS

1. **Verify Prerequisites**
   - Check `gws` is installed: `gws --version`
   - Verify authentication: `gws auth status`
   - Review available commands: `gws calendar-agenda --help`

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
**Original Skill**: `gws-calendar-agenda`

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
