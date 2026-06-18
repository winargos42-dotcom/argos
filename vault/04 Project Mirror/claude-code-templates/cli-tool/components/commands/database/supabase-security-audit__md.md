---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/database/supabase-security-audit.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\database\supabase-security-audit.md
source_ext: .md
source_sha256: 5607bbd1191399803d768f47c1bf0aa50113bc0124a4222358a8ddb2fbd21009
text_sha256: 3caced0d17dab185055c2ba2315b2f3a5d9cc83bc46b49a37f68d40108a666d8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# supabase-security-audit.md

- Source: `claude-code-templates/cli-tool/components/commands/database/supabase-security-audit.md`
- Extract: `text`
- SHA256: `5607bbd1191399803d768f47c1bf0aa50113bc0124a4222358a8ddb2fbd21009`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [audit-scope] | --rls | --permissions | --auth | --api-keys | --comprehensive
description: Conduct comprehensive Supabase security audit with RLS analysis and vulnerability assessment
---

# Supabase Security Audit

Conduct comprehensive Supabase security audit with RLS policy analysis and vulnerability assessment: **$ARGUMENTS**

## Current Security Context

- Supabase access: MCP integration for security analysis and policy review
- RLS policies: Current Row Level Security implementation and policy effectiveness
- Auth configuration: !`find . -name "*auth*" -o -name "*supabase*" | grep -E "\\.(js|ts|json)$" | head -5` authentication setup
- API security: Current API key management and access control implementation

## Task

Execute comprehensive security audit with vulnerability assessment and policy optimization:

**Audit Scope**: Use $ARGUMENTS to focus on RLS policies, permission analysis, authentication security, API key management, or comprehensive security review

**Security Audit Framework**:
1. **RLS Policy Analysis** - Review Row Level Security policies, test policy effectiveness, identify policy gaps, optimize policy performance
2. **Permission Assessment** - Analyze table permissions, review role-based access, validate permission hierarchies, identify over-privileged access
3. **Authentication Security** - Review auth configuration, analyze JWT security, validate session management, assess multi-factor authentication
4. **API Key Management** - Audit API key usage, review key rotation policies, validate key scoping, assess exposure risks
5. **Data Protection** - Analyze sensitive data handling, review encryption implementation, validate data masking, assess backup security
6. **Vulnerability Scanning** - Identify security vulnerabilities, assess injection risks, review CORS configuration, validate rate limiting

**Advanced Features**: Automated security testing, policy simulation, vulnerability scoring, compliance checking, security monitoring setup.

**Compliance Integration**: GDPR compliance checking, SOC2 requirements validation, security best practices enforcement, audit trail analysis.

**Output**: Comprehensive security audit report with vulnerability assessments, policy recommendations, security improvements, and compliance validation.

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
