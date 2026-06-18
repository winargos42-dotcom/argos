---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/render-deploy/references/error-patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\render-deploy\references\error-patterns.md
source_ext: .md
source_sha256: d73664ce45370934f476d660556b4d8e57c979d7b431d401406e203a6ba9f074
text_sha256: b5556cdd3ba832e8f33602cf207cd80872df9c89ed17fe92129a56903176675b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# error-patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/render-deploy/references/error-patterns.md`
- Extract: `text`
- SHA256: `d73664ce45370934f476d660556b4d8e57c979d7b431d401406e203a6ba9f074`

## Content

# Error patterns (compact)

Use this to quickly map log signatures to likely causes and fixes.

| Log pattern | Likely cause | Quick fix |
| --- | --- | --- |
| `KeyError`, `not defined`, `missing environment` | Missing env var | Add env var in render.yaml or via MCP, then redeploy |
| `EADDRINUSE`, `listen EADDRINUSE` | Port binding conflict | Bind to `0.0.0.0:$PORT` |
| `Cannot find module`, `ModuleNotFoundError` | Missing dependency | Add dependency to manifest and rebuild |
| `ECONNREFUSED`, `connection refused` | DB not reachable | Verify DATABASE_URL and DB status |
| `Health check timeout` | No healthy response | Add/verify health endpoint and port |
| `exit 137`, `out of memory` | OOM | Reduce memory use or upgrade plan |
| `Command failed`, `build failed` | Bad build command | Fix build command or dependencies |

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
