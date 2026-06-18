---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/security/add-authentication-system.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\security\add-authentication-system.md
source_ext: .md
source_sha256: 9c40c7989f464a3c6686e798a343da704c918eb43c47a8562618f4219af43b04
text_sha256: 4f8a4f05f419f8ae6ec7bf07078658c3c0951a5dcde48868daaa44fc6dba319b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# add-authentication-system.md

- Source: `claude-code-templates/cli-tool/components/commands/security/add-authentication-system.md`
- Extract: `text`
- SHA256: `9c40c7989f464a3c6686e798a343da704c918eb43c47a8562618f4219af43b04`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [auth-method] | --oauth | --jwt | --mfa | --passwordless
description: Implement secure user authentication system with chosen method and security best practices
---

# Add Authentication System

Implement secure user authentication system: **$ARGUMENTS**

## Current Application State

- Framework detection: @package.json or @requirements.txt or @Cargo.toml
- Existing auth: !`grep -r "auth\|login\|jwt\|session" src/ --include="*.js" --include="*.py" --include="*.rs" | wc -l`
- Security config: @.env* (check for auth-related variables)
- Database setup: Check for user models or auth tables

## Task

Implement comprehensive authentication system with security best practices:

**Authentication Methods**: Choose from username/password, OAuth 2.0, JWT, SAML, MFA, or passwordless based on $ARGUMENTS

**Implementation Areas**:
1. **User Management** - Registration, profiles, password policies, account verification
2. **Authentication Flow** - Login/logout, session management, token handling, middleware
3. **Authorization System** - RBAC, permissions, route protection, API security
4. **Security Hardening** - Password hashing, rate limiting, CSRF protection, secure cookies
5. **Integration** - Frontend components, API endpoints, database models, middleware

**Security Standards**: Implement OWASP authentication guidelines, secure session management, and proper error handling.

**Output**: Production-ready authentication system with comprehensive security controls and user-friendly interface.

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
