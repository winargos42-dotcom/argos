---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/queues/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\queues\README.md
source_ext: .md
source_sha256: 82b1f935a6d2c324cadd590bf01457507f717b0ddf1c0c6e8213758fd93016a1
text_sha256: faa1106897e0f1b89a0b87040e14955f7594a48ef966d3ee88ece436cbef9359
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/queues/README.md`
- Extract: `text`
- SHA256: `82b1f935a6d2c324cadd590bf01457507f717b0ddf1c0c6e8213758fd93016a1`

## Content

# Cloudflare Queues

Flexible message queuing for async task processing with guaranteed at-least-once delivery and configurable batching.

## Overview

Queues provide:
- At-least-once delivery guarantee
- Push-based (Worker) and pull-based (HTTP) consumers
- Configurable batching and retries
- Dead Letter Queues (DLQ)
- Delays up to 12 hours

**Use cases:** Async processing, API buffering, rate limiting, event workflows, deferred jobs

## Quick Start

```bash
wrangler queues create my-queue
wrangler queues consumer add my-queue my-worker
```

```typescript
// Producer
await env.MY_QUEUE.send({ userId: 123, action: 'notify' });

// Consumer (with proper error handling)
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const msg of batch.messages) {
      try {
        await process(msg.body);
        msg.ack();
      } catch (error) {
        msg.retry({ delaySeconds: 60 });
      }
    }
  }
};
```

## Critical Warnings

**Before using Queues, understand these production mistakes:**

1. **Uncaught errors retry ENTIRE batch** (not just failed message). Always use per-message try/catch.
2. **Messages not ack'd/retry'd will auto-retry forever** until max_retries. Always explicitly handle each message.

See [gotchas.md](./gotchas.md) for detailed solutions.

## Core Operations

| Operation | Purpose | Limit |
|-----------|---------|-------|
| `send(body, options?)` | Publish message | 128 KB |
| `sendBatch(messages)` | Bulk publish | 100 msgs/256 KB |
| `message.ack()` | Acknowledge success | - |
| `message.retry(options?)` | Retry with delay | - |
| `batch.ackAll()` | Ack entire batch | - |

## Architecture

```
[Producer Worker] → [Queue] → [Consumer Worker/HTTP] → [Processing]
```

- Max 10,000 queues per account
- 5,000 msgs/second per queue
- 4-14 day retention (configurable)

## Reading Order

**New to Queues?** Start here:
1. [configuration.md](./configuration.md) - Set up queues, bindings, consumers
2. [api.md](./api.md) - Send messages, handle batches, ack/retry patterns
3. [patterns.md](./patterns.md) - Real-world examples and integrations
4. [gotchas.md](./gotchas.md) - Critical warnings and troubleshooting

**Task-based routing:**
- Setup queue → [configuration.md](./configuration.md)
- Send/receive messages → [api.md](./api.md)
- Implement specific pattern → [patterns.md](./patterns.md)
- Debug/troubleshoot → [gotchas.md](./gotchas.md)

## In This Reference

- [configuration.md](./configuration.md) - wrangler.jsonc setup, producer/consumer config, DLQ, content types
- [api.md](./api.md) - Send/batch methods, queue handler, ack/retry rules, type-safe patterns
- [patterns.md](./patterns.md) - Async tasks, buffering, rate limiting, D1/Workflows/DO integrations
- [gotchas.md](./gotchas.md) - Critical batch error handling, idempotency, error classification

## See Also

- [workers](../workers/) - Worker runtime for producers/consumers
- [r2](../r2/) - Process R2 event notifications via queues
- [d1](../d1/) - Batch write to D1 from queue consumers

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
