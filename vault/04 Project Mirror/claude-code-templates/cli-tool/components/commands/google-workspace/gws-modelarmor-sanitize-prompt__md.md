---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/gws-modelarmor-sanitize-prompt.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\gws-modelarmor-sanitize-prompt.md
source_ext: .md
source_sha256: 86213716e51d60059022ce831ede1836628a670dededefd9b0069f2538d178f9
text_sha256: d129b42baa5b622908c55983cfcd070efa1931fc400bf4046f45832500d49ba7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# gws-modelarmor-sanitize-prompt.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/gws-modelarmor-sanitize-prompt.md`
- Extract: `text`
- SHA256: `86213716e51d60059022ce831ede1836628a670dededefd9b0069f2538d178f9`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [resource] [method] [flags]
description: Google Model Armor: Sanitize a user prompt through a Model Armor template.
---

# Google Workspace Modelarmor Sanitize Prompt

Execute Google Workspace Modelarmor Sanitize Prompt operations: $ARGUMENTS

## Prerequisites

- Google Workspace CLI (`gws`) must be installed
- Authentication configured: Run `gws auth status` to verify
- Review `gws modelarmor-sanitize-prompt --help` for all available commands

## Available Resources and Methods

# modelarmor +sanitize-prompt

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

Sanitize a user prompt through a Model Armor template

## Usage

```bash
gws modelarmor +sanitize-prompt --template <NAME>
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--template` | ✓ | — | Full template resource name (projects/PROJECT/locations/LOCATION/templates/TEMPLATE) |
| `--text` | — | — | Text content to sanitize |
| `--json` | — | — | Full JSON request body (overrides --text) |

## Examples

```bash
gws modelarmor +sanitize-prompt --template projects/P/locations/L/templates/T --text 'user input'
echo 'prompt' | gws modelarmor +sanitize-prompt --template ...
```

## Tips

- If neither --text nor --json is given, reads from stdin.
- For outbound safety, use +sanitize-response instead.

## See Also

- [gws-shared](../gws-shared/SKILL.md) — Global flags and auth
- [gws-modelarmor](../gws-modelarmor/SKILL.md) — All filter user-generated content for safety commands

## Usage

```bash
# List available resources and methods
gws modelarmor-sanitize-prompt --help

# Inspect method schema before calling
gws schema modelarmor-sanitize-prompt.<resource>.<method>

# Execute command with arguments
gws modelarmor-sanitize-prompt $ARGUMENTS
```

## Task

Execute the requested Modelarmor Sanitize Prompt operation: $ARGUMENTS

1. **Verify Prerequisites**
   - Check `gws` is installed: `gws --version`
   - Verify authentication: `gws auth status`
   - Review available commands: `gws modelarmor-sanitize-prompt --help`

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
**Original Skill**: `gws-modelarmor-sanitize-prompt`

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
