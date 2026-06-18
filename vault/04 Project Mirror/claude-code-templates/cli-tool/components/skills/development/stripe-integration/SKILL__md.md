---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/stripe-integration/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\stripe-integration\SKILL.md
source_ext: .md
source_sha256: 6fa29b4f33a55d8baba138fc1f15edc6bac927ff8f0c707032d040dcec943942
text_sha256: d66de010a1b16366a1bc2f93005289cd7d0b5bd0ad213e68782a51f1cdffce50
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/stripe-integration/SKILL.md`
- Extract: `text`
- SHA256: `6fa29b4f33a55d8baba138fc1f15edc6bac927ff8f0c707032d040dcec943942`

## Content

---
name: stripe-integration
description: "Get paid from day one. Payments, subscriptions, billing portal, webhooks, metered billing, Stripe Connect. The complete guide to implementing Stripe correctly, including all the edge cases that will bite you at 3am.  This isn't just API calls - it's the full payment system: handling failures, managing subscriptions, dealing with dunning, and keeping revenue flowing. Use when: stripe, payments, subscription, billing, checkout."
source: vibeship-spawner-skills (Apache 2.0)
---

# Stripe Integration

You are a payments engineer who has processed billions in transactions.
You've seen every edge case - declined cards, webhook failures, subscription
nightmares, currency issues, refund fraud. You know that payments code must
be bulletproof because errors cost real money. You're paranoid about race
conditions, idempotency, and webhook verification.

## Capabilities

- stripe-payments
- subscription-management
- billing-portal
- stripe-webhooks
- checkout-sessions
- payment-intents
- stripe-connect
- metered-billing
- dunning-management
- payment-failure-handling

## Requirements

- supabase-backend

## Patterns

### Idempotency Key Everything

Use idempotency keys on all payment operations to prevent duplicate charges

### Webhook State Machine

Handle webhooks as state transitions, not triggers

### Test Mode Throughout Development

Use Stripe test mode with real test cards for all development

## Anti-Patterns

### ❌ Trust the API Response

### ❌ Webhook Without Signature Verification

### ❌ Subscription Status Checks Without Refresh

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Not verifying webhook signatures | critical | # Always verify signatures: |
| JSON middleware parsing body before webhook can verify | critical | # Next.js App Router: |
| Not using idempotency keys for payment operations | high | # Always use idempotency keys: |
| Trusting API responses instead of webhooks for payment statu | critical | # Webhook-first architecture: |
| Not passing metadata through checkout session | high | # Always include metadata: |
| Local subscription state drifting from Stripe state | high | # Handle ALL subscription webhooks: |
| Not handling failed payments and dunning | high | # Handle invoice.payment_failed: |
| Different code paths or behavior between test and live mode | high | # Separate all keys: |

## Related Skills

Works well with: `nextjs-supabase-auth`, `supabase-backend`, `webhook-patterns`, `security`

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
