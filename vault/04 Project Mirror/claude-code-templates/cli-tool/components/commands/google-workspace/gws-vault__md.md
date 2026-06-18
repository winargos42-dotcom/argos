---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/google-workspace/gws-vault.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\google-workspace\gws-vault.md
source_ext: .md
source_sha256: 390e15732e5a8ba0843c49edf31980e264eea3ce939e2f02ab212a158e28d367
text_sha256: 4d283636398ef29902613d5e3b4ae8a2e8870fca2ed9bf375f1cec339865b13f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# gws-vault.md

- Source: `claude-code-templates/cli-tool/components/commands/google-workspace/gws-vault.md`
- Extract: `text`
- SHA256: `390e15732e5a8ba0843c49edf31980e264eea3ce939e2f02ab212a158e28d367`

## Content

---
allowed-tools: Bash, Read, Write, Edit
argument-hint: [resource] [method] [flags]
description: Google Vault: Manage eDiscovery holds and exports.
---

# Google Workspace Vault

Execute Google Workspace Vault operations: $ARGUMENTS

## Prerequisites

- Google Workspace CLI (`gws`) must be installed
- Authentication configured: Run `gws auth status` to verify
- Review `gws vault --help` for all available commands

## Available Resources and Methods

# vault (v1)

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

```bash
gws vault <resource> <method> [flags]
```

## API Resources

### matters

  - `addPermissions` — Adds an account as a matter collaborator.
  - `close` — Closes the specified matter. Returns the matter with updated state.
  - `count` — Counts the accounts processed by the specified query.
  - `create` — Creates a matter with the given name and description. The initial state is open, and the owner is the method caller. Returns the created matter with default view.
  - `delete` — Deletes the specified matter. Returns the matter with updated state.
  - `get` — Gets the specified matter.
  - `list` — Lists matters the requestor has access to.
  - `removePermissions` — Removes an account as a matter collaborator.
  - `reopen` — Reopens the specified matter. Returns the matter with updated state.
  - `undelete` — Undeletes the specified matter. Returns the matter with updated state.
  - `update` — Updates the specified matter. This updates only the name and description of the matter, identified by matter ID. Changes to any other fields are ignored. Returns the default view of the matter.
  - `exports` — Operations on the 'exports' resource
  - `holds` — Operations on the 'holds' resource
  - `savedQueries` — Operations on the 'savedQueries' resource

### operations

  - `cancel` — Starts asynchronous cancellation on a long-running operation. The server makes a best effort to cancel the operation, but success is not guaranteed. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`. Clients can use Operations.GetOperation or other methods to check whether the cancellation succeeded or whether the operation completed despite cancellation.
  - `delete` — Deletes a long-running operation. This method indicates that the client is no longer interested in the operation result. It does not cancel the operation. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`.
  - `get` — Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.
  - `list` — Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`.

## Discovering Commands

Before calling any API method, inspect it:

```bash
# Browse resources and methods
gws vault --help

# Inspect a method's required params, types, and defaults
gws schema vault.<resource>.<method>
```

Use `gws schema` output to build your `--params` and `--json` flags.

## Usage

```bash
# List available resources and methods
gws vault --help

# Inspect method schema before calling
gws schema vault.<resource>.<method>

# Execute command with arguments
gws vault $ARGUMENTS
```

## Task

Execute the requested Vault operation: $ARGUMENTS

1. **Verify Prerequisites**
   - Check `gws` is installed: `gws --version`
   - Verify authentication: `gws auth status`
   - Review available commands: `gws vault --help`

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
**Original Skill**: `gws-vault`

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
