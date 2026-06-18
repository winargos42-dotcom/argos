---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/zaraz/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\zaraz\patterns.md
source_ext: .md
source_sha256: 53424f7c8fb430901ecf1e832fa0152e8a69436fa2e7cb288d7d6a2a1506dd11
text_sha256: 2ea1d00fe81b1e881c00090fd18c96d8c78ebb41fcc55f540b68150320d90d17
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:38
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/zaraz/patterns.md`
- Extract: `text`
- SHA256: `53424f7c8fb430901ecf1e832fa0152e8a69436fa2e7cb288d7d6a2a1506dd11`

## Content

# Zaraz Patterns

## SPA Tracking

**History Change Trigger (Recommended):** Configure in dashboard - no code needed, Zaraz auto-detects route changes.

**Manual tracking (React/Vue/Next.js):**
```javascript
// On route change
zaraz.track('pageview', { page_path: pathname, page_title: document.title });
```

## User Identification

```javascript
// Login
zaraz.set({ userId: user.id, email: user.email, plan: user.plan });
zaraz.track('login', { method: 'oauth' });

// Logout - set to null (cannot clear)
zaraz.set('userId', null);
```

## E-commerce Funnel

| Event | Method |
|-------|--------|
| View | `zaraz.ecommerce('Product Viewed', { product_id, name, price })` |
| Add to cart | `zaraz.ecommerce('Product Added', { product_id, quantity })` |
| Checkout | `zaraz.ecommerce('Checkout Started', { cart_id, products: [...] })` |
| Purchase | `zaraz.ecommerce('Order Completed', { order_id, total, products })` |

## A/B Testing

```javascript
zaraz.set('experiment_checkout', variant);
zaraz.track('experiment_viewed', { experiment_id: 'checkout', variant });
// On conversion
zaraz.track('experiment_conversion', { experiment_id, variant, value });
```

## Worker Integration

**Context Enricher** - Modify context before tools execute:
```typescript
export default {
  async fetch(request, env) {
    const body = await request.json();
    body.system.userRegion = request.cf?.region;
    return Response.json(body);
  }
};
```
Configure: Zaraz > Settings > Context Enrichers

**Worker Variables** - Compute dynamic values server-side, use as `{{worker.variable_name}}`.

## GTM Migration

| GTM | Zaraz |
|-----|-------|
| `dataLayer.push({event: 'purchase'})` | `zaraz.ecommerce('Order Completed', {...})` |
| `{{Page URL}}` | `{{system.page.url}}` |
| `{{Page Title}}` | `{{system.page.title}}` |
| Page View trigger | Pageview trigger |
| Click trigger | Click (selector: `*`) |

## Best Practices

1. Use dashboard triggers over inline code
2. Enable History Change for SPAs (no manual code)
3. Debug with `zaraz.debug = true`
4. Implement consent early (GDPR/CCPA)
5. Use Context Enrichers for sensitive/server data

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
