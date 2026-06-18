---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ai-gateway\configuration.md
source_ext: .md
source_sha256: f5fade7be02c081bfa0bfcb330ceda3c60ce666dcaac3aaa954574529a19baab
text_sha256: 1135a774a42e059942ccb12d8ba514e6479d7f8f5f47400b4053f6da5984b532
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/configuration.md`
- Extract: `text`
- SHA256: `f5fade7be02c081bfa0bfcb330ceda3c60ce666dcaac3aaa954574529a19baab`

## Content

# Configuration & Setup

## Creating a Gateway

### Dashboard
AI > AI Gateway > Create Gateway > Configure (auth, caching, rate limiting, logging)

### API
```bash
curl -X POST https://api.cloudflare.com/client/v4/accounts/{account_id}/ai-gateway/gateways \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"id":"my-gateway","cache_ttl":3600,"rate_limiting_interval":60,"rate_limiting_limit":100,"collect_logs":true}'
```

**Naming:** lowercase alphanumeric + hyphens (e.g., `prod-api`, `dev-chat`)

## Wrangler Integration

```toml
[ai]
binding = "AI"

\[\[ai.gateway\]\]
id = "my-gateway"
```

```bash
wrangler secret put CF_API_TOKEN
wrangler secret put OPENAI_API_KEY  # If not using BYOK
```

## Authentication

### Gateway Auth (protects gateway access)
```typescript
const client = new OpenAI({
  baseURL: `https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/openai`,
  defaultHeaders: { 'cf-aig-authorization': `Bearer ${cfToken}` }
});
```

### Provider Auth Options

**1. Unified Billing (keyless)** - pay through Cloudflare, no provider key:
```typescript
const client = new OpenAI({
  baseURL: `https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/openai`,
  defaultHeaders: { 'cf-aig-authorization': `Bearer ${cfToken}` }
});
```
Supports: OpenAI, Anthropic, Google AI Studio

**2. BYOK** - store keys in dashboard (Provider Keys > Add), no key in code

**3. Request Headers** - pass provider key per request:
```typescript
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: `https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/openai`,
  defaultHeaders: { 'cf-aig-authorization': `Bearer ${cfToken}` }
});
```

## API Token Permissions

- **Gateway management:** AI Gateway - Read + Edit
- **Gateway access:** AI Gateway - Read (minimum)

## Gateway Management API

```bash
# List
curl https://api.cloudflare.com/client/v4/accounts/{account_id}/ai-gateway/gateways \
  -H "Authorization: Bearer $CF_API_TOKEN"

# Get
curl .../gateways/{gateway_id}

# Update
curl -X PUT .../gateways/{gateway_id} \
  -d '{"cache_ttl":7200,"rate_limiting_limit":200}'

# Delete
curl -X DELETE .../gateways/{gateway_id}
```

## Getting IDs

- **Account ID:** Dashboard > Overview > Copy
- **Gateway ID:** AI Gateway > Gateway name column

## Python Example

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=f"https://gateway.ai.cloudflare.com/v1/{os.environ['CF_ACCOUNT_ID']}/{os.environ['GATEWAY_ID']}/openai",
    default_headers={"cf-aig-authorization": f"Bearer {os.environ['CF_API_TOKEN']}"}
)
```

## Best Practices

1. **Always authenticate gateways in production**
2. **Use BYOK or unified billing** - secrets out of code
3. **Environment-specific gateways** - separate dev/staging/prod
4. **Set rate limits** - prevent runaway costs
5. **Enable logging** - track usage, debug issues

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
