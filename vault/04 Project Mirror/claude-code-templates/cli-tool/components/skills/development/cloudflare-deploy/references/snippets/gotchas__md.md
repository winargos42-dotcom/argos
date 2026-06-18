---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/snippets/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\snippets\gotchas.md
source_ext: .md
source_sha256: f243bbd25fded90b3f6a3b22436cb7eb5f5330d8c25249d64d9c00b57086de76
text_sha256: 301c7167f03075505498f1f6b5fe1c72a393065a8228f42c435fde9f1b694150
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/snippets/gotchas.md`
- Extract: `text`
- SHA256: `f243bbd25fded90b3f6a3b22436cb7eb5f5330d8c25249d64d9c00b57086de76`

## Content

# Gotchas & Best Practices

## Common Errors

### 1000: "Snippet execution failed"
Runtime error or syntax error. Wrap code in try/catch:
```javascript
try { return await fetch(request); }
catch (error) { return new Response(`Error: ${error.message}`, { status: 500 }); }
```

### 1100: "Exceeded execution limit"
Code takes >5ms CPU. Simplify logic or move to Workers.

### 1201: "Multiple origin fetches"
Call `fetch(request)` exactly once:
```javascript
// ❌ Multiple origin fetches
const r1 = await fetch(request); const r2 = await fetch(request);
// ✅ Single fetch, reuse response
const response = await fetch(request);
```

### 1202: "Subrequest limit exceeded"
Pro: 2 subrequests, Business/Enterprise: 5. Reduce fetch calls.

### "Cannot set property on immutable object"
Clone before modifying:
```javascript
const modifiedRequest = new Request(request);
modifiedRequest.headers.set("X-Custom", "value");
```

### "caches is not defined"
Cache API NOT available in Snippets. Use Workers.

### "Module not found"
Snippets don't support `import`. Use inline code or Workers.

## Best Practices

### Performance
- Keep code <10KB (32KB limit)
- Optimize for 5ms CPU
- Clone only when modifying
- Minimize subrequests

### Security
- Validate all inputs
- Use Web Crypto API for hashing
- Sanitize headers before origin
- Don't log secrets

### Debugging
```javascript
newResponse.headers.set("X-Debug-Country", request.cf.country);
```
```bash
curl -H "X-Test: true" https://example.com -v
```

## Available APIs

**✅ Available:** `fetch()`, `Request`, `Response`, `Headers`, `URL`, `crypto.subtle`, `crypto.randomUUID()`, `atob()`/`btoa()`, `JSON`

**❌ NOT Available:** `caches`, `KV`, `D1`, `R2`, `Durable Objects`, `WebSocket`, `HTMLRewriter`, `import`, Node.js APIs

## Limits

| Resource | Limit |
|----------|-------|
| Snippet size | 32KB |
| Execution time | 5ms CPU |
| Subrequests (Pro/Biz) | 2/5 |
| Snippets/zone | 20 |

## Performance Benchmarks

| Operation | Time |
|-----------|------|
| Header set | <0.1ms |
| URL parsing | <0.2ms |
| fetch() | 1-3ms |
| SHA-256 | 0.5-1ms |

**Migrate to Workers when:** >5ms needed, >5 subrequests, need storage (KV/D1/R2), need npm packages, >32KB code

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
