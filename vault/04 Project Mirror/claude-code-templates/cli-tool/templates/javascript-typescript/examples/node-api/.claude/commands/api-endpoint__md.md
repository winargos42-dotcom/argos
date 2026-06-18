---
argos_import: project_file
source_path: claude-code-templates/cli-tool/templates/javascript-typescript/examples/node-api/.claude/commands/api-endpoint.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\templates\javascript-typescript\examples\node-api\.claude\commands\api-endpoint.md
source_ext: .md
source_sha256: 0cbc8d3c9593c06509c977800b09656bd3109ef62933d486905c09f96705b30e
text_sha256: fa448b6d2da870badcaf0742746e471d449bca336a7b08b94300ee6e0d1bcd9a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# api-endpoint.md

- Source: `claude-code-templates/cli-tool/templates/javascript-typescript/examples/node-api/.claude/commands/api-endpoint.md`
- Extract: `text`
- SHA256: `0cbc8d3c9593c06509c977800b09656bd3109ef62933d486905c09f96705b30e`

## Content

# API Endpoint Generator

Generate a complete API endpoint for $ARGUMENTS following project conventions.

## Task

Create a new API endpoint with all necessary components:

1. **Analyze project architecture**: Examine existing API structure, patterns, and conventions
2. **Identify framework**: Determine if using Express, Fastify, NestJS, Next.js API routes, or other framework
3. **Check authentication**: Review existing auth patterns and middleware usage
4. **Examine data layer**: Identify database/ORM patterns (Prisma, TypeORM, Mongoose, etc.)
5. **Create endpoint structure**: Generate route, controller, validation, and service layers
6. **Implement business logic**: Add core functionality with proper error handling
7. **Add validation**: Include input validation using project's validation library
8. **Create tests**: Write unit and integration tests following project patterns
9. **Update documentation**: Add endpoint documentation (OpenAPI/Swagger if used)

## Implementation Requirements

- Follow project's TypeScript conventions and interfaces
- Use existing middleware patterns for auth, validation, logging
- Include proper HTTP status codes and error responses
- Add comprehensive input validation and sanitization
- Implement proper logging and monitoring
- Consider rate limiting and security headers
- Follow project's database transaction patterns

## Framework-Specific Patterns

I'll adapt to your project's framework:
- **Express**: Routes, controllers, middleware
- **Fastify**: Routes, handlers, schemas, plugins
- **NestJS**: Controllers, services, DTOs, guards
- **Next.js**: API routes with proper HTTP methods
- **tRPC**: Procedures with input/output validation
- **GraphQL**: Resolvers with proper type definitions

## Important Notes

- ALWAYS examine existing endpoints first to understand project patterns
- Use the same error handling and response format as existing endpoints
- Follow project's folder structure and naming conventions
- Don't install new dependencies without asking
- Consider backward compatibility if modifying existing endpoints
- Add proper database migrations if schema changes are needed

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
