---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/web-analytics/integration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\web-analytics\integration.md
source_ext: .md
source_sha256: 6c6b8025c5690e9b09b7dbf496b35c7d5f6654f2ea19c46ce06ccd5493b6428d
text_sha256: a0dbfd1a658252e25d7ffa86180c691c6976265526b36ab14ce9e4b469d95cba
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# integration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/web-analytics/integration.md`
- Extract: `text`
- SHA256: `6c6b8025c5690e9b09b7dbf496b35c7d5f6654f2ea19c46ce06ccd5493b6428d`

## Content

# Framework Integration

**Web Analytics is dashboard-only** - no programmatic API. This covers beacon integration.

## Basic HTML

```html
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' 
        data-cf-beacon='{"token": "YOUR_TOKEN", "spa": true}'></script>
```

Place before closing `</body>` tag.

## Framework Examples

| Framework | Location | Notes |
|-----------|----------|-------|
| React/Vite | `public/index.html` | Add `spa: true` |
| Next.js App Router | `app/layout.tsx` | Use `<Script strategy="afterInteractive">` |
| Next.js Pages | `pages/_document.tsx` | Use `<Script>` |
| Nuxt 3 | `app.vue` with `useHead()` | Or use plugin |
| Vue 3/Vite | `index.html` | Add `spa: true` |
| Gatsby | `gatsby-browser.js` | `onClientEntry` hook |
| SvelteKit | `src/app.html` | Before `</body>` |
| Astro | Layout component | Before `</body>` |
| Angular | `src/index.html` | Add `spa: true` |
| Docusaurus | `docusaurus.config.js` | In `scripts` array |

## Configuration

```json
{
  "token": "YOUR_TOKEN",
  "spa": true
}
```

**Use `spa: true` for:** React Router, Vue Router, Next.js, Nuxt, Gatsby, SvelteKit, Angular

**Use `spa: false` for:** Traditional server-rendered (PHP, Django, Rails, WordPress)

## CSP Headers

```
script-src 'self' https://static.cloudflareinsights.com;
connect-src 'self' https://cloudflareinsights.com;
```

## GDPR Consent

```typescript
// Load conditionally based on consent
if (localStorage.getItem('analytics-consent') === 'true') {
  const script = document.createElement('script');
  script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
  script.defer = true;
  script.setAttribute('data-cf-beacon', '{"token": "YOUR_TOKEN", "spa": true}');
  document.body.appendChild(script);
}
```

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
