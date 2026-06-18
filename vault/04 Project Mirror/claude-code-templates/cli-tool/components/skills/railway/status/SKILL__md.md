---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/railway/status/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\railway\status\SKILL.md
source_ext: .md
source_sha256: 8bf7f9e1a3e67083ac966ac278f36aae22fadc1a1c95f93f3d857cd7a03b5c60
text_sha256: 6c07b8cf8e82d763eebf4ef4beb8404cbd52c5defbbecf965b6ec64298306d3d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/railway/status/SKILL.md`
- Extract: `text`
- SHA256: `8bf7f9e1a3e67083ac966ac278f36aae22fadc1a1c95f93f3d857cd7a03b5c60`

## Content

---
name: railway-status
description: Check current Railway project status for this directory. Use when user asks "railway status", "is it running", "what's deployed", "deployment status", or about uptime. NOT for variables or configuration queries - use railway-environment skill for those.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Status, Project, Environment, Deployment, Infrastructure]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*), Bash(which:*), Bash(command:*)
---

# Railway Status

Check the current Railway project status for this directory.

## When to Use

- User asks about Railway status, project, services, or deployments
- User mentions deploying or pushing to Railway
- Before any Railway operation (deploy, update service, add variables)
- User asks about environments or domains

## When NOT to Use

Use the railway-environment skill instead when user wants:
- Detailed service configuration (builder type, dockerfile path, build command, root directory)
- Deploy config (start command, restart policy, healthchecks, predeploy command)
- Service source (repo, branch, image)
- Compare service configs
- Query or change environment variables

## Check Status

Run:
```bash
railway status --json
```

First verify CLI is installed:
```bash
command -v railway
```

## Handling Errors

### CLI Not Installed
If `command -v railway` fails:

> Railway CLI is not installed. Install with:
> ```
> npm install -g @railway/cli
> ```
> or
> ```
> brew install railway
> ```
> Then authenticate: `railway login`

### Not Authenticated
If `railway whoami` fails:

> Not logged in to Railway. Run:
> ```
> railway login
> ```

### No Project Linked
If status returns "No linked project":

> No Railway project linked to this directory.
>
> To link an existing project: `railway link`
> To create a new project: `railway init`

## Presenting Status

Parse the JSON and present:
- **Project**: name and workspace
- **Environment**: current environment (production, staging, etc.)
- **Services**: list with deployment status
- **Active Deployments**: any in-progress deployments (from `activeDeployments` field)
- **Domains**: any configured domains

Example output format:
```
Project: my-app (workspace: my-team)
Environment: production

Services:
- web: deployed (https://my-app.up.railway.app)
- api: deploying (build in progress)
- postgres: running
```

The `activeDeployments` array on each service shows currently running deployments
with their status (building, deploying, etc.).

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
