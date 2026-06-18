---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/shopify-apps/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\shopify-apps\SKILL.md
source_ext: .md
source_sha256: 5cebc8ff0de76ee091049fa9452ed670517d23e35c58e2fc0e193088fcc1e28a
text_sha256: 679500db2c08248327bc4f41ab3f317c21ccbdc8e21ae128283b0218cfb66f5d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/shopify-apps/SKILL.md`
- Extract: `text`
- SHA256: `5cebc8ff0de76ee091049fa9452ed670517d23e35c58e2fc0e193088fcc1e28a`

## Content

---
name: shopify-apps
description: "Expert patterns for Shopify app development including Remix/React Router apps, embedded apps with App Bridge, webhook handling, GraphQL Admin API, Polaris components, billing, and app extensions. Use when: shopify app, shopify, embedded app, polaris, app bridge."
source: vibeship-spawner-skills (Apache 2.0)
---

# Shopify Apps

## Patterns

### React Router App Setup

Modern Shopify app template with React Router

### Embedded App with App Bridge

Render app embedded in Shopify Admin

### Webhook Handling

Secure webhook processing with HMAC verification

## Anti-Patterns

### ❌ REST API for New Apps

### ❌ Webhook Processing Before Response

### ❌ Polling Instead of Webhooks

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | ## Respond immediately, process asynchronously |
| Issue | high | ## Check rate limit headers |
| Issue | high | ## Request protected customer data access |
| Issue | medium | ## Use TOML only (recommended) |
| Issue | medium | ## Handle both URL formats |
| Issue | high | ## Use GraphQL for all new code |
| Issue | high | ## Use latest App Bridge via script tag |
| Issue | high | ## Implement all GDPR handlers |

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
