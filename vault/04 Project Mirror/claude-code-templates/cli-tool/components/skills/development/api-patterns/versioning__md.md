---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/api-patterns/versioning.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\api-patterns\versioning.md
source_ext: .md
source_sha256: 8ee15be17fea4b37f222039240d66683b1afd7efb436363c9bc1c15baa5bef63
text_sha256: 58abb2fc534e687bb54a4a191188f2698ec9ed3e4e12ba269d93cc03ed8d1ee6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# versioning.md

- Source: `claude-code-templates/cli-tool/components/skills/development/api-patterns/versioning.md`
- Extract: `text`
- SHA256: `8ee15be17fea4b37f222039240d66683b1afd7efb436363c9bc1c15baa5bef63`

## Content

# Versioning Strategies

> Plan for API evolution from day one.

## Decision Factors

| Strategy | Implementation | Trade-offs |
|----------|---------------|------------|
| **URI** | /v1/users | Clear, easy caching |
| **Header** | Accept-Version: 1 | Cleaner URLs, harder discovery |
| **Query** | ?version=1 | Easy to add, messy |
| **None** | Evolve carefully | Best for internal, risky for public |

## Versioning Philosophy

```
Consider:
├── Public API? → Version in URI
├── Internal only? → May not need versioning
├── GraphQL? → Typically no versions (evolve schema)
├── tRPC? → Types enforce compatibility
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
