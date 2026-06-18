---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workflows/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\workflows\README.md
source_ext: .md
source_sha256: 0c70e46ac2cde6386e4686451355207f71f569996f59c1d757efafc5693fe7d5
text_sha256: c0a6be8e49bc081474ad24ec4c1f6ec190c2e431c2d30869e0b5a047b4a25c3f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:38
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/workflows/README.md`
- Extract: `text`
- SHA256: `0c70e46ac2cde6386e4686451355207f71f569996f59c1d757efafc5693fe7d5`

## Content

# Cloudflare Workflows

Durable multi-step applications with automatic retries, state persistence, and long-running execution.

## What It Does

- Chain steps with automatic retry logic
- Persist state between steps (minutes → weeks)
- Handle failures without losing progress
- Wait for external events/approvals
- Sleep without consuming resources

**Available:** Free & Paid Workers plans

## Core Concepts

**Workflow**: Class extending `WorkflowEntrypoint` with `run` method
**Instance**: Single execution with unique ID & independent state
**Steps**: Independently retriable units via `step.do()` - API calls, DB queries, AI invocations
**State**: Persisted from step returns; step name = cache key

## Quick Start

```typescript
import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from 'cloudflare:workers';

type Env = { MY_WORKFLOW: Workflow; DB: D1Database };
type Params = { userId: string };

export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const user = await step.do('fetch user', async () => {
      return await this.env.DB.prepare('SELECT * FROM users WHERE id = ?')
        .bind(event.params.userId).first();
    });
    
    await step.sleep('wait 7 days', '7 days');
    
    await step.do('send reminder', async () => {
      await sendEmail(user.email, 'Reminder!');
    });
  }
}
```

## Key Features

- **Durability**: Failed steps don't re-run successful ones
- **Retries**: Configurable backoff (constant/linear/exponential)
- **Events**: `waitForEvent()` for webhooks/approvals (timeout: 1h → 365d)
- **Sleep**: `sleep()` / `sleepUntil()` for scheduling (max 365d)
- **Parallel**: `Promise.all()` for concurrent steps
- **Idempotency**: Check-then-execute patterns

## Reading Order

**Getting Started:** configuration.md → api.md → patterns.md  
**Troubleshooting:** gotchas.md

## In This Reference
- [configuration.md](./configuration.md) - wrangler.jsonc setup, step config, bindings
- [api.md](./api.md) - Step APIs, instance management, sleep/parameters
- [patterns.md](./patterns.md) - Common workflows, testing, orchestration
- [gotchas.md](./gotchas.md) - Timeouts, limits, debugging strategies

## See Also
- [durable-objects](../durable-objects/) - Alternative stateful approach
- [queues](../queues/) - Message-driven workflows
- [workers](../workers/) - Entry point for workflow instances

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
