---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/security/security-audit.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\security\security-audit.md
source_ext: .md
source_sha256: dabee9fd535af725cc20e525d37197110df81dd2a5b96c06560f5b5d8cca788b
text_sha256: 2aea97ad793f84ea5ba4fd9d4f3892d65f6f17bc2ba249f662eeee05df97b2b7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# security-audit.md

- Source: `claude-code-templates/cli-tool/components/commands/security/security-audit.md`
- Extract: `text`
- SHA256: `dabee9fd535af725cc20e525d37197110df81dd2a5b96c06560f5b5d8cca788b`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [focus-area] | --full
description: Perform comprehensive security assessment and vulnerability analysis
---

# Security Audit

Perform comprehensive security assessment: $ARGUMENTS

## Current Environment

- Dependency scan: !`npm audit --audit-level=moderate 2>/dev/null || pip check 2>/dev/null || echo "No package manager detected"`
- Environment files: @.env* (if exists)
- Security config: @.github/workflows/security.yml or @security/ (if exists)
- Recent commits: !`git log --oneline --grep="security\|fix" -10`

## Task

Perform systematic security audit following these steps:

1. **Environment Setup**
   - Identify the technology stack and framework
   - Check for existing security tools and configurations
   - Review deployment and infrastructure setup

2. **Dependency Security**
   - Scan all dependencies for known vulnerabilities
   - Check for outdated packages with security issues
   - Review dependency sources and integrity
   - Use appropriate tools: `npm audit`, `pip check`, `cargo audit`, etc.

3. **Authentication & Authorization**
   - Review authentication mechanisms and implementation
   - Check for proper session management
   - Verify authorization controls and access restrictions
   - Examine password policies and storage

4. **Input Validation & Sanitization**
   - Check all user input validation and sanitization
   - Look for SQL injection vulnerabilities
   - Identify potential XSS (Cross-Site Scripting) issues
   - Review file upload security and validation

5. **Data Protection**
   - Identify sensitive data handling practices
   - Check encryption implementation for data at rest and in transit
   - Review data masking and anonymization practices
   - Verify secure communication protocols (HTTPS, TLS)

6. **Secrets Management**
   - Scan for hardcoded secrets, API keys, and passwords
   - Check for proper secrets management practices
   - Review environment variable security
   - Identify exposed configuration files

7. **Error Handling & Logging**
   - Review error messages for information disclosure
   - Check logging practices for security events
   - Verify sensitive data is not logged
   - Assess error handling robustness

8. **Infrastructure Security**
   - Review containerization security (Docker, etc.)
   - Check CI/CD pipeline security
   - Examine cloud configuration and permissions
   - Assess network security configurations

9. **Security Headers & CORS**
   - Check security headers implementation
   - Review CORS configuration
   - Verify CSP (Content Security Policy) settings
   - Examine cookie security attributes

10. **Reporting**
    - Document all findings with severity levels (Critical, High, Medium, Low)
    - Provide specific remediation steps for each issue
    - Include code examples and file references
    - Create an executive summary with key recommendations

Use automated security scanning tools when available and provide manual review for complex security patterns.

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
