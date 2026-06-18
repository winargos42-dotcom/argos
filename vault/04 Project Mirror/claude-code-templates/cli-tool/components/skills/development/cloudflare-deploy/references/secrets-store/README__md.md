---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/secrets-store/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\secrets-store\README.md
source_ext: .md
source_sha256: 743347003a1bc091e537398fd7a96bda5a8a3df87b55f584c991016b37f392c1
text_sha256: 82c078e9d71d9bd28b2f23535f086e74bec7adad08e3cb6c289326a4a6e14550
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/secrets-store/README.md`
- Extract: `text`
- SHA256: `743347003a1bc091e537398fd7a96bda5a8a3df87b55f584c991016b37f392c1`

## Content

# Cloudflare Secrets Store

Account-level encrypted secret management for Workers and AI Gateway.

## Overview

**Secrets Store**: Centralized, account-level secrets, reusable across Workers
**Worker Secrets**: Per-Worker secrets (`wrangler secret put`)

### Architecture

- **Store**: Container (1/account in beta)
- **Secret**: String ≤1024 bytes
- **Scopes**: Permission boundaries controlling access
  - `workers`: For Workers runtime access
  - `ai-gateway`: For AI Gateway access
  - Secrets must have correct scope for binding to work
- **Bindings**: Connect secrets via `env` object

**Regional Availability**: Global except China Network (unavailable)

### Access Control

- **Super Admin**: Full access
- **Admin**: Create/edit/delete secrets, view metadata
- **Deployer**: View metadata + bindings
- **Reporter**: View metadata only

API Token permissions: `Account Secrets Store Edit/Read`

### Limits (Beta)

- 100 secrets/account
- 1 store/account
- 1024 bytes max/secret
- Production secrets count toward limit

## When to Use

**Use Secrets Store when:**
- Multiple Workers share same credential
- Centralized management needed
- Compliance requires audit trail
- Team collaboration on secrets

**Use Worker Secrets when:**
- Secret unique to one Worker
- Simple single-Worker project
- No cross-Worker sharing needed

## In This Reference

### Reading Order by Task

| Task | Start Here | Then Read |
|------|------------|-----------|
| Quick overview | README.md | - |
| First-time setup | README.md → configuration.md | api.md |
| Add secret to Worker | configuration.md | api.md |
| Implement access pattern | api.md | patterns.md |
| Debug errors | gotchas.md | api.md |
| Secret rotation | patterns.md | configuration.md |
| Best practices | gotchas.md | patterns.md |

### Files

- [configuration.md](./configuration.md) - Wrangler commands, binding config
- [api.md](./api.md) - Binding API, get/put/delete operations
- [patterns.md](./patterns.md) - Rotation, encryption, access control
- [gotchas.md](./gotchas.md) - Security issues, limits, best practices

## See Also
- [workers](../workers/) - Worker bindings integration
- [wrangler](../wrangler/) - CLI secret management commands

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
