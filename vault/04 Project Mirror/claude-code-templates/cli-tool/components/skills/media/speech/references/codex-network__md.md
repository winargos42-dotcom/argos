---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/media/speech/references/codex-network.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\media\speech\references\codex-network.md
source_ext: .md
source_sha256: e1472401dca9f289baf833befcb96d1c8ba4c53b1185b047486ad10bd1907147
text_sha256: c956a51d3e67246cfb43982aa8c82065350fcce4ef7b94bd89e599c575c94d9c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# codex-network.md

- Source: `claude-code-templates/cli-tool/components/skills/media/speech/references/codex-network.md`
- Extract: `text`
- SHA256: `e1472401dca9f289baf833befcb96d1c8ba4c53b1185b047486ad10bd1907147`

## Content

# Codex network approvals / sandbox notes

This guidance is intentionally isolated from `SKILL.md` because it can vary by environment and may become stale. Prefer the defaults in your environment when in doubt.

## Why am I asked to approve every speech generation call?
Speech generation uses the OpenAI Audio API, so the CLI needs outbound network access. In many Codex setups, network access is disabled by default (especially under stricter sandbox modes), and/or the approval policy may require confirmation before networked commands run.

## How do I reduce repeated approval prompts (network)?
If you trust the repo and want fewer prompts, enable network access for the relevant sandbox mode and relax the approval policy.

Example `~/.codex/config.toml` pattern:

```
approval_policy = "never"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

Or for a single session:

```
codex --sandbox workspace-write --ask-for-approval never
```

## Safety note
Use caution: enabling network and disabling approvals reduces friction but increases risk if you run untrusted code or work in an untrusted repository.

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
