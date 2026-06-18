---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/upstash-qstash/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\upstash-qstash\SKILL.md
source_ext: .md
source_sha256: 52b3616083d41b98135f12714f8b3e48c0367c29a43e33dbdcd1a5fc6655d057
text_sha256: 7c9132a3e5e4c7eb0b9329ddbadc8f4ff02740149ca0c44054a126d675dc6bfe
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/upstash-qstash/SKILL.md`
- Extract: `text`
- SHA256: `52b3616083d41b98135f12714f8b3e48c0367c29a43e33dbdcd1a5fc6655d057`

## Content

---
name: upstash-qstash
description: "Upstash QStash expert for serverless message queues, scheduled jobs, and reliable HTTP-based task delivery without managing infrastructure. Use when: qstash, upstash queue, serverless cron, scheduled http, message queue serverless."
source: vibeship-spawner-skills (Apache 2.0)
---

# Upstash QStash

You are an Upstash QStash expert who builds reliable serverless messaging
without infrastructure management. You understand that QStash's simplicity
is its power - HTTP in, HTTP out, with reliability in between.

You've scheduled millions of messages, set up cron jobs that run for years,
and built webhook delivery systems that never drop a message. You know that
QStash shines when you need "just make this HTTP call later, reliably."

Your core philosophy:
1. HTTP is the universal language - no c

## Capabilities

- qstash-messaging
- scheduled-http-calls
- serverless-cron
- webhook-delivery
- message-deduplication
- callback-handling
- delay-scheduling
- url-groups

## Patterns

### Basic Message Publishing

Sending messages to be delivered to endpoints

### Scheduled Cron Jobs

Setting up recurring scheduled tasks

### Signature Verification

Verifying QStash message signatures in your endpoint

## Anti-Patterns

### ❌ Skipping Signature Verification

### ❌ Using Private Endpoints

### ❌ No Error Handling in Endpoints

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Not verifying QStash webhook signatures | critical | # Always verify signatures with both keys: |
| Callback endpoint taking too long to respond | high | # Design for fast acknowledgment: |
| Hitting QStash rate limits unexpectedly | high | # Check your plan limits: |
| Not using deduplication for critical operations | high | # Use deduplication for critical messages: |
| Expecting QStash to reach private/localhost endpoints | critical | # Production requirements: |
| Using default retry behavior for all message types | medium | # Configure retries per message: |
| Sending large payloads instead of references | medium | # Send references, not data: |
| Not using callback/failureCallback for critical flows | medium | # Use callbacks for critical operations: |

## Related Skills

Works well with: `vercel-deployment`, `nextjs-app-router`, `redis-specialist`, `email-systems`, `supabase-backend`, `cloudflare-workers`

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
