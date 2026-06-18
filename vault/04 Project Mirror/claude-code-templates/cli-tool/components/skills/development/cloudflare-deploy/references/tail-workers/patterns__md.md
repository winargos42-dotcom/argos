---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/tail-workers/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\tail-workers\patterns.md
source_ext: .md
source_sha256: 657df651016480de80f4b6cf9ba72c5a1307c4501da1a95803bde697ee5838e8
text_sha256: 400bb20063049d802f9b9d97924810817234bba9a12d8fd5ff13e9f0913812e4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/tail-workers/patterns.md`
- Extract: `text`
- SHA256: `657df651016480de80f4b6cf9ba72c5a1307c4501da1a95803bde697ee5838e8`

## Content

# Tail Workers Common Patterns

## Community Libraries

While most tail Worker implementations are custom, these libraries may help:

**Logging/Observability:**
- **Axiom** - `axiom-cloudflare-workers` (npm) - Direct Axiom integration
- **Baselime** - SDK for Baselime observability platform
- **LogFlare** - Structured log aggregation

**Type Definitions:**
- **@cloudflare/workers-types** - Official TypeScript types (use `TraceItem`)

**Note:** Most integrations require custom tail handler implementation. See integration examples below.

## Basic Patterns

### HTTP Endpoint Logging

```typescript
export default {
  async tail(events, env, ctx) {
    const payload = events.map(event => ({
      script: event.scriptName,
      timestamp: event.eventTimestamp,
      outcome: event.outcome,
      url: event.event?.request?.url,
      status: event.event?.response?.status,
      logs: event.logs,
      exceptions: event.exceptions,
    }));
    
    ctx.waitUntil(
      fetch(env.LOG_ENDPOINT, {
        method: "POST",
        body: JSON.stringify(payload),
      })
    );
  }
};
```

### Error Tracking Only

```typescript
export default {
  async tail(events, env, ctx) {
    const errors = events.filter(e => 
      e.outcome === 'exception' || e.exceptions.length > 0
    );
    
    if (errors.length === 0) return;
    
    ctx.waitUntil(
      fetch(env.ERROR_ENDPOINT, {
        method: "POST",
        body: JSON.stringify(errors),
      })
    );
  }
};
```

## Storage Integration

### KV Storage with TTL

```typescript
export default {
  async tail(events, env, ctx) {
    ctx.waitUntil(
      Promise.all(events.map(event =>
        env.LOGS_KV.put(
          `log:${event.scriptName}:${event.eventTimestamp}`,
          JSON.stringify(event),
          { expirationTtl: 86400 }  // 24 hours
        )
      ))
    );
  }
};
```

### Analytics Engine Metrics

```typescript
export default {
  async tail(events, env, ctx) {
    ctx.waitUntil(
      Promise.all(events.map(event =>
        env.ANALYTICS.writeDataPoint({
          blobs: [event.scriptName, event.outcome],
          doubles: [1, event.event?.response?.status ?? 0],
          indexes: [event.event?.request?.cf?.colo ?? 'unknown'],
        })
      ))
    );
  }
};
```

## Filtering & Routing

Filter by route, outcome, or other criteria:

```typescript
export default {
  async tail(events, env, ctx) {
    // Route filtering
    const apiEvents = events.filter(e => 
      e.event?.request?.url?.includes('/api/')
    );
    
    // Multi-destination routing
    const errors = events.filter(e => e.outcome === 'exception');
    const success = events.filter(e => e.outcome === 'ok');
    
    const tasks = [];
    if (errors.length > 0) {
      tasks.push(fetch(env.ERROR_ENDPOINT, {
        method: "POST",
        body: JSON.stringify(errors),
      }));
    }
    if (success.length > 0) {
      tasks.push(fetch(env.SUCCESS_ENDPOINT, {
        method: "POST",
        body: JSON.stringify(success),
      }));
    }
    
    ctx.waitUntil(Promise.all(tasks));
  }
};
```

## Sampling

Reduce costs by processing only a percentage of events:

```typescript
export default {
  async tail(events, env, ctx) {
    if (Math.random() > 0.1) return;  // 10% sample rate
    ctx.waitUntil(fetch(env.LOG_ENDPOINT, {
      method: "POST",
      body: JSON.stringify(events),
    }));
  }
};
```

## Advanced Patterns

### Batching with Durable Objects

Accumulate events before sending:

```typescript
export default {
  async tail(events, env, ctx) {
    const batch = env.BATCH_DO.get(env.BATCH_DO.idFromName("batch"));
    ctx.waitUntil(batch.fetch("https://batch/add", {
      method: "POST",
      body: JSON.stringify(events),
    }));
  }
};
```

See durable-objects skill for full implementation.

### Workers for Platforms

Dynamic dispatch sends TWO events per request. Filter by `scriptName` to distinguish dispatch vs user Worker events.

### Error Handling

Always wrap external calls. See gotchas.md for fallback storage pattern.

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
