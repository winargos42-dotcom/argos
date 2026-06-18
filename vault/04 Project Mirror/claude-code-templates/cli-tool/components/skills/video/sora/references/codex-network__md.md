---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/video/sora/references/codex-network.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\video\sora\references\codex-network.md
source_ext: .md
source_sha256: ac2278dc8bc6a13ed289cfd6f37a523365470a9b780d005f48f900d85da62cb2
text_sha256: 923fce6a135ea02b7119292418490ee4bf5764104fcb69aaabd89baa8fde57c4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# codex-network.md

- Source: `claude-code-templates/cli-tool/components/skills/video/sora/references/codex-network.md`
- Extract: `text`
- SHA256: `ac2278dc8bc6a13ed289cfd6f37a523365470a9b780d005f48f900d85da62cb2`

## Content

# Codex network approvals / sandbox notes

This guidance is intentionally isolated from `SKILL.md` because it can vary by environment and may become stale. Prefer the defaults in your environment when in doubt.

## Why am I asked to approve every video generation call?
Video generation uses the OpenAI Video API, so the CLI needs outbound network access. In many Codex setups, network access is disabled by default (especially under stricter sandbox modes), and/or the approval policy may require confirmation before networked commands run.

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
