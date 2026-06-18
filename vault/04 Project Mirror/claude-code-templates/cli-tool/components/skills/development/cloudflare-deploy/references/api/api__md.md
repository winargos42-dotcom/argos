---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/api/api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\api\api.md
source_ext: .md
source_sha256: ebdd5208ce26ab816a35bc3c1abbabf9285216ad46489ce253de6f4caa9482f4
text_sha256: 847c33ce18c1a4ff210ce5db75db0694113fe5367bdba983b0e6f0d7dd2742b1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# api.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/api/api.md`
- Extract: `text`
- SHA256: `ebdd5208ce26ab816a35bc3c1abbabf9285216ad46489ce253de6f4caa9482f4`

## Content

# API Reference

## Client Initialization

### TypeScript

```typescript
import Cloudflare from 'cloudflare';

const client = new Cloudflare({
  apiToken: process.env.CLOUDFLARE_API_TOKEN,
});
```

### Python

```python
from cloudflare import Cloudflare

client = Cloudflare(api_token=os.environ.get("CLOUDFLARE_API_TOKEN"))

# For async:
from cloudflare import AsyncCloudflare
client = AsyncCloudflare(api_token=os.environ["CLOUDFLARE_API_TOKEN"])
```

### Go

```go
import (
    "github.com/cloudflare/cloudflare-go/v4"
    "github.com/cloudflare/cloudflare-go/v4/option"
)

client := cloudflare.NewClient(
    option.WithAPIToken(os.Getenv("CLOUDFLARE_API_TOKEN")),
)
```

## Authentication

### API Token (Recommended)

**Create token**: Dashboard → My Profile → API Tokens → Create Token

```bash
export CLOUDFLARE_API_TOKEN='your-token-here'

curl "https://api.cloudflare.com/client/v4/zones" \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

**Token scopes**: Always use minimal permissions (zone-specific, time-limited).

### API Key (Legacy)

```bash
curl "https://api.cloudflare.com/client/v4/zones" \
  --header "X-Auth-Email: user@example.com" \
  --header "X-Auth-Key: $CLOUDFLARE_API_KEY"
```

**Not recommended:** Full account access, cannot scope permissions.

## Auto-Pagination

All SDKs support automatic pagination for list operations.

```typescript
// TypeScript: for await...of
for await (const zone of client.zones.list()) {
  console.log(zone.id);
}
```

```python
# Python: iterator protocol
for zone in client.zones.list():
    print(zone.id)
```

```go
// Go: ListAutoPaging
iter := client.Zones.ListAutoPaging(ctx, cloudflare.ZoneListParams{})
for iter.Next() {
    zone := iter.Current()
    fmt.Println(zone.ID)
}
```

## Error Handling

```typescript
try {
  const zone = await client.zones.get({ zone_id: 'xxx' });
} catch (err) {
  if (err instanceof Cloudflare.NotFoundError) {
    // 404
  } else if (err instanceof Cloudflare.RateLimitError) {
    // 429 - SDK auto-retries with backoff
  } else if (err instanceof Cloudflare.APIError) {
    console.log(err.status, err.message);
  }
}
```

**Common Error Types:**
- `AuthenticationError` (401) - Invalid token
- `PermissionDeniedError` (403) - Insufficient scope
- `NotFoundError` (404) - Resource not found
- `RateLimitError` (429) - Rate limit exceeded
- `InternalServerError` (≥500) - Cloudflare error

## Zone Management

```typescript
// List zones
const zones = await client.zones.list({
  account: { id: 'account-id' },
  status: 'active',
});

// Create zone
const zone = await client.zones.create({
  account: { id: 'account-id' },
  name: 'example.com',
  type: 'full', // or 'partial'
});

// Update zone
await client.zones.edit('zone-id', {
  paused: false,
});

// Delete zone
await client.zones.delete('zone-id');
```

```go
// Go: requires cloudflare.F() wrapper
zone, err := client.Zones.New(ctx, cloudflare.ZoneNewParams{
    Account: cloudflare.F(cloudflare.ZoneNewParamsAccount{
        ID: cloudflare.F("account-id"),
    }),
    Name: cloudflare.F("example.com"),
    Type: cloudflare.F(cloudflare.ZoneNewParamsTypeFull),
})
```

## DNS Management

```typescript
// Create DNS record
await client.dns.records.create({
  zone_id: 'zone-id',
  type: 'A',
  name: 'subdomain.example.com',
  content: '192.0.2.1',
  ttl: 1, // auto
  proxied: true, // Orange cloud
});

// List DNS records (with auto-pagination)
for await (const record of client.dns.records.list({
  zone_id: 'zone-id',
  type: 'A',
})) {
  console.log(record.name, record.content);
}

// Update DNS record
await client.dns.records.update({
  zone_id: 'zone-id',
  dns_record_id: 'record-id',
  type: 'A',
  name: 'subdomain.example.com',
  content: '203.0.113.1',
  proxied: true,
});

// Delete DNS record
await client.dns.records.delete({
  zone_id: 'zone-id',
  dns_record_id: 'record-id',
});
```

```python
# Python example
client.dns.records.create(
    zone_id="zone-id",
    type="A",
    name="subdomain.example.com",
    content="192.0.2.1",
    ttl=1,
    proxied=True,
)
```

## See Also

- [configuration.md](./configuration.md) - SDK configuration, environment variables
- [patterns.md](./patterns.md) - Real-world patterns and workflows
- [gotchas.md](./gotchas.md) - Rate limits, troubleshooting

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
