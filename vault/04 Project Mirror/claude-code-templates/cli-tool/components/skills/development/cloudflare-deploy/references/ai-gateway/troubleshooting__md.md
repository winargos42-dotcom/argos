---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/troubleshooting.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ai-gateway\troubleshooting.md
source_ext: .md
source_sha256: bb4d7a44f80bc31b78460c6944e7b838d12d3b42502a2d214cc2054330e7e814
text_sha256: c79d02ce7b9e6cb361f1700eff6e12149fc74547aad3438501863d8cd02b2a79
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# troubleshooting.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/troubleshooting.md`
- Extract: `text`
- SHA256: `bb4d7a44f80bc31b78460c6944e7b838d12d3b42502a2d214cc2054330e7e814`

## Content

# AI Gateway Troubleshooting

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 401 | Missing `cf-aig-authorization` header | Add header with CF API token |
| 403 | Invalid provider key / BYOK expired | Check provider key in dashboard |
| 429 | Rate limit exceeded | Increase limit or implement backoff |

### 401 Fix

```typescript
const client = new OpenAI({
  baseURL: `https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/openai`,
  defaultHeaders: { 'cf-aig-authorization': `Bearer ${CF_API_TOKEN}` }
});
```

### 429 Retry Pattern

```typescript
async function requestWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try { return await fn(); }
    catch (e) {
      if (e.status === 429 && i < maxRetries - 1) {
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        continue;
      }
      throw e;
    }
  }
}
```

## Gotchas

| Issue | Reality |
|-------|---------|
| Metadata limits | Max 5 entries, flat only (no nesting) |
| Cache key collision | Use unique keys per expected response |
| BYOK + Unified Billing | Mutually exclusive |
| Rate limit scope | Per-gateway, not per-user (use dynamic routing for per-user) |
| Log delay | 30-60 seconds normal |
| Streaming + caching | **Incompatible** |
| Model name (unified API) | Prefix required: `openai/gpt-4o`, not `gpt-4o` |

## Cache Not Working

**Causes:**
- Different request params (temperature, etc.)
- Streaming enabled
- Caching disabled in settings

**Check:** `response.headers.get('cf-aig-cache-status')` → HIT or MISS

## Logs Not Appearing

1. Check logging enabled: Dashboard → Gateway → Settings
2. Remove `cf-aig-collect-log: false` header
3. Wait 30-60 seconds
4. Check log limit (10M default)

## Debugging

```bash
# Test connectivity
curl -v https://gateway.ai.cloudflare.com/v1/{account}/{gateway}/openai/models \
  -H "Authorization: Bearer $OPENAI_KEY" \
  -H "cf-aig-authorization: Bearer $CF_TOKEN"
```

```typescript
// Check response headers
console.log('Cache:', response.headers.get('cf-aig-cache-status'));
console.log('Request ID:', response.headers.get('cf-ray'));
```

## Analytics

Dashboard → AI Gateway → Select gateway

**Metrics:** Requests, tokens, latency (p50/p95/p99), cache hit rate, costs

**Log filters:** `status: error`, `provider: openai`, `cost > 0.01`, `duration > 1000`

**Export:** Logpush to S3/GCS/Datadog/Splunk

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
