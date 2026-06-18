---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/design-rest-api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\design-rest-api.md
source_ext: .md
source_sha256: 8d720f7bdc4ff16afd2ed0a60c22d64c2d2dcd3b8d843947d071deef7e0ac13d
text_sha256: ece42a17bc62825d97b1e8a3dc562abd5b4eebba939aa18c8f23f005e5ee3cde
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# design-rest-api.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/design-rest-api.md`
- Extract: `text`
- SHA256: `8d720f7bdc4ff16afd2ed0a60c22d64c2d2dcd3b8d843947d071deef7e0ac13d`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [api-version] | --v1 | --v2 | --graphql-hybrid | --openapi
description: Design RESTful API architecture with comprehensive endpoints, authentication, and documentation
---

# Design REST API

Design comprehensive RESTful API architecture: **$ARGUMENTS**

## Current Application State

- Framework detection: @package.json or @requirements.txt (Express, FastAPI, Spring Boot, etc.)
- Existing API: !`grep -r "route\|endpoint\|@app\\.route" src/ 2>/dev/null | wc -l` routes found
- Authentication: !`grep -r "auth\|jwt\|session" src/ 2>/dev/null | wc -l` auth components
- Documentation: @swagger.yaml or @openapi.json (if exists)

## Task

Design complete RESTful API with industry best practices and comprehensive functionality:

**API Version**: Use $ARGUMENTS to specify API version, GraphQL hybrid approach, or OpenAPI specification

**API Architecture**:
1. **Resource Design** - RESTful endpoints, HTTP methods, URL structure, resource relationships
2. **Request/Response Models** - Data validation, serialization, error handling, status codes
3. **Authentication & Authorization** - JWT, OAuth, RBAC, API keys, rate limiting
4. **API Documentation** - OpenAPI/Swagger specs, interactive documentation, code examples
5. **Versioning Strategy** - URL, header, or content-type based versioning
6. **Performance & Security** - Caching, pagination, CORS, input validation, SQL injection prevention

**Advanced Features**: Real-time capabilities, file uploads, batch operations, webhooks, and monitoring integration.

**Standards Compliance**: Follow REST principles, HTTP specifications, and API design best practices.

**Output**: Complete API specification with endpoints, authentication, validation, documentation, and client SDKs.

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
