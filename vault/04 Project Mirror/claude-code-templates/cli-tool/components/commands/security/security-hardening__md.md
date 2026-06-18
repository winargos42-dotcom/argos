---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/security/security-hardening.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\security\security-hardening.md
source_ext: .md
source_sha256: f4c70cb960bb98283eecb5b2b425afdf55a267169ef9943dadfcf10fd48f100d
text_sha256: 38f60ca096115d9305fd71281d9338f5b7685ebd107886726ae72c8981c82040
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# security-hardening.md

- Source: `claude-code-templates/cli-tool/components/commands/security/security-hardening.md`
- Extract: `text`
- SHA256: `f4c70cb960bb98283eecb5b2b425afdf55a267169ef9943dadfcf10fd48f100d`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [focus-area] | --headers | --auth | --encryption | --infrastructure
description: Harden application security configuration with comprehensive security controls
---

# Security Hardening

Harden application security configuration and controls: **$ARGUMENTS**

## Current Security Posture

- Framework: @package.json or @requirements.txt or @Cargo.toml (detect framework)
- Security headers: !`curl -I http://localhost:3000 2>/dev/null | grep -i 'x-\|content-security\|strict-transport' || echo "No server running"`
- Environment config: @.env* (check for security-related variables)
- Dependencies: !`npm audit --audit-level=moderate 2>/dev/null || echo "Run dependency audit first"`

## Task

Implement comprehensive security hardening based on security best practices:

**Hardening Focus**: Use $ARGUMENTS to target specific areas or apply comprehensive hardening

**Security Controls**:
1. **Authentication & Authorization** - MFA, RBAC, session security, password policies
2. **Input Validation** - XSS prevention, SQL injection protection, CSRF tokens
3. **Secure Communication** - HTTPS/TLS, HSTS, certificate management
4. **Data Protection** - Encryption at rest/transit, key management, secure storage
5. **Security Headers** - CSP, CORS, security response headers
6. **Infrastructure Security** - Container hardening, network segmentation, monitoring

**Output**: Hardened application with comprehensive security controls, proper configuration, and monitoring capabilities.

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
