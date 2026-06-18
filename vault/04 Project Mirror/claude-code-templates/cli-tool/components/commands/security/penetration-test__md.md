---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/security/penetration-test.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\security\penetration-test.md
source_ext: .md
source_sha256: aa8f730c9c1f94a588b80da7696d5965e9e164af74bd9c14127510c73d7b8418
text_sha256: 176fc5e1d8b742ae258ef849616ac5b32467065a47720242e7e6e7cedcf300fb
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# penetration-test.md

- Source: `claude-code-templates/cli-tool/components/commands/security/penetration-test.md`
- Extract: `text`
- SHA256: `aa8f730c9c1f94a588b80da7696d5965e9e164af74bd9c14127510c73d7b8418`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [target] | --web-app | --api | --auth | --full-scan
description: Perform penetration testing and vulnerability assessment on application
---

# Penetration Test

Perform penetration testing and vulnerability assessment: **$ARGUMENTS**

## Application Context

- Running services: !`netstat -tlnp 2>/dev/null | grep LISTEN | head -10 || lsof -i -P | grep LISTEN | head -10`
- Web framework: @package.json or @requirements.txt (detect framework and version)
- API endpoints: !`grep -r "route\|endpoint\|@app\\.route\|@RequestMapping" src/ 2>/dev/null | wc -l`
- Authentication: !`grep -r "auth\|login\|jwt\|session" src/ 2>/dev/null | wc -l`

## Task

Conduct systematic penetration testing following ethical hacking methodologies:

**Test Target**: Use $ARGUMENTS to focus on web application, API, authentication, or comprehensive testing

**Testing Phases**:
1. **Reconnaissance** - Service discovery, technology fingerprinting, attack surface mapping
2. **Vulnerability Assessment** - OWASP Top 10, injection flaws, broken authentication
3. **Exploitation Testing** - XSS, CSRF, SQL injection, privilege escalation attempts
4. **Authentication Testing** - Brute force, session management, authorization bypasses
5. **API Security Testing** - Input validation, rate limiting, authentication bypass
6. **Infrastructure Testing** - Network security, container security, configuration issues

**Testing Methodology**:
- Follow OWASP Testing Guide and NIST guidelines
- Use both automated tools and manual testing techniques
- Document all findings with proof-of-concept examples
- Provide remediation recommendations for each vulnerability
- Maintain ethical boundaries and avoid data damage

**Output**: Comprehensive penetration test report with executive summary, detailed findings, risk ratings, and remediation roadmap.

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
