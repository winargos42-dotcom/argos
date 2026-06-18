---
argos_import: project_file
source_path: claude-code-templates/docu/docs/components/commands.md
source_abs: F:\debug\argoss\claude-code-templates\docu\docs\components\commands.md
source_ext: .md
source_sha256: e5a3fd5eb7547a63cbb491f8325523a12cf101a5b0bd73d466e4a08041a9c5b9
text_sha256: 8ec5a70e7b914d435bea42326509ca1fad7b6c65b50f2bbe7069a2eafe32b13b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:55
---

# commands.md

- Source: `claude-code-templates/docu/docs/components/commands.md`
- Extract: `text`
- SHA256: `e5a3fd5eb7547a63cbb491f8325523a12cf101a5b0bd73d466e4a08041a9c5b9`

## Content

---
sidebar_position: 3
---

# Commands

Custom slash commands that automate development workflows. Browse and install from **[aitmpl.com](https://aitmpl.com)**.

## ⚡ What are Commands?

Commands are custom slash commands for Claude Code that automate common development tasks. Type `/command-name` in Claude Code to execute them.

## Installation

### 📦 Basic Installation
Install this component locally in your project. Works with your existing Claude Code setup.

```bash
npx claude-code-templates@latest --command testing/generate-tests --yes
```

### Multiple Commands
```bash
npx claude-code-templates@latest --command setup/setup-testing,performance/optimize-bundle --yes
```

## 💡 Usage After Installation

Once installed, use commands in Claude Code:
```
/generate-tests
/optimize-bundle
/security-audit
/setup-testing
```

## 📁 Command Categories

Browse commands by workflow area to find the right automation for your needs:

### Setup & Configuration
Project initialization and foundation setup. Examples: `setup-ci-cd-pipeline` for automated builds, `setup-testing` for test frameworks, `migrate-to-typescript` for type safety.

### Testing
Test automation and quality assurance workflows. Examples: `generate-tests` for automatic test creation, `setup-e2e` for end-to-end testing, `test-coverage` for coverage analysis.

### Performance
Optimization and performance analysis tools. Examples: `optimize-bundle` for build optimization, `performance-audit` for speed analysis, `add-caching` for performance improvements.

### Database
Database operations and management automation. Examples: `supabase-migration-assistant` for schema changes, `supabase-security-audit` for database security, `supabase-type-generator` for TypeScript types.

### Documentation
Documentation generation and maintenance tools. Examples: `generate-api-docs` for API documentation, `update-readme` for project documentation, `create-guide` for user guides.

### Security
Security analysis and hardening automation. Examples: `security-audit` for vulnerability scanning, `dependency-audit` for package security, `fix-vulnerabilities` for security patches.

## 🎯 How to Choose Commands

Select commands based on your current workflow needs:

### By Development Phase
- **Project Start**: Begin with `setup/*` commands for foundation setup
- **Development**: Use `testing/*` and `documentation/*` for quality workflows
- **Pre-launch**: Add `security/*` and `performance/*` for optimization
- **Maintenance**: Focus on `database/*` and `performance/*` for ongoing operations

### By Technology Stack
- **Supabase projects**: Choose `database/supabase-*` commands for database management
- **React applications**: Use `performance/optimize-bundle` for build optimization
- **API projects**: Select `documentation/generate-api-docs` for API documentation
- **Any project**: Start with `setup/setup-testing` for quality foundation

### By Current Challenges
- **Slow builds**: Use `performance/optimize-bundle` for build optimization
- **Missing tests**: Choose `testing/generate-tests` for test automation
- **Security concerns**: Select `security/security-audit` for vulnerability assessment
- **Poor documentation**: Pick `documentation/update-readme` for documentation improvements

## 🔧 Pro Tips

- **Install setup commands first** for new projects
- **Use testing commands early** in development
- **Add security commands** before deployment
- **Browse [aitmpl.com](https://aitmpl.com)** for specific workflows

---

**Find more commands:** [Browse all commands on aitmpl.com](https://aitmpl.com) → Filter by "Commands"

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
