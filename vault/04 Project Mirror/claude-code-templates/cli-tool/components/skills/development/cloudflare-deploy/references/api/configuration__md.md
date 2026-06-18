---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/api/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\api\configuration.md
source_ext: .md
source_sha256: 25d564adbe0fdde2faccd5a9a261b17360c49fc82c7bfabd0ffc1b31438b2158
text_sha256: 6ea23fb895605fd2a2380580f7cd21ab39c51dde470067ed191fd387f6337cb4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/api/configuration.md`
- Extract: `text`
- SHA256: `25d564adbe0fdde2faccd5a9a261b17360c49fc82c7bfabd0ffc1b31438b2158`

## Content

# Configuration

## Environment Variables

### Set Variables

| Platform | Command |
|----------|---------|
| Linux/macOS | `export CLOUDFLARE_API_TOKEN='token'` |
| PowerShell | `$env:CLOUDFLARE_API_TOKEN = 'token'` |
| Windows CMD | `set CLOUDFLARE_API_TOKEN=token` |

**Security:** Never commit tokens. Use `.env` files (gitignored) or secret managers.

### .env File Pattern

```bash
# .env (add to .gitignore)
CLOUDFLARE_API_TOKEN=your-token-here
CLOUDFLARE_ACCOUNT_ID=your-account-id
```

```typescript
// TypeScript
import 'dotenv/config';

const client = new Cloudflare({
  apiToken: process.env.CLOUDFLARE_API_TOKEN,
});
```

```python
# Python
from dotenv import load_dotenv
load_dotenv()

client = Cloudflare(api_token=os.environ["CLOUDFLARE_API_TOKEN"])
```

## SDK Configuration

### TypeScript

```typescript
const client = new Cloudflare({
  apiToken: process.env.CLOUDFLARE_API_TOKEN,
  timeout: 120000,        // 2 min (default 60s), in milliseconds
  maxRetries: 5,          // default 2
  baseURL: 'https://...', // proxy (rare)
});

// Per-request overrides
await client.zones.get(
  { zone_id: 'zone-id' },
  { timeout: 5000, maxRetries: 0 }
);
```

### Python

```python
client = Cloudflare(
    api_token=os.environ["CLOUDFLARE_API_TOKEN"],
    timeout=120,         # seconds (default 60)
    max_retries=5,       # default 2
    base_url="https://...",  # proxy (rare)
)

# Per-request overrides
client.with_options(timeout=5, max_retries=0).zones.get(zone_id="zone-id")
```

### Go

```go
client := cloudflare.NewClient(
    option.WithAPIToken(os.Getenv("CLOUDFLARE_API_TOKEN")),
    option.WithMaxRetries(5),  // default 10 (higher than TS/Python)
    option.WithRequestTimeout(2 * time.Minute),  // default 60s
    option.WithBaseURL("https://..."),  // proxy (rare)
)

// Per-request overrides
client.Zones.Get(ctx, "zone-id", option.WithMaxRetries(0))
```

## Configuration Options

| Option | TypeScript | Python | Go | Default |
|--------|-----------|--------|-----|---------|
| Timeout | `timeout` (ms) | `timeout` (s) | `WithRequestTimeout` | 60s |
| Retries | `maxRetries` | `max_retries` | `WithMaxRetries` | 2 (Go: 10) |
| Base URL | `baseURL` | `base_url` | `WithBaseURL` | api.cloudflare.com |

**Note:** Go SDK has higher default retries (10) than TypeScript/Python (2).

## Timeout Configuration

**When to increase:**
- Large zone transfers
- Bulk DNS operations
- Worker script uploads

```typescript
const client = new Cloudflare({
  timeout: 300000, // 5 minutes
});
```

## Retry Configuration

**When to increase:** Rate-limit-heavy workflows, flaky network

**When to decrease:** Fast-fail requirements, user-facing requests

```typescript
// Increase retries for batch operations
const client = new Cloudflare({ maxRetries: 10 });

// Disable retries for fast-fail
const fastClient = new Cloudflare({ maxRetries: 0 });
```

## Wrangler CLI Integration

```bash
# Configure authentication
wrangler login
# Or
export CLOUDFLARE_API_TOKEN='token'

# Common commands that use API
wrangler deploy              # Uploads worker via API
wrangler kv:key put          # KV operations
wrangler r2 bucket create    # R2 operations
wrangler d1 execute          # D1 operations
wrangler pages deploy        # Pages operations

# Get API configuration
wrangler whoami              # Shows authenticated user
```

### wrangler.toml

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"
account_id = "your-account-id"

# Can also use env vars:
# CLOUDFLARE_ACCOUNT_ID
# CLOUDFLARE_API_TOKEN
```

## See Also

- [api.md](./api.md) - Client initialization, authentication
- [gotchas.md](./gotchas.md) - Rate limits, timeout errors
- [Wrangler Reference](../wrangler/) - CLI tool details

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
