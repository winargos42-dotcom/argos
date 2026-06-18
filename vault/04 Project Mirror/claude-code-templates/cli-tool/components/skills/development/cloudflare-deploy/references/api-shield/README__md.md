---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/api-shield/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\api-shield\README.md
source_ext: .md
source_sha256: bc9a99bfca5fae2d575d890201441b7856e6791a7fb8430c7404059a20ced389
text_sha256: a032c7160b70c9a200e982bc457acd746760c2960e25b7554dfb315da98f71dc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/api-shield/README.md`
- Extract: `text`
- SHA256: `bc9a99bfca5fae2d575d890201441b7856e6791a7fb8430c7404059a20ced389`

## Content

# Cloudflare API Shield Reference

Expert guidance for API Shield - comprehensive API security suite for discovery, protection, and monitoring.

## Reading Order

| Task | Files to Read |
|------|---------------|
| Initial setup | README → configuration.md |
| Implement JWT validation | configuration.md → api.md |
| Add schema validation | configuration.md → patterns.md |
| Detect API attacks | patterns.md → api.md |
| Debug issues | gotchas.md |

## Feature Selection

What protection do you need?

```
├─ Validate request/response structure → Schema Validation 2.0 (configuration.md)
├─ Verify auth tokens → JWT Validation (configuration.md)
├─ Client certificates → mTLS (configuration.md)
├─ Detect BOLA attacks → BOLA Detection (patterns.md)
├─ Track auth coverage → Auth Posture (patterns.md)
├─ Stop volumetric abuse → Abuse Detection (patterns.md)
└─ Discover shadow APIs → API Discovery (api.md)
```

## In This Reference

- **[configuration.md](configuration.md)** - Setup, session identifiers, rules, token/mTLS configs
- **[api.md](api.md)** - Endpoint management, discovery, validation APIs, GraphQL operations
- **[patterns.md](patterns.md)** - Common patterns, progressive rollout, OWASP mappings, workflows
- **[gotchas.md](gotchas.md)** - Troubleshooting, false positives, performance, best practices

## Quick Start

API Shield: Enterprise-grade API security (Discovery, Schema Validation 2.0, JWT, mTLS, BOLA Detection, Auth Posture). Available as Enterprise add-on with preview access.

## See Also

- [API Shield Docs](https://developers.cloudflare.com/api-shield/)
- [API Reference](https://developers.cloudflare.com/api/resources/api_gateway/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

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
