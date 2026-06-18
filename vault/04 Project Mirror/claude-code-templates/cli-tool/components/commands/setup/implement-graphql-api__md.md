---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/implement-graphql-api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\implement-graphql-api.md
source_ext: .md
source_sha256: 9a6ef99aa9de563417c61ef195293defb3cfe6f39eab2cc5df1236723c389e10
text_sha256: acc19993bdc4c16f912b48556986d0df224df1f522171308929a7c4671434d39
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# implement-graphql-api.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/implement-graphql-api.md`
- Extract: `text`
- SHA256: `9a6ef99aa9de563417c61ef195293defb3cfe6f39eab2cc5df1236723c389e10`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [schema-approach] | --schema-first | --code-first | --federation
description: Implement GraphQL API with comprehensive schema, resolvers, and real-time subscriptions
---

# Implement GraphQL API

Implement comprehensive GraphQL API with modern best practices: **$ARGUMENTS**

## Current Application Context

- Framework: @package.json or @requirements.txt (detect Apollo, GraphQL Yoga, etc.)
- Existing API: !`find . -name "*.graphql" -o -name "*schema*" -o -name "*resolver*" | wc -l`
- Database integration: @prisma/schema.prisma or database connection configs
- Authentication: !`grep -r "auth\|jwt\|context" src/ 2>/dev/null | wc -l`

## Task

Build production-ready GraphQL API with comprehensive functionality and performance optimization:

**Schema Approach**: Use $ARGUMENTS to specify schema-first, code-first, or federation architecture

**GraphQL Implementation**:
1. **Schema Design** - Type definitions, queries, mutations, subscriptions, custom scalars
2. **Resolver Architecture** - Data fetching, authentication, authorization, error handling
3. **DataLoader Integration** - N+1 query prevention, batch loading, caching strategies
4. **Real-time Features** - WebSocket subscriptions, live data updates, connection management
5. **Security & Performance** - Query complexity analysis, depth limiting, rate limiting
6. **Development Tools** - GraphQL Playground, introspection, schema stitching

**Advanced Features**: File uploads, federated schemas, Apollo Federation, schema directives, and monitoring.

**Production Readiness**: Implement comprehensive error handling, logging, metrics, and deployment strategies.

**Output**: Complete GraphQL API with optimized resolvers, real-time capabilities, security controls, and developer documentation.

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
