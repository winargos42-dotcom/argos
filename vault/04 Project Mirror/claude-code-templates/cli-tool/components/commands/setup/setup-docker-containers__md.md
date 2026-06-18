---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/setup-docker-containers.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\setup-docker-containers.md
source_ext: .md
source_sha256: 975a9bfe293e5d24a1cdac8270031f97ae2ec32a8f7377610e1bbc5f273d5ed3
text_sha256: dbcd5a8946b7deefb0d72dab4a23af9ca9976ba899f1db9b6e9b8b1db9f9fc9c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-docker-containers.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/setup-docker-containers.md`
- Extract: `text`
- SHA256: `975a9bfe293e5d24a1cdac8270031f97ae2ec32a8f7377610e1bbc5f273d5ed3`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [environment-type] | --development | --production | --microservices | --compose
description: Setup Docker containerization with multi-stage builds and development workflows
---

# Setup Docker Containers

Setup comprehensive Docker containerization for development and production: **$ARGUMENTS**

## Current Project State

- Application type: @package.json or @requirements.txt (detect Node.js, Python, etc.)
- Existing Docker: @Dockerfile or @docker-compose.yml (if exists)
- Dependencies: !`find . -name "package-lock.json" -o -name "poetry.lock" -o -name "Pipfile.lock" | wc -l`
- Services needed: Database, cache, message queue detection from configs

## Task

Implement production-ready Docker containerization with optimized builds and development workflows:

**Environment Type**: Use $ARGUMENTS to specify development, production, microservices, or Docker Compose setup

**Containerization Strategy**:
1. **Dockerfile Creation** - Multi-stage builds, layer optimization, security best practices
2. **Development Workflow** - Hot reloading, volume mounts, debugging capabilities
3. **Production Optimization** - Image size reduction, security scanning, health checks
4. **Multi-Service Setup** - Docker Compose, service discovery, networking configuration
5. **CI/CD Integration** - Build automation, registry management, deployment pipelines
6. **Monitoring & Logs** - Container observability, log aggregation, resource monitoring

**Security Features**: Non-root users, minimal base images, vulnerability scanning, secrets management.

**Performance Optimization**: Layer caching, build contexts, multi-platform builds, and resource constraints.

**Output**: Complete Docker setup with optimized containers, development workflows, production deployment, and comprehensive documentation.

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
