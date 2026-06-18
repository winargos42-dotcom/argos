---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/crafting-effective-readmes/templates/internal.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\crafting-effective-readmes\templates\internal.md
source_ext: .md
source_sha256: 7cf46108143977e07c5d9ac56a2eccb907f46131361de1f2f8ffac7bdd2016a7
text_sha256: 6d2d0ac208385fa97f5753608f3a941411f40daaa1901fb60021d29ed24c6ff0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# internal.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/crafting-effective-readmes/templates/internal.md`
- Extract: `text`
- SHA256: `7cf46108143977e07c5d9ac56a2eccb907f46131361de1f2f8ffac7bdd2016a7`

## Content

# Internal/Work Project README Template

Use this template for team codebases, services, and internal tools.
Focus on onboarding new team members and operational knowledge.

---

# [Service/Project Name]

[One-line description of what this service does]

**Team**: [Team name or slack channel]  
**On-call**: [Rotation or contact info]

## Overview

[2-3 sentences on what this does, why it exists, and where it fits in the system architecture.]

### Dependencies

- **Upstream**: [Services this depends on]
- **Downstream**: [Services that depend on this]

## Local Development Setup

### Prerequisites

- [Required tool 1 with version]
- [Required tool 2]
- Access to [internal system/VPN/etc]

### Environment Variables

| Variable | Description | Where to get it |
|----------|-------------|-----------------|
| `DATABASE_URL` | [Description] | [1Password/Vault/etc] |
| `API_KEY` | [Description] | [Where to find] |

### Running Locally

```bash
[Step-by-step commands to get running]
```

### Running Tests

```bash
[Test commands]
```

## Architecture

[Brief description of system design. Link to architecture diagrams if they exist.]

```
[Simple ASCII diagram if helpful]
```

### Key Files

| Path | Purpose |
|------|---------|
| `src/[important-file]` | [What it does] |
| `config/` | [Configuration files] |

## Deployment

[How to deploy, or link to deployment docs]

### Environments

| Environment | URL | Notes |
|-------------|-----|-------|
| Development | [URL] | [Notes] |
| Staging | [URL] | [Notes] |
| Production | [URL] | [Notes] |

## Runbooks

### [Common Task 1]

```bash
[Commands or steps]
```

### [Common Task 2]

[Steps]

## Troubleshooting

### [Common Problem 1]

**Symptom**: [What you see]  
**Cause**: [Why it happens]  
**Fix**: [How to resolve]

## Contributing

[Link to team contribution guidelines or PR process]

## Related Docs

- [Link to design doc]
- [Link to API docs]
- [Link to monitoring dashboard]

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
