---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/api-patterns/rate-limiting.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\api-patterns\rate-limiting.md
source_ext: .md
source_sha256: 633a0a84726b8b2ba35aa5eb9fcaed795d91cd0d9458d364ac7dff832c18beef
text_sha256: f1538d288ce362012241a6085beb3b5ff06d11f754b5867bf0adb7b62afd0657
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# rate-limiting.md

- Source: `claude-code-templates/cli-tool/components/skills/development/api-patterns/rate-limiting.md`
- Extract: `text`
- SHA256: `633a0a84726b8b2ba35aa5eb9fcaed795d91cd0d9458d364ac7dff832c18beef`

## Content

# Rate Limiting Principles

> Protect your API from abuse and overload.

## Why Rate Limit

```
Protect against:
├── Brute force attacks
├── Resource exhaustion
├── Cost overruns (if pay-per-use)
└── Unfair usage
```

## Strategy Selection

| Type | How | When |
|------|-----|------|
| **Token bucket** | Burst allowed, refills over time | Most APIs |
| **Sliding window** | Smooth distribution | Strict limits |
| **Fixed window** | Simple counters per window | Basic needs |

## Response Headers

```
Include in headers:
├── X-RateLimit-Limit (max requests)
├── X-RateLimit-Remaining (requests left)
├── X-RateLimit-Reset (when limit resets)
└── Return 429 when exceeded
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
