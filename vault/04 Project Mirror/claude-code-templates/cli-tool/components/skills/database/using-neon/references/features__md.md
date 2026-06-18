---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/using-neon/references/features.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\using-neon\references\features.md
source_ext: .md
source_sha256: 011d8563535a9abea0283e34289b3ba5f1f2b391249077870a43e56e5d100678
text_sha256: 0cff45a98336cb47393fb77f86b2dcfe0745fdab0ea89c311c29e2cead7eab16
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# features.md

- Source: `claude-code-templates/cli-tool/components/skills/database/using-neon/references/features.md`
- Extract: `text`
- SHA256: `011d8563535a9abea0283e34289b3ba5f1f2b391249077870a43e56e5d100678`

## Content

# Neon Features

Overview of Neon's key platform features. For detailed information, fetch the official docs.

## Branching

Create instant, copy-on-write clones of your database at any point in time. Branches are isolated environments perfect for development, testing, and preview deployments.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction/branching
```

**Key Points:**

- Branches are instant (no data copying)
- Copy-on-write means branches only store changes from parent
- Use for: dev environments, staging, testing, preview deployments
- Branches can have their own compute endpoint

**Use Cases:**

| Use Case            | Description                                 |
| ------------------- | ------------------------------------------- |
| Development         | Each developer gets isolated branch         |
| Preview Deployments | Branch per PR/preview URL                   |
| Testing             | Reset test data by recreating branch        |
| Schema Migrations   | Test migrations on branch before production |

If the Neon MCP server is available, you can use it to list and create branches. Otherwise, refer to the Neon CLI or Platform API.

## Autoscaling

Neon automatically scales compute resources based on workload demand.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction/autoscaling
```

**Key Points:**

- Scales between min and max compute units (CUs)
- Responds to CPU and memory pressure
- No manual intervention required
- Configure limits per project or endpoint

## Scale to Zero

Databases automatically suspend after a period of inactivity, reducing costs to storage-only.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction/scale-to-zero
```

**Key Points:**

- Default suspend after 5 minutes of inactivity (configurable)
- First query after suspend has ~500ms cold start
- Storage is always maintained
- Perfect for dev/staging environments with intermittent use

## Instant Restore

Restore your database to any point within your retention window without backups.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction/branch-restore
```

**Key Points:**

- Point-in-time recovery without pre-configured backups
- Restore window depends on plan (7-30 days)
- Create branches from any point in history
- Time Travel queries to view historical data

## Read Replicas

Create read-only compute endpoints to scale read workloads.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction/read-replicas
```

**Key Points:**

- Read replicas share storage with primary (no data duplication)
- Instant creation
- Independent scaling from primary
- Use for: analytics, reporting, read-heavy workloads

## Connection Pooling

Built-in connection pooling via PgBouncer for efficient connection management.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/connect/connection-pooling
```

**Key Points:**

- Enabled by adding `-pooler` to endpoint hostname
- Transaction mode by default
- Supports up to 10,000 concurrent connections
- Essential for serverless environments

## IP Allow Lists

Restrict database access to specific IP addresses or ranges.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/introduction/ip-allow
```

## Logical Replication

Replicate data to/from external Postgres databases.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/guides/logical-replication-guide
```

## Neon Auth

Managed authentication that branches with your database.

```bash
curl -H "Accept: text/markdown" https://neon.tech/docs/auth/overview
```

**Key Points:**

- Sign-in/sign-up with email, social providers (Google, GitHub)
- Session management
- UI components included
- Branches with your database

For setup, see `neon-auth.md`. For auth + data API, see `neon-js.md`.

## Feature Documentation Reference

| Feature             | Documentation                                           | Resource       |
| ------------------- | ------------------------------------------------------- | -------------- |
| Branching           | https://neon.tech/docs/introduction/branching           | -              |
| Autoscaling         | https://neon.tech/docs/introduction/autoscaling         | -              |
| Scale to Zero       | https://neon.tech/docs/introduction/scale-to-zero       | -              |
| Instant Restore     | https://neon.tech/docs/introduction/branch-restore      | -              |
| Read Replicas       | https://neon.tech/docs/introduction/read-replicas       | -              |
| Connection Pooling  | https://neon.tech/docs/connect/connection-pooling       | -              |
| IP Allow            | https://neon.tech/docs/introduction/ip-allow            | -              |
| Logical Replication | https://neon.tech/docs/guides/logical-replication-guide | -              |
| Neon Auth           | https://neon.tech/docs/auth/overview                    | `neon-auth.md` |
| Data API            | https://neon.tech/docs/data-api/overview                | `neon-js.md`   |

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
