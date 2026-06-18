---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/architecture/patterns-reference.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\architecture\patterns-reference.md
source_ext: .md
source_sha256: 86e2088c3f2c87fa9d5cbfbd17cd265783aefc7ef7a361638d866bfb0a930c74
text_sha256: 264d0c372a6b5d2a7bba506a4dd4d74855f69298d4dabf1ae046d51f2f49bd9d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# patterns-reference.md

- Source: `claude-code-templates/cli-tool/components/skills/development/architecture/patterns-reference.md`
- Extract: `text`
- SHA256: `86e2088c3f2c87fa9d5cbfbd17cd265783aefc7ef7a361638d866bfb0a930c74`

## Content

# Architecture Patterns Reference

> Quick reference for common patterns with usage guidance.

## Data Access Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Active Record** | Simple CRUD, rapid prototyping | Complex queries, multiple sources | Low |
| **Repository** | Testing needed, multiple sources | Simple CRUD, single database | Medium |
| **Unit of Work** | Complex transactions | Simple operations | High |
| **Data Mapper** | Complex domain, performance | Simple CRUD, rapid dev | High |

## Domain Logic Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Transaction Script** | Simple CRUD, procedural | Complex business rules | Low |
| **Table Module** | Record-based logic | Rich behavior needed | Low |
| **Domain Model** | Complex business logic | Simple CRUD | Medium |
| **DDD (Full)** | Complex domain, domain experts | Simple domain, no experts | High |

## Distributed System Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Modular Monolith** | Small teams, unclear boundaries | Clear contexts, different scales | Medium |
| **Microservices** | Different scales, large teams | Small teams, simple domain | Very High |
| **Event-Driven** | Real-time, loose coupling | Simple workflows, strong consistency | High |
| **CQRS** | Read/write performance diverges | Simple CRUD, same model | High |
| **Saga** | Distributed transactions | Single database, simple ACID | High |

## API Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **REST** | Standard CRUD, resources | Real-time, complex queries | Low |
| **GraphQL** | Flexible queries, multiple clients | Simple CRUD, caching needs | Medium |
| **gRPC** | Internal services, performance | Public APIs, browser clients | Medium |
| **WebSocket** | Real-time updates | Simple request/response | Medium |

---

## Simplicity Principle

**"Start simple, add complexity only when proven necessary."**

- You can always add patterns later
- Removing complexity is MUCH harder than adding it
- When in doubt, choose simpler option

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
