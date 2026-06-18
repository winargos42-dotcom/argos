---
argos_import: project_file
source_path: mempalace-develop/examples/HOOKS_TUTORIAL.md
source_abs: F:\debug\argoss\mempalace-develop\examples\HOOKS_TUTORIAL.md
source_ext: .md
source_sha256: 32c47cae5262a7ad10834df2b77c0c9819c03e2c2f4439d12bf75d56c3f552ff
text_sha256: 32c47cae5262a7ad10834df2b77c0c9819c03e2c2f4439d12bf75d56c3f552ff
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# HOOKS_TUTORIAL.md

- Source: `mempalace-develop/examples/HOOKS_TUTORIAL.md`
- Extract: `text`
- SHA256: `32c47cae5262a7ad10834df2b77c0c9819c03e2c2f4439d12bf75d56c3f552ff`

## Content

# How to Use MemPalace Hooks (Auto-Save)

MemPalace hooks act as an "Auto-Save" feature. They help your AI keep a permanent memory without you needing to run manual commands.

### 1. What are these hooks?
* **Save Hook** (`mempal_save_hook.sh`): Saves new facts and decisions every 15 messages.
* **PreCompact Hook** (`mempal_precompact_hook.sh`): Saves your context right before the AI's memory window fills up.

### 2. Setup for Claude Code
Add this to your configuration file to enable automatic background saving:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "", 
        "hooks": [{"type": "command", "command": "./hooks/mempal_save_hook.sh"}]
      }
    ],
    "PreCompact": [
      {
        "matcher": "", 
        "hooks": [{"type": "command", "command": "./hooks/mempal_precompact_hook.sh"}]
      }
    ]
  }
}

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
