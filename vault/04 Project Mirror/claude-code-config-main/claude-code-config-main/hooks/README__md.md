---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/hooks/README.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\hooks\README.md
source_ext: .md
source_sha256: 0c647cec0abc26a3d6506762334502ac6a14cf2da8d26e8541bb5ab66df9a953
text_sha256: 0c647cec0abc26a3d6506762334502ac6a14cf2da8d26e8541bb5ab66df9a953
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:26
---

# README.md

- Source: `claude-code-config-main/claude-code-config-main/hooks/README.md`
- Extract: `text`
- SHA256: `0c647cec0abc26a3d6506762334502ac6a14cf2da8d26e8541bb5ab66df9a953`

## Content

# Hook Examples

Ready-to-use hook scripts for Claude Code. Copy to your project or `~/.claude/` and register in `settings.json`.

## Quick Setup

Add any hook to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "EventName": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python path/to/script.py",
            "statusMessage": "Running hook..."
          }
        ]
      }
    ]
  }
}
```

## Available Hooks

### Session Management

| Script | Event | What It Does |
|---|---|---|
| [session-drift-validator.py](session-drift-validator.py) | `SessionStart` | Validates file path references in CLAUDE.md and rules/ at session start. Catches stale pointers before the agent acts on them. |
| [session-handoff-reminder.py](session-handoff-reminder.py) | `Stop` | Reminds to write a handoff file when closing a long session. Prevents context loss between sessions. |

### Safety Guards

| Script | Event | What It Does |
|---|---|---|
| [destructive-command-guard.py](destructive-command-guard.py) | `PreToolUse` | Warns before destructive commands (`rm -rf`, `DROP TABLE`, `git push --force`, `git reset --hard`). Returns `{"decision": "block"}` with explanation. |
| [secret-leak-guard.py](secret-leak-guard.py) | `PreToolUse` | Blocks Write/Edit operations that would introduce secrets (API keys, tokens, passwords) into tracked files. |

### Quality & Context

| Script | Event | What It Does |
|---|---|---|
| [kvcache-stats.py](../scripts/kvcache_stats.py) | Manual | Analyzes KV-cache hit rate across sessions. Not a hook but a diagnostic script. |

## Hook Events Reference (Claude Code v2.1.89+)

| Event | When It Fires | Use For |
|---|---|---|
| `SessionStart` | New session begins | Validation, context loading, drift detection |
| `Stop` | Session ends | Handoff, cleanup, learning extraction |
| `PreToolUse` | Before any tool call | Safety guards, permission checks, logging |
| `PostToolUse` | After any tool call | Logging, notifications, side effects |
| `Notification` | Agent sends notification | Custom notification routing |
| `TaskCreated` | Sub-agent task spawned | Tracking, resource allocation |

### Conditional Hooks (v2.1.89+)

Use the `if` field to run hooks only for specific patterns:

```json
{
  "event": "PreToolUse",
  "hooks": [{ "type": "command", "command": "check_git.sh" }],
  "if": "Bash(git *)"
}
```

### Hook Responses

Hooks can return JSON to control behavior:

| Response | Effect |
|---|---|
| `{"decision": "allow"}` | Proceed normally |
| `{"decision": "block", "reason": "..."}` | Block the tool call |
| `{"decision": "defer"}` | Pause headless session for human review |
| `{"retry": true}` | Retry after PermissionDenied (v2.1.89+) |

### Matcher Patterns for PreToolUse/PostToolUse

```json
{"matcher": "Bash"}           // Any Bash call
{"matcher": "Write"}          // Any file write
{"matcher": "Bash(git *)"}    // Git commands only
{"matcher": "Bash(rm *)"}     // Delete commands only
{"matcher": "mcp__*"}         // Any MCP tool call
```

## Principles

- **Hook > Rule** for guaranteed behaviors. Rules are instructions of hope; hooks execute unconditionally.
- **One concern per hook.** Don't combine drift validation with secret scanning.
- **Exit 0 always.** A crashing hook blocks the agent. Use `|| true` in settings.json as a safety net.
- **Keep hooks fast.** They run synchronously. Target <500ms per hook.

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
