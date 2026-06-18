---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/tail-workers/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\tail-workers\README.md
source_ext: .md
source_sha256: e39e7ebcbc9b3597f2c8b49e2a9f3ffd75010528c049257c5c6f04036666c16c
text_sha256: 22776dd6348b07d2c7132ee4a52715f49bc61c1bb50d0af81e49281e44bb9799
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/tail-workers/README.md`
- Extract: `text`
- SHA256: `e39e7ebcbc9b3597f2c8b49e2a9f3ffd75010528c049257c5c6f04036666c16c`

## Content

# Cloudflare Tail Workers

Specialized Workers that consume execution events from producer Workers for logging, debugging, analytics, and observability.

## When to Use This Reference

- Implementing observability/logging for Cloudflare Workers
- Processing Worker execution events, logs, exceptions
- Building custom analytics or error tracking
- Configuring real-time event streaming
- Working with tail handlers or tail consumers

## Core Concepts

### What Are Tail Workers?

Tail Workers automatically process events from producer Workers (the Workers being monitored). They receive:
- HTTP request/response info
- Console logs (`console.log/error/warn/debug`)
- Uncaught exceptions
- Execution outcomes (`ok`, `exception`, `exceededCpu`, etc.)
- Diagnostic channel events

**Key characteristics:**
- Invoked AFTER producer finishes executing
- Capture entire request lifecycle including Service Bindings and Dynamic Dispatch sub-requests
- Billed by CPU time, not request count
- Available on Workers Paid and Enterprise tiers

### Alternative: OpenTelemetry Export

**Before using Tail Workers, consider OpenTelemetry:**

For batch exports to observability tools (Sentry, Grafana, Honeycomb):
- OTEL export sends logs/traces in batches (more efficient)
- Built-in integrations with popular platforms
- Lower overhead than Tail Workers
- **Use Tail Workers only for custom real-time processing**

## Decision Tree

```
Need observability for Workers?
├─ Batch export to known tools (Sentry/Grafana/Honeycomb)?
│  └─ Use OpenTelemetry export (not Tail Workers)
├─ Custom real-time processing needed?
│  ├─ Aggregated metrics?
│  │  └─ Use Tail Worker + Analytics Engine
│  ├─ Error tracking?
│  │  └─ Use Tail Worker + external service
│  ├─ Custom logging/debugging?
│  │  └─ Use Tail Worker + KV/HTTP endpoint
│  └─ Complex event processing?
│     └─ Use Tail Worker + Durable Objects
└─ Quick debugging?
   └─ Use `wrangler tail` (different from Tail Workers)
```

## Reading Order

1. **[configuration.md](configuration.md)** - Set up Tail Workers
2. **[api.md](api.md)** - Handler signature, types, redaction
3. **[patterns.md](patterns.md)** - Common use cases and integrations
4. **[gotchas.md](gotchas.md)** - Pitfalls and debugging tips

## Quick Example

```typescript
export default {
  async tail(events, env, ctx) {
    // Process events from producer Worker
    ctx.waitUntil(
      fetch(env.LOG_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(events),
      })
    );
  }
};
```

## Related Skills

- **observability** - General Workers observability patterns, OTEL export
- **analytics-engine** - Aggregated metrics storage for tail event data
- **durable-objects** - Stateful event processing, batching tail events
- **logpush** - Alternative for batch log export (non-real-time)
- **workers-for-platforms** - Dynamic dispatch with tail consumers

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
