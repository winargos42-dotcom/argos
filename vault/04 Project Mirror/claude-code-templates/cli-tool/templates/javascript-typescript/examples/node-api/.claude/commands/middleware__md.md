---
argos_import: project_file
source_path: claude-code-templates/cli-tool/templates/javascript-typescript/examples/node-api/.claude/commands/middleware.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\templates\javascript-typescript\examples\node-api\.claude\commands\middleware.md
source_ext: .md
source_sha256: bb635f79d761b90c4a658657e8a49f12a40794c41dcdc8811a08b7417fc4ac76
text_sha256: 2a7b7a3daaa414d518aed51160c4a0d89d065a2103f0d5b32c3f9546868a39af
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# middleware.md

- Source: `claude-code-templates/cli-tool/templates/javascript-typescript/examples/node-api/.claude/commands/middleware.md`
- Extract: `text`
- SHA256: `bb635f79d761b90c4a658657e8a49f12a40794c41dcdc8811a08b7417fc4ac76`

## Content

# Express Middleware

Create Express middleware for $ARGUMENTS following project conventions.

## Task

Create or optimize Express middleware based on the requirements:

1. **Analyze existing middleware**: Check current middleware patterns, naming conventions, and file organization
2. **Examine Express setup**: Review app configuration, middleware stack order, and TypeScript usage
3. **Identify middleware type**: Determine the middleware category:
   - Authentication/Authorization (JWT, sessions, role-based)
   - Validation (request body, params, query validation)
   - Logging (request/response logging, audit trails)
   - Error handling (global error handlers, custom errors)
   - Security (CORS, rate limiting, helmet)
   - Utility (parsing, compression, static files)
4. **Check dependencies**: Review existing middleware dependencies to avoid duplication
5. **Implement middleware**: Create middleware with proper TypeScript types and error handling
6. **Test middleware**: Write unit and integration tests following project patterns
7. **Update middleware stack**: Integrate middleware into Express app configuration
8. **Add documentation**: Include JSDoc comments and usage examples

## Implementation Requirements

- Follow project's TypeScript conventions and interfaces
- Use existing error handling patterns and response formats
- Include proper request/response typing with custom interfaces
- Add comprehensive error handling and logging
- Consider middleware execution order and dependencies
- Implement proper async/await patterns for async middleware
- Follow project's folder structure for middleware files

## Middleware Patterns to Consider

Based on the request:
- **Authentication**: JWT verification, session management, API key validation
- **Authorization**: Role-based access control, permission checking
- **Validation**: Schema validation with Joi/Zod, sanitization
- **Logging**: Request logging, performance monitoring, audit trails
- **Error Handling**: Global error handlers, custom error classes
- **Security**: CORS configuration, rate limiting, input sanitization
- **Utility**: Request parsing, response formatting, caching

## Integration Considerations

- **Middleware order**: Ensure proper execution sequence in Express app
- **Error propagation**: Handle errors correctly with next() function
- **Request enhancement**: Add properties to request object with proper typing
- **Response modification**: Modify response objects while maintaining type safety
- **Performance**: Consider middleware performance impact on request processing

## Important Notes

- ALWAYS examine existing middleware first to understand project patterns
- Use the same error handling and response format as existing middleware
- Follow project's folder structure for middleware (usually /middleware)
- Don't install new dependencies without asking
- Consider middleware performance and request processing impact
- Add proper TypeScript types for enhanced request/response objects
- Test middleware in isolation and integration contexts

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
