---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workers\README.md
source_ext: .md
source_sha256: a426e0cafade8f3b76fcf84eeb777d3aa263b2634f4011305d085621565a03ef
text_sha256: 4e00df1c6d64cd393c909430769c183b7027b4fe1db0c2dbb31090987baff14c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers/README.md`
- Extract: `text`
- SHA256: `a426e0cafade8f3b76fcf84eeb777d3aa263b2634f4011305d085621565a03ef`

## Content

# Cloudflare Workers

Expert guidance for building, deploying, and optimizing Cloudflare Workers applications.

## Overview

Cloudflare Workers run on V8 isolates (NOT containers/VMs):
- Extremely fast cold starts (< 1ms)
- Global deployment across 300+ locations
- Web standards compliant (fetch, URL, Headers, Request, Response)
- Support JS/TS, Python, Rust, and WebAssembly

**Key principle**: Workers use web platform APIs wherever possible for portability.

## Module Worker Pattern (Recommended)

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response('Hello World!');
  },
};
```

**Handler parameters**:
- `request`: Incoming HTTP request (standard Request object)
- `env`: Environment bindings (KV, D1, R2, secrets, vars)
- `ctx`: Execution context (`waitUntil`, `passThroughOnException`)

## Essential Commands

```bash
npx wrangler dev                    # Local dev
npx wrangler dev --remote           # Remote dev (actual resources)
npx wrangler deploy                 # Production
npx wrangler deploy --env staging   # Specific environment
npx wrangler tail                   # Stream logs
npx wrangler secret put API_KEY     # Set secret
```

## When to Use Workers

- API endpoints at the edge
- Request/response transformation
- Authentication/authorization layers
- Static asset optimization
- A/B testing and feature flags
- Rate limiting and security
- Proxy/routing logic
- WebSocket applications

## Quick Start

```bash
npm create cloudflare@latest my-worker -- --type hello-world
cd my-worker
npx wrangler dev
```

## Handler Signatures

```typescript
// HTTP requests
async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response>

// Cron triggers
async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void>

// Queue consumer
async queue(batch: MessageBatch, env: Env, ctx: ExecutionContext): Promise<void>

// Tail consumer
async tail(events: TraceItem[], env: Env, ctx: ExecutionContext): Promise<void>
```

## Resources

**Docs**: https://developers.cloudflare.com/workers/  
**Examples**: https://developers.cloudflare.com/workers/examples/  
**Runtime APIs**: https://developers.cloudflare.com/workers/runtime-apis/

## In This Reference

- [Configuration](./configuration.md) - wrangler.jsonc setup, bindings, environments
- [API](./api.md) - Runtime APIs, bindings, execution context
- [Patterns](./patterns.md) - Common workflows, testing, optimization
- [Frameworks](./frameworks.md) - Hono, routing, validation
- [Gotchas](./gotchas.md) - Common issues, limits, troubleshooting

## Reading Order

| Task | Start With | Then Read |
|------|------------|-----------|
| First Worker | README → Configuration → API | Patterns |
| Add framework | Frameworks | Configuration (bindings) |
| Add storage/bindings | Configuration → API (binding usage) | See Also links |
| Debug issues | Gotchas | API (specific binding docs) |
| Production optimization | Patterns | API (caching, streaming) |
| Type safety | Configuration (TypeScript) | Frameworks (Hono typing) |

## See Also

- [KV](../kv/README.md) - Key-value storage
- [D1](../d1/README.md) - SQL database
- [R2](../r2/README.md) - Object storage
- [Durable Objects](../durable-objects/README.md) - Stateful coordination
- [Queues](../queues/README.md) - Message queues
- [Wrangler](../wrangler/README.md) - CLI tool reference

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
