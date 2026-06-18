---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/testing/test-changelog-automation.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\testing\test-changelog-automation.md
source_ext: .md
source_sha256: 25d9b669c3a7ecd7661ce03ddc93094a06118bdcc6448723e2114f6c67662410
text_sha256: ecc64d26109a4c64aa1d927a4aef200ccdc19d899699b8591ff4841acfef585f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# test-changelog-automation.md

- Source: `claude-code-templates/cli-tool/components/commands/testing/test-changelog-automation.md`
- Extract: `text`
- SHA256: `25d9b669c3a7ecd7661ce03ddc93094a06118bdcc6448723e2114f6c67662410`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [automation-type] | --changelog | --workflow-demo | --ci-integration | --validation
description: Automate changelog testing workflow with CI integration and validation
---

# Test Changelog Automation

Automate changelog testing workflow with comprehensive CI integration: **$ARGUMENTS**

## Current Automation Context

- Changelog files: !`find . -name "CHANGELOG*" -o -name "changelog*" | head -1 || echo "No changelog detected"`
- CI system: !`find . -name ".github" -o -name ".gitlab-ci.yml" -o -name "Jenkinsfile" | head -1 || echo "No CI detected"`
- Version control: !`git status >/dev/null 2>&1 && echo "Git repository" || echo "No git repository"`
- Release process: Analysis of existing release automation and versioning

## Task

Implement comprehensive changelog automation with testing and validation workflows:

**Automation Type**: Use $ARGUMENTS to focus on changelog automation, workflow demonstration, CI integration, or validation testing

**Changelog Automation Framework**:

1. **Automation Setup** - Configure changelog generation, setup version control integration, implement automated updates, design validation rules
2. **Workflow Integration** - Design CI/CD integration, configure automated triggers, implement validation checks, optimize execution performance
3. **Testing Strategy** - Create changelog validation tests, implement format verification, design content validation, setup regression testing
4. **Quality Assurance** - Configure automated formatting, implement consistency checks, setup content validation, optimize maintenance workflows
5. **Validation Framework** - Design automated validation rules, implement compliance checking, configure error reporting, optimize feedback loops
6. **CI Integration** - Setup automated execution, configure deployment triggers, implement notification systems, optimize pipeline performance

**Advanced Features**: Automated release note generation, semantic versioning integration, automated documentation updates, compliance validation.

**Quality Metrics**: Changelog accuracy, automation reliability, validation effectiveness, maintenance efficiency.

**Output**: Complete changelog automation with testing workflows, CI integration, validation rules, and maintenance procedures.

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
