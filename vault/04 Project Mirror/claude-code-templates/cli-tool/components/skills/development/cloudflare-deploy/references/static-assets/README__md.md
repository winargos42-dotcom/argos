---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/static-assets/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\static-assets\README.md
source_ext: .md
source_sha256: 550e0bfdc5c9c01389270a98ac8ad322f7ab886259d0d771b81c33fbac164fa6
text_sha256: ef31f6ca300cb5fb1f111a626f6d92ef2b5b48a3ed97c2203874c33a2f38c0e8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/static-assets/README.md`
- Extract: `text`
- SHA256: `550e0bfdc5c9c01389270a98ac8ad322f7ab886259d0d771b81c33fbac164fa6`

## Content

# Cloudflare Static Assets Skill Reference

Expert guidance for deploying and configuring static assets with Cloudflare Workers. This skill covers configuration patterns, routing architectures, asset binding usage, and best practices for SPAs, SSG sites, and full-stack applications.

## Quick Start

```jsonc
// wrangler.jsonc
{
  "name": "my-app",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "assets": {
    "directory": "./dist"
  }
}
```

```typescript
// src/index.ts
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return env.ASSETS.fetch(request);
  }
};
```

Deploy: `wrangler deploy`

## When to Use Workers Static Assets vs Pages

| Factor | Workers Static Assets | Cloudflare Pages |
|--------|----------------------|------------------|
| **Use case** | Hybrid apps (static + dynamic API) | Static sites, SSG |
| **Worker control** | Full control over routing | Limited (Functions) |
| **Configuration** | Code-first, flexible | Git-based, opinionated |
| **Dynamic routing** | Worker-first patterns | Functions (_functions/) |
| **Best for** | Full-stack apps, SPAs with APIs | Jamstack, static docs |

**Decision tree:**

- Need custom routing logic? → Workers Static Assets
- Pure static site or SSG? → Pages
- API routes + SPA? → Workers Static Assets
- Framework (Next, Nuxt, Remix)? → Pages

## Reading Order

1. **configuration.md** - Setup, wrangler.jsonc options, routing patterns
2. **api.md** - ASSETS binding API, request/response handling
3. **patterns.md** - Common patterns (SPA, API routes, auth, A/B testing)
4. **gotchas.md** - Limits, errors, performance tips

## In This Reference

- **[configuration.md](configuration.md)** - Setup, deployment, configuration
- **[api.md](api.md)** - API endpoints, methods, interfaces
- **[patterns.md](patterns.md)** - Common patterns, use cases, examples
- **[gotchas.md](gotchas.md)** - Troubleshooting, best practices, limitations

## See Also

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Static Assets Docs](https://developers.cloudflare.com/workers/static-assets/)
- [Cloudflare Pages](https://developers.cloudflare.com/pages/)

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
