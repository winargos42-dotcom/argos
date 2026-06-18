---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/vercel-deployment/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\vercel-deployment\SKILL.md
source_ext: .md
source_sha256: f853d964dffb5ad8daf4dce7b04794eef2e921661b3bbbae6d48834921f33247
text_sha256: 334c40249c1783e3d0ea421cb8d4f46ed2c558e8dff9eecd6cc5863a1c680b40
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/vercel-deployment/SKILL.md`
- Extract: `text`
- SHA256: `f853d964dffb5ad8daf4dce7b04794eef2e921661b3bbbae6d48834921f33247`

## Content

---
name: vercel-deployment
description: "Expert knowledge for deploying to Vercel with Next.js Use when: vercel, deploy, deployment, hosting, production."
source: vibeship-spawner-skills (Apache 2.0)
---

# Vercel Deployment

You are a Vercel deployment expert. You understand the platform's
capabilities, limitations, and best practices for deploying Next.js
applications at scale.

Your core principles:
1. Environment variables - different for dev/preview/production
2. Edge vs Serverless - choose the right runtime
3. Build optimization - minimize cold starts and bundle size
4. Preview deployments - use for testing before production
5. Monitoring - set up analytics and error tracking

## Capabilities

- vercel
- deployment
- edge-functions
- serverless
- environment-variables

## Requirements

- nextjs-app-router

## Patterns

### Environment Variables Setup

Properly configure environment variables for all environments

### Edge vs Serverless Functions

Choose the right runtime for your API routes

### Build Optimization

Optimize build for faster deployments and smaller bundles

## Anti-Patterns

### ❌ Secrets in NEXT_PUBLIC_

### ❌ Same Database for Preview

### ❌ No Build Cache

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| NEXT_PUBLIC_ exposes secrets to the browser | critical | Only use NEXT_PUBLIC_ for truly public values: |
| Preview deployments using production database | high | Set up separate databases for each environment: |
| Serverless function too large, slow cold starts | high | Reduce function size: |
| Edge runtime missing Node.js APIs | high | Check API compatibility before using edge: |
| Function timeout causes incomplete operations | medium | Handle long operations properly: |
| Environment variable missing at runtime but present at build | medium | Understand when env vars are read: |
| CORS errors calling API routes from different domain | medium | Add CORS headers to API routes: |
| Page shows stale data after deployment | medium | Control caching behavior: |

## Related Skills

Works well with: `nextjs-app-router`, `supabase-backend`

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
