---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/architecture/context-discovery.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\architecture\context-discovery.md
source_ext: .md
source_sha256: 6530f3270743104a992e95b01675d60a85e10466526da9fde9c1006540e8dcb7
text_sha256: 0698e38a37669c36c819bac70c51213bb955e99125ca96b690c840c317595a17
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# context-discovery.md

- Source: `claude-code-templates/cli-tool/components/skills/development/architecture/context-discovery.md`
- Extract: `text`
- SHA256: `6530f3270743104a992e95b01675d60a85e10466526da9fde9c1006540e8dcb7`

## Content

# Context Discovery

> Before suggesting any architecture, gather context.

## Question Hierarchy (Ask User FIRST)

1. **Scale**
   - How many users? (10, 1K, 100K, 1M+)
   - Data volume? (MB, GB, TB)
   - Transaction rate? (per second/minute)

2. **Team**
   - Solo developer or team?
   - Team size and expertise?
   - Distributed or co-located?

3. **Timeline**
   - MVP/Prototype or long-term product?
   - Time to market pressure?

4. **Domain**
   - CRUD-heavy or business logic complex?
   - Real-time requirements?
   - Compliance/regulations?

5. **Constraints**
   - Budget limitations?
   - Legacy systems to integrate?
   - Technology stack preferences?

## Project Classification Matrix

```
                    MVP              SaaS           Enterprise
┌─────────────────────────────────────────────────────────────┐
│ Scale        │ <1K           │ 1K-100K      │ 100K+        │
│ Team         │ Solo          │ 2-10         │ 10+          │
│ Timeline     │ Fast (weeks)  │ Medium (months)│ Long (years)│
│ Architecture │ Simple        │ Modular      │ Distributed  │
│ Patterns     │ Minimal       │ Selective    │ Comprehensive│
│ Example      │ Next.js API   │ NestJS       │ Microservices│
└─────────────────────────────────────────────────────────────┘
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
