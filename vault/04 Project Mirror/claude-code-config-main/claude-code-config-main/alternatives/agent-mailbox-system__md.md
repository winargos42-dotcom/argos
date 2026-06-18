---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/alternatives/agent-mailbox-system.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\alternatives\agent-mailbox-system.md
source_ext: .md
source_sha256: 25befc5ab4da6e4b3b8470d28dca3c95a4545c43a01a556f531632ca204ec5f0
text_sha256: 25befc5ab4da6e4b3b8470d28dca3c95a4545c43a01a556f531632ca204ec5f0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:26
---

# agent-mailbox-system.md

- Source: `claude-code-config-main/claude-code-config-main/alternatives/agent-mailbox-system.md`
- Extract: `text`
- SHA256: `25befc5ab4da6e4b3b8470d28dca3c95a4545c43a01a556f531632ca204ec5f0`

## Content

# Agent Mailbox System: File-based Inter-Agent Communication

Date: 2026-04-12

## Problem

Multiple Claude Code sessions working on the same project need to communicate: ask questions, report decisions, notify about completed tasks. Git push/pull is too slow for real-time communication.

## Solution: SMB-based File Mailbox

```
.claude/mailbox/
  ani/       <- inbox for agent "ani"
  artem/     <- inbox for agent "artem"
  nastya/    <- inbox for agent "nastya"
  all/       <- broadcast (all agents read)
```

Each message = markdown file with frontmatter:
```markdown
---
from: artem
to: ani
priority: normal
status: unread
date: 2026-04-11 14:46
topic: cmake libsodium question
---

Message body here.
```

## Delivery: Instant via SMB

If agents work on the same filesystem (SMB share, NFS, or same machine):
- Agent A writes file to `mailbox/B/` -> Agent B sees it instantly
- No git push/pull needed
- No daemon/server needed

For remote agents: use git push + hooks, or SMB over Tailscale/VPN.

## Auto-check via Hooks

```json
{
  "hooks": {
    "SessionStart": [{"hook_command": "python .claude/scripts/check_mail.py"}],
    "UserPromptSubmit": [{"hook_command": "python .claude/scripts/check_mail.py"}],
    "PreToolUse": [{"hook_command": "python .claude/scripts/check_mail_throttled.py"}]
  }
}
```

- **SessionStart**: full inbox check, show all unread
- **UserPromptSubmit**: check before each user message
- **PreToolUse (throttled)**: check every 2 min during autonomous work

Throttled version uses a timestamp file to avoid checking on every tool call.

## CLI

```bash
# Send
python mail.py send --from artem --to ani --topic "question" --body "text"

# Check inbox
python mail.py check --who ani --unread-only

# Broadcast
python mail.py broadcast --from ani --topic "architecture decision" --body "text"

# Summary
python mail.py summary
```

## Key Finding

UserPromptSubmit hook = best trigger. Agent sees new mail before processing user's next message. For long autonomous tasks, throttled PreToolUse every 2 min catches urgent messages.

## Real-world Usage

Used in retouch-app project with 3 agents (ani, artem, nastya):
- Ani sends task lists to Nastya via mailbox
- Nastya reports completed tasks back
- Broadcast for architecture decisions that affect all agents
- Instant delivery via SMB share (Z: drive over Tailscale)

## Files

- `mail.py` - CLI (send/check/reply/broadcast/summary)
- `check_mail.py` - full inbox check for SessionStart/UserPromptSubmit hooks
- `check_mail_throttled.py` - throttled check for PreToolUse hook
- `agent-mailbox.md` - rule for agents explaining the system

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
