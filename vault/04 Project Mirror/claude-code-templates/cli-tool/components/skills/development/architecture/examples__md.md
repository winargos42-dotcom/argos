---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/architecture/examples.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\architecture\examples.md
source_ext: .md
source_sha256: f1eb6f965d497a3ed95223a95e5b6a4d65105243dd39f2f6d3208ca16cfb67f8
text_sha256: 5bdd281a7409189049af4c55fbf8c8f562c250cd3e34cd60741be113110843a5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# examples.md

- Source: `claude-code-templates/cli-tool/components/skills/development/architecture/examples.md`
- Extract: `text`
- SHA256: `f1eb6f965d497a3ed95223a95e5b6a4d65105243dd39f2f6d3208ca16cfb67f8`

## Content

# Architecture Examples

> Real-world architecture decisions by project type.

---

## Example 1: MVP E-commerce (Solo Developer)

```yaml
Requirements:
  - <1000 users initially
  - Solo developer
  - Fast to market (8 weeks)
  - Budget-conscious

Architecture Decisions:
  App Structure: Monolith (simpler for solo)
  Framework: Next.js (full-stack, fast)
  Data Layer: Prisma direct (no over-abstraction)
  Authentication: JWT (simpler than OAuth)
  Payment: Stripe (hosted solution)
  Database: PostgreSQL (ACID for orders)

Trade-offs Accepted:
  - Monolith → Can't scale independently (team doesn't justify it)
  - No Repository → Less testable (simple CRUD doesn't need it)
  - JWT → No social login initially (can add later)

Future Migration Path:
  - Users > 10K → Extract payment service
  - Team > 3 → Add Repository pattern
  - Social login requested → Add OAuth
```

---

## Example 2: SaaS Product (5-10 Developers)

```yaml
Requirements:
  - 1K-100K users
  - 5-10 developers
  - Long-term (12+ months)
  - Multiple domains (billing, users, core)

Architecture Decisions:
  App Structure: Modular Monolith (team size optimal)
  Framework: NestJS (modular by design)
  Data Layer: Repository pattern (testing, flexibility)
  Domain Model: Partial DDD (rich entities)
  Authentication: OAuth + JWT
  Caching: Redis
  Database: PostgreSQL

Trade-offs Accepted:
  - Modular Monolith → Some module coupling (microservices not justified)
  - Partial DDD → No full aggregates (no domain experts)
  - RabbitMQ later → Initial synchronous (add when proven needed)

Migration Path:
  - Team > 10 → Consider microservices
  - Domains conflict → Extract bounded contexts
  - Read performance issues → Add CQRS
```

---

## Example 3: Enterprise (100K+ Users)

```yaml
Requirements:
  - 100K+ users
  - 10+ developers
  - Multiple business domains
  - Different scaling needs
  - 24/7 availability

Architecture Decisions:
  App Structure: Microservices (independent scale)
  API Gateway: Kong/AWS API GW
  Domain Model: Full DDD
  Consistency: Event-driven (eventual OK)
  Message Bus: Kafka
  Authentication: OAuth + SAML (enterprise SSO)
  Database: Polyglot (right tool per job)
  CQRS: Selected services

Operational Requirements:
  - Service mesh (Istio/Linkerd)
  - Distributed tracing (Jaeger/Tempo)
  - Centralized logging (ELK/Loki)
  - Circuit breakers (Resilience4j)
  - Kubernetes/Helm
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
