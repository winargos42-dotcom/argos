---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/render-deploy/references/troubleshooting-basics.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\render-deploy\references\troubleshooting-basics.md
source_ext: .md
source_sha256: 1344b4dbd51ac04b0ef11602e7305280a922aac9368a5d40200cf3c5456077ca
text_sha256: f999b13fc56ff62ccf6eec593d0e4cee94e52dec27a815e40d68532bf558a4ca
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# troubleshooting-basics.md

- Source: `claude-code-templates/cli-tool/components/skills/development/render-deploy/references/troubleshooting-basics.md`
- Extract: `text`
- SHA256: `1344b4dbd51ac04b0ef11602e7305280a922aac9368a5d40200cf3c5456077ca`

## Content

# Basic troubleshooting (deploy-time and startup)

Use this when a deploy fails, the service crashes on start, or health checks time out.
Keep fixes minimal and redeploy after each change.

## 1) Classify the failure

- **Build failure**: errors in build logs, missing dependencies, build command issues.
- **Startup failure**: app exits quickly, crashes, or cannot bind to `$PORT`.
- **Runtime/health failure**: service is live but health checks fail or 5xx errors.

## 2) Quick checks by class

**Build failure**
- Confirm the build command is correct for the runtime.
- Ensure required dependencies are present in `package.json`, `requirements.txt`, etc.
- Check for missing build-time env vars.

**Startup failure**
- Confirm the start command and working directory.
- Ensure port binding is `0.0.0.0:$PORT`.
- Check for missing runtime env vars (secrets, DB URLs).

**Runtime/health failure**
- Verify the health endpoint path and response.
- Confirm the app is actually listening on `$PORT`.
- Check database connectivity and migrations.

## 3) Map error signatures to fixes

Use [error-patterns.md](error-patterns.md) for a compact catalog of common log messages.

## 4) If still blocked

Gather the latest build logs and runtime error logs, then consider the optional
`render-debug` skill for deeper diagnostics (metrics, DB checks, expanded patterns).

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
