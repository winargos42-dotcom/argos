---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/gws-modelarmor.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\gws-modelarmor.md
source_ext: .md
source_sha256: cb7a99b3c489b38d897f6fa6aca67c8f76f6bfd2930d08c9e0c06ecd36fe3c7e
text_sha256: 4cbc78f4f4d88779621f11c8f34d2b9e429c1ae4d452b51e701d207896430deb
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# gws-modelarmor.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/gws-modelarmor.md`
- Extract: `text`
- SHA256: `cb7a99b3c489b38d897f6fa6aca67c8f76f6bfd2930d08c9e0c06ecd36fe3c7e`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [resource] [method] [flags]
description: Google Model Armor: Filter user-generated content for safety.
---

# Google Workspace Modelarmor

Execute Google Workspace Modelarmor operations: $ARGUMENTS

## Prerequisites

- Google Workspace CLI (`gws`) must be installed
- Authentication configured: Run `gws auth status` to verify
- Review `gws modelarmor --help` for all available commands

## Available Resources and Methods

# modelarmor (v1)

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

```bash
gws modelarmor <resource> <method> [flags]
```

## Helper Commands

| Command | Description |
|---------|-------------|
| [`+sanitize-prompt`](../gws-modelarmor-sanitize-prompt/SKILL.md) | Sanitize a user prompt through a Model Armor template |
| [`+sanitize-response`](../gws-modelarmor-sanitize-response/SKILL.md) | Sanitize a model response through a Model Armor template |
| [`+create-template`](../gws-modelarmor-create-template/SKILL.md) | Create a new Model Armor template |

## Discovering Commands

Before calling any API method, inspect it:

```bash
# Browse resources and methods
gws modelarmor --help

# Inspect a method's required params, types, and defaults
gws schema modelarmor.<resource>.<method>
```

Use `gws schema` output to build your `--params` and `--json` flags.

## Usage

```bash
# List available resources and methods
gws modelarmor --help

# Inspect method schema before calling
gws schema modelarmor.<resource>.<method>

# Execute command with arguments
gws modelarmor $ARGUMENTS
```

## Task

Execute the requested Modelarmor operation: $ARGUMENTS

1. **Verify Prerequisites**
   - Check `gws` is installed: `gws --version`
   - Verify authentication: `gws auth status`
   - Review available commands: `gws modelarmor --help`

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
**Original Skill**: `gws-modelarmor`

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
