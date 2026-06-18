---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-playground/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workers-playground\gotchas.md
source_ext: .md
source_sha256: a07b51705f3ac79ddd3eb298e1a23fd68c54abdc74eaf0107973bd23ca8026ac
text_sha256: 85e262f98373f1631dcef3f44a57b6d9e30f8e930e013dc8667fa5993bb6dfae
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-playground/gotchas.md`
- Extract: `text`
- SHA256: `a07b51705f3ac79ddd3eb298e1a23fd68c54abdc74eaf0107973bd23ca8026ac`

## Content

# Workers Playground Gotchas

## Platform Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Safari broken | Preview fails | Use Chrome/Firefox/Edge |
| TypeScript unsupported | TS syntax errors | Write plain JS or use JSDoc |
| No bindings | `env` always `{}` | Mock data or use external APIs |
| No env vars | Can't access secrets | Hardcode for testing |

## Common Runtime Errors

### "Response body already read"

```javascript
// ❌ Body consumed twice
const body = await request.text();
await fetch(url, { body: request.body }); // Error!

// ✅ Clone first
const clone = request.clone();
const body = await request.text();
await fetch(url, { body: clone.body });
```

### "Worker exceeded CPU time"

**Limit:** 10ms (free), 50ms (paid)

```javascript
// ✅ Move slow work to background
ctx.waitUntil(fetch('https://analytics.example.com', {...}));
return new Response('OK'); // Return immediately
```

### "Too many subrequests"

**Limit:** 50 (free), 1000 (paid)

```javascript
// ❌ 100 individual fetches
// ✅ Batch into single API call
await fetch('https://api.example.com/batch', {
  body: JSON.stringify({ ids: [...] })
});
```

## Best Practices

```javascript
// Clone before caching
await cache.put(request, response.clone());
return response;

// Validate input early
if (request.method !== 'POST') return new Response('', { status: 405 });

// Handle errors
try { ... } catch (e) {
  return Response.json({ error: e.message }, { status: 500 });
}
```

## Limits

| Resource | Free | Paid |
|----------|------|------|
| CPU time | 10ms | 50ms |
| Memory | 128 MB | 128 MB |
| Subrequests | 50 | 1000 |

## Browser Support

| Browser | Status |
|---------|--------|
| Chrome | ✅ Recommended |
| Firefox | ✅ Works |
| Edge | ✅ Works |
| Safari | ❌ Broken |

## Debugging

```javascript
console.log('URL:', request.url); // View in browser DevTools Console
```

**Note:** `console.log` works in playground. For production, use Logpush or Tail Workers.

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
