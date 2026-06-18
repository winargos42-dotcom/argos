---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/gws-gmail-triage.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\gws-gmail-triage.md
source_ext: .md
source_sha256: 032d41b514db107f682b6804c5c049841816428326a6afefce8ad79212cd93aa
text_sha256: 2cdb102a81f45a9e0574a029d0a9d12cbe568e03ded30d3494ebefcf58e26ef9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# gws-gmail-triage.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/gws-gmail-triage.md`
- Extract: `text`
- SHA256: `032d41b514db107f682b6804c5c049841816428326a6afefce8ad79212cd93aa`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [resource] [method] [flags]
description: Gmail: Show unread inbox summary (sender, subject, date).
---

# Google Workspace Gmail Triage

Execute Google Workspace Gmail Triage operations: $ARGUMENTS

## Prerequisites

- Google Workspace CLI (`gws`) must be installed
- Authentication configured: Run `gws auth status` to verify
- Review `gws gmail-triage --help` for all available commands

## Available Resources and Methods

# gmail +triage

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

Show unread inbox summary (sender, subject, date)

## Usage

```bash
gws gmail +triage
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--max` | — | 20 | Maximum messages to show (default: 20) |
| `--query` | — | — | Gmail search query (default: is:unread) |
| `--labels` | — | — | Include label names in output |

## Examples

```bash
gws gmail +triage
gws gmail +triage --max 5 --query 'from:boss'
gws gmail +triage --format json | jq '.[].subject'
gws gmail +triage --labels
```

## Tips

- Read-only — never modifies your mailbox.
- Defaults to table output format.

## See Also

- [gws-shared](../gws-shared/SKILL.md) — Global flags and auth
- [gws-gmail](../gws-gmail/SKILL.md) — All send, read, and manage email commands

## Usage

```bash
# List available resources and methods
gws gmail-triage --help

# Inspect method schema before calling
gws schema gmail-triage.<resource>.<method>

# Execute command with arguments
gws gmail-triage $ARGUMENTS
```

## Task

Execute the requested Gmail Triage operation: $ARGUMENTS

1. **Verify Prerequisites**
   - Check `gws` is installed: `gws --version`
   - Verify authentication: `gws auth status`
   - Review available commands: `gws gmail-triage --help`

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
**Original Skill**: `gws-gmail-triage`

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
