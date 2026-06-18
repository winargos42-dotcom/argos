---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/gws-licensing.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\gws-licensing.md
source_ext: .md
source_sha256: 2e93550ccc8c9ec455cd1c815df0b90095e8928a53e08c9dae9efbb276906047
text_sha256: 70b0a28fd7ba74297c9a547b1a2aee429cff6c6ce042f603f108e435e8d09f43
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# gws-licensing.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/gws-licensing.md`
- Extract: `text`
- SHA256: `2e93550ccc8c9ec455cd1c815df0b90095e8928a53e08c9dae9efbb276906047`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [resource] [method] [flags]
description: Google Workspace Enterprise License Manager: Manage product licenses.
---

# Google Workspace Licensing

Execute Google Workspace Licensing operations: $ARGUMENTS

## Prerequisites

- Google Workspace CLI (`gws`) must be installed
- Authentication configured: Run `gws auth status` to verify
- Review `gws licensing --help` for all available commands

## Available Resources and Methods

# licensing (v1)

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

```bash
gws licensing <resource> <method> [flags]
```

## API Resources

### licenseAssignments

  - `delete` — Revoke a license.
  - `get` — Get a specific user's license by product SKU.
  - `insert` — Assign a license.
  - `listForProduct` — List all users assigned licenses for a specific product SKU.
  - `listForProductAndSku` — List all users assigned licenses for a specific product SKU.
  - `patch` — Reassign a user's product SKU with a different SKU in the same product. This method supports patch semantics.
  - `update` — Reassign a user's product SKU with a different SKU in the same product.

## Discovering Commands

Before calling any API method, inspect it:

```bash
# Browse resources and methods
gws licensing --help

# Inspect a method's required params, types, and defaults
gws schema licensing.<resource>.<method>
```

Use `gws schema` output to build your `--params` and `--json` flags.

## Usage

```bash
# List available resources and methods
gws licensing --help

# Inspect method schema before calling
gws schema licensing.<resource>.<method>

# Execute command with arguments
gws licensing $ARGUMENTS
```

## Task

Execute the requested Licensing operation: $ARGUMENTS

1. **Verify Prerequisites**
   - Check `gws` is installed: `gws --version`
   - Verify authentication: `gws auth status`
   - Review available commands: `gws licensing --help`

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
**Original Skill**: `gws-licensing`

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
