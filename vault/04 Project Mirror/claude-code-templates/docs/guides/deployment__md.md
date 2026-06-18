---
argos_import: project_file
source_path: claude-code-templates/docs/guides/deployment.md
source_abs: F:\debug\argoss\claude-code-templates\docs\guides\deployment.md
source_ext: .md
source_sha256: a496b73e5fe0134829b76504768c13d45ee878df237355035410062b711d5790
text_sha256: 3b1184491c05fb2e04cecdeb039c283ae9a324ae2a09d0be783bcea15713b279
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# deployment.md

- Source: `claude-code-templates/docs/guides/deployment.md`
- Extract: `text`
- SHA256: `a496b73e5fe0134829b76504768c13d45ee878df237355035410062b711d5790`

## Content

# 🚀 Deployment Guide

This project is configured for automatic deployment to Vercel from the `main` branch.

## GitHub Actions Setup

### Required Secrets

Add these secrets to your GitHub repository settings:

1. **VERCEL_TOKEN**: Your Vercel account token
   - Go to [Vercel Account Settings](https://vercel.com/account/tokens)
   - Create a new token with appropriate permissions
   - Add as `VERCEL_TOKEN` in GitHub Secrets

2. **VERCEL_ORG_ID**: Your Vercel organization ID
   - Run `vercel link` in your project
   - Copy the `orgId` from `.vercel/project.json`
   - Add as `VERCEL_ORG_ID` in GitHub Secrets

3. **VERCEL_PROJECT_ID**: Your Vercel project ID
   - Run `vercel link` in your project
   - Copy the `projectId` from `.vercel/project.json`
   - Add as `VERCEL_PROJECT_ID` in GitHub Secrets

### Getting the IDs

Run these commands in your project root:

```bash
# Link to Vercel project
vercel link

# Get your IDs from the generated file
cat .vercel/project.json
```

## Deployment Flow

- ✅ **Push to main** → Automatic production deploy to aitmpl.com
- ✅ **Other branches** → Manual deploy only (no auto-deploy)
- ✅ **Pull Requests** → No deployment

## Manual Deployment

For testing other branches:

```bash
# Deploy current branch to preview URL
vercel

# Deploy current branch to production
vercel --prod
```

## Domain Configuration

The main branch deploys to the custom domain: **aitmpl.com**

Configured in Vercel dashboard under Project Settings → Domains.

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
