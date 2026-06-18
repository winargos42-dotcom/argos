---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/using-neon/references/what-is-neon.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\using-neon\references\what-is-neon.md
source_ext: .md
source_sha256: aca5d223573ebb859953d4c72ae57e2c666816a55da2ede05a6cca94a939b826
text_sha256: eda6c2651ef797ae0182767e975d5139e24ed341dba26e1b8b46dab5664ddeda
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# what-is-neon.md

- Source: `claude-code-templates/cli-tool/components/skills/database/using-neon/references/what-is-neon.md`
- Extract: `text`
- SHA256: `aca5d223573ebb859953d4c72ae57e2c666816a55da2ede05a6cca94a939b826`

## Content

# What is Neon

Neon is a serverless Postgres platform designed to help you build reliable and scalable applications faster. It separates compute and storage to offer modern developer features such as autoscaling, branching, instant restore, and scale-to-zero.

For the full introduction, fetch the official docs:

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction
```

## Core Concepts

Understanding Neon's resource hierarchy is essential for working with the platform effectively.

| Concept          | Description                                                           | Key Relationship          |
| ---------------- | --------------------------------------------------------------------- | ------------------------- |
| Organization     | Highest-level container for billing, users, and projects              | Contains Projects         |
| Project          | Primary container for all database resources for an application       | Contains Branches         |
| Branch           | Lightweight, copy-on-write clone of database state                    | Contains Databases, Roles |
| Compute Endpoint | Running PostgreSQL instance (CPU/RAM for queries)                     | Attached to a Branch      |
| Database         | Logical container for data (tables, schemas, views)                   | Exists within a Branch    |
| Role             | PostgreSQL role for authentication and authorization                  | Belongs to a Branch       |
| Operation        | Async action by the control plane (creating branch, starting compute) | Associated with Project   |

## Key Differentiators

1. **Serverless Architecture**: Compute scales automatically and can suspend when idle
2. **Branching**: Create instant database copies without duplicating storage
3. **Separation of Compute and Storage**: Pay for compute only when active
4. **Postgres Compatible**: Works with any Postgres driver, ORM, or tool

## Documentation Resources

| Topic                  | Documentation URL                                         |
| ---------------------- | --------------------------------------------------------- |
| Introduction           | https://neon.tech/docs/introduction                       |
| Architecture           | https://neon.tech/docs/introduction/architecture-overview |
| Plans & Billing        | https://neon.tech/docs/introduction/about-billing         |
| Regions                | https://neon.tech/docs/introduction/regions               |
| Postgres Compatibility | https://neon.tech/docs/reference/compatibility            |

```bash
# Fetch architecture docs
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction/architecture-overview

# Fetch plans and billing
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction/about-billing
```

## When to Use Neon

Neon is ideal for:

- **Serverless applications**: Functions that need database access without managing connections
- **Development workflows**: Branch databases like code for isolated testing
- **Variable workloads**: Auto-scale during traffic spikes, scale to zero when idle
- **Cost optimization**: Pay only for active compute time and storage used

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
