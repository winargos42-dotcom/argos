---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/zaraz/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\zaraz\gotchas.md
source_ext: .md
source_sha256: 27a9920b404b5df496f8f5d6825610e13358f842725ea45e6243eca33fe72f05
text_sha256: 30378f48fde6e866780466228a3e698005a9ce23a24188c8ed520195b03eac3e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:38
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/zaraz/gotchas.md`
- Extract: `text`
- SHA256: `27a9920b404b5df496f8f5d6825610e13358f842725ea45e6243eca33fe72f05`

## Content

# Zaraz Gotchas

## Events Not Firing

**Check:**
1. Tool enabled in dashboard (green dot)
2. Trigger conditions met
3. Consent granted for tool's purpose
4. Tool credentials correct (GA4: `G-XXXXXXXXXX`, FB: numeric only)

**Debug:**
```javascript
zaraz.debug = true;
console.log('Tools:', zaraz.tools);
console.log('Consent:', zaraz.consent.getAll());
```

## Consent Issues

**Modal not showing:**
```javascript
// Clear consent cookie
document.cookie = 'zaraz-consent=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
location.reload();
```

**Tools firing before consent:** Map tool to consent purpose with "Do not load until consent granted".

## SPA Tracking

**Route changes not tracked:**
1. Configure History Change trigger in dashboard
2. Hash routing (`#/path`) requires manual tracking:
```javascript
window.addEventListener('hashchange', () => {
  zaraz.track('pageview', { page_path: location.pathname + location.hash });
});
```

**React fix:**
```javascript
const location = useLocation();
useEffect(() => {
  zaraz.track('pageview', { page_path: location.pathname });
}, [location]); // Include dependency
```

## Performance

**Slow page load:**
- Audit tool count (50+ degrades performance)
- Disable blocking triggers unless required
- Reduce event payload size (<100KB)

## Tool-Specific Issues

| Tool | Issue | Fix |
|------|-------|-----|
| GA4 | Events not in real-time | Wait 5-10 min, use DebugView |
| Facebook | Invalid Pixel ID | Use numeric only (no `fbpx_` prefix) |
| Google Ads | Conversions not attributed | Include `send_to: 'AW-XXX/LABEL'` |

## Data Layer

- Properties persist per page only - set on each page load
- Nested access: `{{client.__zarazTrack.user.plan}}`

## Limits

| Resource | Limit |
|----------|-------|
| Request size | 100KB |
| Consent purposes | 20 |
| API rate | 1000 req/sec |

## When NOT to Use Zaraz

- Server-to-server tracking (use Workers)
- Real-time bidirectional communication
- Binary data transmission
- Authentication flows

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
