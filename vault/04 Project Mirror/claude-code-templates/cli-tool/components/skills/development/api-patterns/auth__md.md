---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/api-patterns/auth.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\api-patterns\auth.md
source_ext: .md
source_sha256: c7a18d1160ffaf3921f8c979dea78be5ae01443e77c2d3b6df869e00309f7415
text_sha256: d35ba351bf05454ad097522b80fb19368b47f66ff4ab0e76a0d69e303c2b72f0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# auth.md

- Source: `claude-code-templates/cli-tool/components/skills/development/api-patterns/auth.md`
- Extract: `text`
- SHA256: `c7a18d1160ffaf3921f8c979dea78be5ae01443e77c2d3b6df869e00309f7415`

## Content

# Authentication Patterns

> Choose auth pattern based on use case.

## Selection Guide

| Pattern | Best For |
|---------|----------|
| **JWT** | Stateless, microservices |
| **Session** | Traditional web, simple |
| **OAuth 2.0** | Third-party integration |
| **API Keys** | Server-to-server, public APIs |
| **Passkey** | Modern passwordless (2025+) |

## JWT Principles

```
Important:
├── Always verify signature
├── Check expiration
├── Include minimal claims
├── Use short expiry + refresh tokens
└── Never store sensitive data in JWT
```

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
