---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/render-deploy/references/post-deploy-checks.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\render-deploy\references\post-deploy-checks.md
source_ext: .md
source_sha256: 294b93e3365d731bfe0a91e46b05a01868e38319707d8776ce8031cce8feec30
text_sha256: bd1e3e24abe6c9eb63164ac8ada9b285ceaffbd1722f58bbc1d3d94af4c59911
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# post-deploy-checks.md

- Source: `claude-code-templates/cli-tool/components/skills/development/render-deploy/references/post-deploy-checks.md`
- Extract: `text`
- SHA256: `294b93e3365d731bfe0a91e46b05a01868e38319707d8776ce8031cce8feec30`

## Content

# Post-deploy checks

Use this after any deploy or service creation. Keep it short; stop when a check fails.

## 1) Confirm deploy status

```
list_deploys(serviceId: "<service-id>", limit: 1)
```

- Expect `status: "live"`.
- If status is failed, inspect build/runtime logs immediately.

## 2) Verify service health

- Hit the health endpoint (preferred) or `/` and confirm a 200 response.
- If there is no health endpoint, add one and redeploy.

## 3) Scan recent error logs

```
list_logs(resource: ["<service-id>"], level: ["error"], limit: 50)
```

- If you see a clear error signature, jump to the matching fix in
  [troubleshooting-basics.md](troubleshooting-basics.md) or
  [error-patterns.md](error-patterns.md).

## 4) Verify env vars and port binding

- Confirm all required env vars are set (especially secrets marked `sync: false`).
- Ensure the app binds to `0.0.0.0:$PORT` (not localhost).

## 5) Redeploy only after fixing the first failure

- Avoid repeated deploys without changes; fix one issue at a time.

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
