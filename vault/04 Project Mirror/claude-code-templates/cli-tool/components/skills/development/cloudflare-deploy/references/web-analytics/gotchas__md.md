---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/web-analytics/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\web-analytics\gotchas.md
source_ext: .md
source_sha256: 31707b6a3db1ae251e5c97cdb9b6e6b0217991422f332199bfd214fb7e809bc7
text_sha256: e81a0ac61dce03a4890b9950ba06662c16e4b9ddb4eecdff204221501cd8d6d5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/web-analytics/gotchas.md`
- Extract: `text`
- SHA256: `31707b6a3db1ae251e5c97cdb9b6e6b0217991422f332199bfd214fb7e809bc7`

## Content

# Web Analytics Gotchas

## Critical Issues

### SPA Navigation Not Tracked

**Symptom:** Only initial pageload counted  
**Fix:** Add `spa: true`:
```html
<script data-cf-beacon='{"token": "TOKEN", "spa": true}' ...></script>
```

### CSP Blocking Beacon

**Symptom:** Console error "Refused to load script"  
**Fix:** Allow both domains:
```
script-src 'self' https://static.cloudflareinsights.com https://cloudflareinsights.com;
```

### Hash-Based Routing Unsupported

**Symptom:** `#/path` URLs not tracked  
**Fix:** Migrate to History API (`BrowserRouter`, not `HashRouter`). No workaround for hash routing.

### No Data Appearing

**Causes & Fixes:**
1. **Delay** - Wait 5-15 minutes
2. **Wrong token** - Verify matches dashboard exactly
3. **Script blocked** - Check DevTools Network tab for beacon.min.js
4. **Domain mismatch** - Dashboard site must match actual URL

### Auto-Injection Fails

**Cause:** `Cache-Control: no-transform` header  
**Fix:** Remove `no-transform` or install beacon manually

### Duplicate Pageviews

**Cause:** Multiple beacon scripts  
**Fix:** Keep only one beacon per page

## Configuration Issues

| Issue | Fix |
|-------|-----|
| 10-site limit reached | Delete old sites or proxy through CF (unlimited) |
| Token not recognized | Use exact alphanumeric token from dashboard |

## Framework-Specific

### Next.js Hydration Warning

```tsx
<script suppressHydrationWarning ... />
```

### Gatsby Window Undefined

Use `gatsby-browser.js` to load client-side only.

## Limits

| Resource | Limit |
|----------|-------|
| Non-proxied sites | 10 |
| Proxied sites | Unlimited |
| Data retention | 6 months |
| Ingestion delay | 5-10 min |
| API access | None (dashboard only) |

## When NOT to Use Web Analytics

Use alternatives if you need:
- Custom event tracking
- Real-time data
- User-level tracking
- Conversion funnels
- Data export/API access

**Web Analytics excels at:** Core Web Vitals, basic traffic, privacy compliance, free unlimited pageviews.

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
