---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-for-platforms/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workers-for-platforms\gotchas.md
source_ext: .md
source_sha256: 26294f75c6ecece4cd71974c61620d5c6309a1b64a9d8dcf8c158a52140a685a
text_sha256: 98904178ec81e30e0503ae512cedf76e0d8bdcc517009984b474a6008243e18f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workers-for-platforms/gotchas.md`
- Extract: `text`
- SHA256: `26294f75c6ecece4cd71974c61620d5c6309a1b64a9d8dcf8c158a52140a685a`

## Content

# Gotchas & Limits

## Common Errors

### "Worker not found"

**Cause:** Attempting to get Worker that doesn't exist in namespace  
**Solution:** Catch error and return 404:

```typescript
try {
  const userWorker = env.DISPATCHER.get(workerName);
  return userWorker.fetch(request);
} catch (e) {
  if (e.message.startsWith("Worker not found")) {
    return new Response("Worker not found", { status: 404 });
  }
  throw e;  // Re-throw unexpected errors
}
```

### "CPU time limit exceeded"

**Cause:** User Worker exceeded configured CPU time limit  
**Solution:** Track violations in Analytics Engine and return 429 response; consider adjusting limits per customer tier

### "Hostname Routing Issues"

**Cause:** DNS proxy settings causing routing problems  
**Solution:** Use `*/*` wildcard route which works regardless of proxy settings for orange-to-orange routing

### "Bindings Lost on Update"

**Cause:** Not using `keep_bindings` flag when updating Worker  
**Solution:** Use `keep_bindings: true` in API requests to preserve existing bindings during updates

### "Tag Filtering Not Working"

**Cause:** Special characters not URL encoded in tag filters  
**Solution:** URL encode tags (e.g., `tags=production%3Ayes`) and avoid special chars like `,` and `&`

### "Deploy Failures with ES Modules"

**Cause:** Incorrect upload format for ES modules  
**Solution:** Use multipart form upload, specify `main_module` in metadata, and set file type to `application/javascript+module`

### "Static Asset Upload Failed"

**Cause:** Invalid hash format, expired token, or incorrect encoding  
**Solution:** Hash must be first 16 bytes (32 hex chars) of SHA-256, upload within 1 hour of session creation, deploy within 1 hour of upload completion, and Base64 encode file contents

### "Outbound Worker Not Intercepting Calls"

**Cause:** Outbound Workers don't intercept Durable Object or mTLS binding fetch  
**Solution:** Plan egress control accordingly; not all fetch calls are intercepted

### "TCP Socket Connection Failed"

**Cause:** Outbound Worker enabled blocks `connect()` API for TCP sockets  
**Solution:** Outbound Workers only intercept `fetch()` calls; TCP socket connections unavailable when outbound configured. Remove outbound if TCP needed, or use proxy pattern.

### "API Rate Limit Exceeded"

**Cause:** Exceeded Cloudflare API rate limits (1200 requests per 5 minutes per account, 200 requests per second per IP)  
**Solution:** Implement exponential backoff:

```typescript
async function deployWithBackoff(deploy: () => Promise<void>, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await deploy();
    } catch (e) {
      if (e.status === 429 && i < maxRetries - 1) {
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        continue;
      }
      throw e;
    }
  }
}
```

### "Gradual Deployment Not Supported"

**Cause:** Attempted to use gradual deployments with user Workers  
**Solution:** Gradual deployments not supported for Workers in dispatch namespaces. Use all-at-once deployment with staged rollout via dispatch worker logic (feature flags, percentage-based routing).

### "Asset Session Expired"

**Cause:** Upload JWT expired (1 hour validity) or completion token expired (1 hour after upload)  
**Solution:** Complete asset upload within 1 hour of session creation, and deploy Worker within 1 hour of upload completion. For large uploads, batch files or increase upload parallelism.

## Platform Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Workers per namespace | Unlimited | Unlike regular Workers (500 per account) |
| Namespaces per account | Unlimited | Best practice: 1 production + 1 staging |
| Max tags per Worker | 8 | For filtering and organization |
| Worker mode | Untrusted (default) | No `request.cf` access unless trusted mode |
| Cache isolation | Per-Worker (untrusted) | Shared in trusted mode with key prefixes |
| Durable Object namespaces | Unlimited | No per-account limit for WfP |
| Gradual Deployments | Not supported | All-at-once only |
| `caches.default` | Disabled (untrusted) | Use Cache API with custom keys |

## Asset Upload Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Upload session JWT validity | 1 hour | Must complete upload within this time |
| Completion token validity | 1 hour | Must deploy within this time after upload |
| Asset hash format | First 16 bytes SHA-256 | 32 hex characters |
| Base64 encoding | Required | For binary files |

## API Rate Limits

| Limit Type | Value | Scope |
|------------|-------|-------|
| Client API | 1200 requests / 5 min | Per account |
| Client API | 200 requests / sec | Per IP address |
| GraphQL | Varies by query cost | Query complexity |

See [Cloudflare API Rate Limits](https://developers.cloudflare.com/fundamentals/api/reference/limits/) for details.

## Operational Limits

| Operation | Limit | Notes |
|-----------|-------|-------|
| CPU time (custom limits) | Up to Workers plan limit | Set per-invocation in dispatch worker |
| Subrequests (custom limits) | Up to Workers plan limit | Set per-invocation in dispatch worker |
| Outbound Worker subrequests | Not intercepted for DO/mTLS | Only regular fetch() calls |
| TCP sockets with outbound | Disabled | `connect()` API unavailable |

See [README.md](./README.md), [configuration.md](./configuration.md), [api.md](./api.md), [patterns.md](./patterns.md)

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
