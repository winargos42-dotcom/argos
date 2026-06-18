---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/web-analytics/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\web-analytics\patterns.md
source_ext: .md
source_sha256: 7ec8a759ad26cacb4c76124c28d8cadb61b558e6ad15301ec4c00e4a04eada6c
text_sha256: 6ccd1e334d260b968731f5f613ad28882bc199b72883e3254a52ded8d859f5a8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/web-analytics/patterns.md`
- Extract: `text`
- SHA256: `7ec8a759ad26cacb4c76124c28d8cadb61b558e6ad15301ec4c00e4a04eada6c`

## Content

# Web Analytics Patterns

## Core Web Vitals Debugging

Dashboard → Core Web Vitals → Click metric → Debug View shows top 5 problematic elements.

### LCP Fixes

```html
<!-- Priority hints -->
<img src="hero.jpg" loading="eager" fetchpriority="high" />
<link rel="preload" as="image" href="/hero.jpg" fetchpriority="high" />
```

### CLS Fixes

```css
/* Reserve space */
.ad-container { min-height: 250px; }
img { width: 400px; height: 300px; } /* Explicit dimensions */
```

### INP Fixes

```typescript
// Debounce expensive operations
const handleInput = debounce(search, 300);

// Yield to main thread
await task(); await new Promise(r => setTimeout(r, 0)); await task2();

// Move to Web Worker for heavy computation
```

| Metric | Good | Poor |
|--------|------|------|
| LCP | ≤2.5s | >4s |
| INP | ≤200ms | >500ms |
| CLS | ≤0.1 | >0.25 |

## GDPR Consent

```typescript
// Load beacon only after consent
const consent = localStorage.getItem('analytics-consent');
if (consent === 'accepted') {
  const script = document.createElement('script');
  script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
  script.setAttribute('data-cf-beacon', '{"token": "TOKEN", "spa": true}');
  document.body.appendChild(script);
}
```

Alternative: Dashboard → "Enable, excluding visitor data in the EU"

## SPA Navigation

```html
<!-- REQUIRED for React/Vue/etc routing -->
<script data-cf-beacon='{"token": "TOKEN", "spa": true}' ...></script>
```

Without `spa: true`: only initial pageload tracked.

## Staging/Production Separation

```typescript
// Use env-specific tokens
const token = process.env.NEXT_PUBLIC_CF_ANALYTICS_TOKEN;
// .env.production: production token
// .env.staging: staging token (or empty to disable)
```

## Bot Filtering

Dashboard → Filters → "Exclude Bot Traffic"

Filters: Search crawlers, monitoring services, known bots.  
Not filtered: Headless browsers (Playwright/Puppeteer).

## Ad-Blocker Impact

~25-40% of users may block `cloudflareinsights.com`. No official workaround.
Dashboard shows minimum baseline; use server logs for complete picture.

## Limitations

- No UTM parameter tracking
- No webhooks/alerts/API
- No custom beacon domains
- Max 10 non-proxied sites

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
