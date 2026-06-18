---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/tail-workers/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\tail-workers\configuration.md
source_ext: .md
source_sha256: 0a54eccb88b3865e5f005300b3a543588c37072f674842d07895ff595c1a9b62
text_sha256: 8efac4877ad572f631f78643712a9c1e151661d4efedd728ee23fe2877669845
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/tail-workers/configuration.md`
- Extract: `text`
- SHA256: `0a54eccb88b3865e5f005300b3a543588c37072f674842d07895ff595c1a9b62`

## Content

# Tail Workers Configuration

## Setup Steps

### 1. Create Tail Worker

Create a Worker with a `tail()` handler:

```typescript
export default {
  async tail(events, env, ctx) {
    // Process events from producer Worker
    ctx.waitUntil(
      fetch(env.LOG_ENDPOINT, {
        method: "POST",
        body: JSON.stringify(events),
      })
    );
  }
};
```

### 2. Configure Producer Worker

In producer's `wrangler.jsonc`:

```jsonc
{
  "name": "my-producer-worker",
  "tail_consumers": [
    {
      "service": "my-tail-worker"
    }
  ]
}
```

### 3. Deploy Both Workers

```bash
# Deploy Tail Worker first
cd tail-worker
wrangler deploy

# Then deploy producer Worker
cd ../producer-worker
wrangler deploy
```

## Wrangler Configuration

### Single Tail Consumer

```jsonc
{
  "name": "producer-worker",
  "tail_consumers": [
    {
      "service": "logging-tail-worker"
    }
  ]
}
```

### Multiple Tail Consumers

```jsonc
{
  "name": "producer-worker",
  "tail_consumers": [
    {
      "service": "logging-tail-worker"
    },
    {
      "service": "metrics-tail-worker"
    }
  ]
}
```

**Note:** Each consumer receives ALL events independently.

### Remove Tail Consumer

```jsonc
{
  "tail_consumers": []
}
```

Then redeploy producer Worker.

## Environment Variables

Tail Workers use same binding syntax as regular Workers:

```jsonc
{
  "name": "my-tail-worker",
  "vars": {
    "LOG_ENDPOINT": "https://logs.example.com/ingest"
  },
  "kv_namespaces": [
    {
      "binding": "LOGS_KV",
      "id": "abc123..."
    }
  ]
}
```

## Testing & Development

### Local Testing

**Tail Workers cannot be fully tested with `wrangler dev`.** Deploy to staging environment for testing.

### Testing Strategy

1. Deploy producer Worker to staging
2. Deploy Tail Worker to staging
3. Configure `tail_consumers` in producer
4. Trigger producer Worker requests
5. Verify Tail Worker receives events (check destination logs/storage)

### Wrangler Tail Command

```bash
# Stream logs to terminal (NOT Tail Workers)
wrangler tail my-producer-worker
```

**This is different from Tail Workers:**
- `wrangler tail` streams logs to your terminal
- Tail Workers are Workers that process events programmatically

## Deployment Checklist

- [ ] Tail Worker has `tail()` handler
- [ ] Tail Worker deployed before producer
- [ ] Producer's `wrangler.jsonc` has correct `tail_consumers`
- [ ] Environment variables configured
- [ ] Tested with staging environment
- [ ] Monitoring configured for Tail Worker itself

## Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Max tail consumers per producer | 10 | Each receives all events independently |
| Events batch size | Up to 100 events per invocation | Larger batches split across invocations |
| Tail Worker CPU time | Same as regular Workers | 10ms (free), 30ms (paid), 50ms (paid bundle) |
| Pricing tier | Workers Paid or Enterprise | Not available on free plan |
| Request body size | 100 MB max | When sending to external endpoints |
| Event retention | None | Events not retried if tail handler fails |

## Workers for Platforms

For dynamic dispatch Workers, both dispatch and user Worker events sent to tail consumer:

```jsonc
{
  "name": "dispatch-worker",
  "tail_consumers": [
    {
      "service": "platform-tail-worker"
    }
  ]
}
```

Tail Worker receives TWO `TraceItem` elements per request:
1. Dynamic dispatch Worker event
2. User Worker event

See [patterns.md](patterns.md) for handling.

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
