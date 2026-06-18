---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/api-patterns/api-style.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\api-patterns\api-style.md
source_ext: .md
source_sha256: 7949ef165589396c15127e356d8298df9757a0b896aeaad12edba87840e11ffe
text_sha256: ac7b7677e862c7b6f1a622425ac398807890272a3dcb31f528993f6411abccc2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# api-style.md

- Source: `claude-code-templates/cli-tool/components/skills/development/api-patterns/api-style.md`
- Extract: `text`
- SHA256: `7949ef165589396c15127e356d8298df9757a0b896aeaad12edba87840e11ffe`

## Content

# API Style Selection (2025)

> REST vs GraphQL vs tRPC - Hangi durumda hangisi?

## Decision Tree

```
Who are the API consumers?
│
├── Public API / Multiple platforms
│   └── REST + OpenAPI (widest compatibility)
│
├── Complex data needs / Multiple frontends
│   └── GraphQL (flexible queries)
│
├── TypeScript frontend + backend (monorepo)
│   └── tRPC (end-to-end type safety)
│
├── Real-time / Event-driven
│   └── WebSocket + AsyncAPI
│
└── Internal microservices
    └── gRPC (performance) or REST (simplicity)
```

## Comparison

| Factor | REST | GraphQL | tRPC |
|--------|------|---------|------|
| **Best for** | Public APIs | Complex apps | TS monorepos |
| **Learning curve** | Low | Medium | Low (if TS) |
| **Over/under fetching** | Common | Solved | Solved |
| **Type safety** | Manual (OpenAPI) | Schema-based | Automatic |
| **Caching** | HTTP native | Complex | Client-based |

## Selection Questions

1. Who are the API consumers?
2. Is the frontend TypeScript?
3. How complex are the data relationships?
4. Is caching critical?
5. Public or internal API?

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
