---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/security/secrets-scanner.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\security\secrets-scanner.md
source_ext: .md
source_sha256: 8f9615a8ac92b43455049b350d8c95777431fddb46b7944ce2d86a0f212280cd
text_sha256: 86e24eefaefa16396712ba7c3103a4831969109dc7fe3623af1774d186e87108
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# secrets-scanner.md

- Source: `claude-code-templates/cli-tool/components/commands/security/secrets-scanner.md`
- Extract: `text`
- SHA256: `8f9615a8ac92b43455049b350d8c95777431fddb46b7944ce2d86a0f212280cd`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [scope] | --api-keys | --passwords | --certificates | --fix
description: Scan codebase for exposed secrets, credentials, and sensitive information
---

# Secrets Scanner

Scan codebase for exposed secrets and sensitive information: **$ARGUMENTS**

## Current Repository State

- Git status: !`git status --porcelain | wc -l` uncommitted files
- File types: !`find . -name "*.js" -o -name "*.py" -o -name "*.env*" -o -name "*.yml" | wc -l` scannables
- Recent commits: !`git log --oneline --grep="password\|key\|secret\|token" -5`
- Environment files: @.env* or @config/* (if exists)

## Task

Perform comprehensive secrets detection and remediation across codebase:

**Scan Scope**: Use $ARGUMENTS to focus on API keys, passwords, certificates, or complete scan

**Detection Categories**:
1. **API Keys & Tokens** - GitHub, AWS, Google Cloud, Stripe, third-party services
2. **Database Credentials** - Connection strings, usernames, passwords
3. **Certificates & Keys** - Private keys, SSH keys, SSL certificates
4. **Authentication Secrets** - JWT secrets, session keys, OAuth credentials
5. **Configuration Leaks** - Hardcoded URLs, internal endpoints, debug settings

**Remediation Actions**:
- Identify exposed secrets with file locations and line numbers
- Provide secure alternatives (environment variables, secret management)
- Generate .gitignore entries for sensitive files
- Create secure configuration templates
- Implement secrets management best practices

**Output**: Detailed security report with risk levels, immediate actions, and long-term security improvements.

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
