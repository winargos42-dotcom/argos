---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/setup-ci-cd-pipeline.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\setup-ci-cd-pipeline.md
source_ext: .md
source_sha256: 3dd3731d1b672c13c6bfcd892f8e0574a71ec6ec2d0eabf93de48e251d399bd9
text_sha256: 18759dc30e637027c62cd48a3f8b439ebbd636bae225e70447a06d97792e762b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-ci-cd-pipeline.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/setup-ci-cd-pipeline.md`
- Extract: `text`
- SHA256: `3dd3731d1b672c13c6bfcd892f8e0574a71ec6ec2d0eabf93de48e251d399bd9`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [platform] | --github-actions | --gitlab-ci | --azure-pipelines | --jenkins
description: Setup comprehensive CI/CD pipeline with automated testing, deployment, and monitoring
---

# Setup CI/CD Pipeline

Setup comprehensive CI/CD pipeline with automated workflows and deployments: **$ARGUMENTS**

## Current Repository State

- Version control: !`git remote -v | head -1` (GitHub, GitLab, etc.)
- Existing CI: !`find . -name ".github" -o -name ".gitlab-ci.yml" -o -name "azure-pipelines.yml" | wc -l`
- Test framework: @package.json or testing files detection
- Deployment config: @Dockerfile or deployment manifests

## Task

Implement production-ready CI/CD pipeline with comprehensive automation and best practices:

**Platform Choice**: Use $ARGUMENTS to specify GitHub Actions, GitLab CI, Azure Pipelines, or Jenkins

**Pipeline Architecture**:
1. **Build Automation** - Code compilation, dependency installation, artifact creation
2. **Testing Strategy** - Unit tests, integration tests, e2e tests, code coverage reporting
3. **Quality Gates** - Linting, security scanning, vulnerability assessment, code quality metrics
4. **Deployment Automation** - Staging deployment, production deployment, rollback mechanisms
5. **Environment Management** - Infrastructure provisioning, configuration management, secrets handling
6. **Monitoring Integration** - Performance monitoring, error tracking, deployment notifications

**Advanced Features**: Parallel job execution, matrix builds, deployment strategies (blue-green, canary), and multi-environment support.

**Security & Compliance**: Secure credential management, compliance checks, audit trails, and approval workflows.

**Output**: Complete CI/CD pipeline with automated testing, secure deployments, monitoring integration, and comprehensive documentation.

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
