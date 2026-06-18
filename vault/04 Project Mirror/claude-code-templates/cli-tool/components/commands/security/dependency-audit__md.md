---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/security/dependency-audit.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\security\dependency-audit.md
source_ext: .md
source_sha256: d679c2cdd0b1c80c1ceb366a45aa8b546fd102935dbd6851c495539affbcdccf
text_sha256: 103b7781bd907150713a839207ca6112a94cd60fb2aafa154a68754491ada621
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# dependency-audit.md

- Source: `claude-code-templates/cli-tool/components/commands/security/dependency-audit.md`
- Extract: `text`
- SHA256: `d679c2cdd0b1c80c1ceb366a45aa8b546fd102935dbd6851c495539affbcdccf`

## Content

---
allowed-tools: Read, Bash, Grep
argument-hint: [scope] | --security | --licenses | --updates | --all
description: Audit dependencies for security vulnerabilities, license compliance, and update recommendations
---

# Dependency Audit

Audit dependencies for security vulnerabilities and compliance: **$ARGUMENTS**

## Current Dependencies

- Package files: @package.json or @requirements.txt or @Cargo.toml or @pom.xml
- Lock files: @package-lock.json or @poetry.lock or @Cargo.lock
- Security scan: !`npm audit --audit-level=moderate 2>/dev/null || pip check 2>/dev/null || cargo audit 2>/dev/null || echo "No security scanner available"`
- Outdated packages: !`npm outdated 2>/dev/null || pip list --outdated 2>/dev/null || echo "Check manually"`

## Task

Perform comprehensive dependency security and compliance audit:

**Audit Scope**: Use $ARGUMENTS to focus on security, licenses, updates, or complete audit

**Analysis Areas**:
1. **Vulnerability Scanning** - Known CVEs, security advisories, exploit availability
2. **Version Analysis** - Outdated packages, breaking changes, update recommendations
3. **License Compliance** - License compatibility, restrictions, legal obligations
4. **Supply Chain Security** - Package authenticity, maintainer status, suspicious dependencies
5. **Performance Impact** - Bundle size, unused dependencies, optimization opportunities

**Output**: Prioritized security report with critical vulnerabilities, recommended actions, and compliance status.

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
