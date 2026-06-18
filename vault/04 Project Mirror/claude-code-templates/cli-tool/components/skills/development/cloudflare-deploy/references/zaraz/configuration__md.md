---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/zaraz/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\zaraz\configuration.md
source_ext: .md
source_sha256: 09bf49fd221093f7761339086cc14893efa6673a2982009ec0b01f907c5e33b2
text_sha256: 6f3666ac64d1b36b4a708b3dea9d3b1d9679b34c58a00e3ca8e254edd602418a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:38
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/zaraz/configuration.md`
- Extract: `text`
- SHA256: `09bf49fd221093f7761339086cc14893efa6673a2982009ec0b01f907c5e33b2`

## Content

# Zaraz Configuration

## Dashboard Setup

1. Domain → Zaraz → Start setup
2. Add tool (e.g., Google Analytics 4)
3. Enter credentials (GA4: `G-XXXXXXXXXX`)
4. Configure triggers
5. Save and Publish

## Triggers

| Type | When | Use Case |
|------|------|----------|
| Pageview | Page load | Track page views |
| Click | Element clicked | Button tracking |
| Form Submission | Form submitted | Lead capture |
| History Change | URL changes (SPA) | React/Vue routing |
| Variable Match | Custom condition | Conditional firing |

### History Change (SPA)

```
Type: History Change
Event: pageview
```

Fires on `pushState`, `replaceState`, hash changes. **No manual tracking needed.**

### Click Trigger

```
Type: Click
CSS Selector: .buy-button
Event: purchase_intent
Properties:
  button_text: {{system.clickElement.text}}
```

## Tool Configuration

**GA4:**
```
Measurement ID: G-XXXXXXXXXX
Events: page_view, purchase, user_engagement
```

**Facebook Pixel:**
```
Pixel ID: 1234567890123456
Events: PageView, Purchase, AddToCart
```

**Google Ads:**
```
Conversion ID: AW-XXXXXXXXX
Conversion Label: YYYYYYYYYY
```

## Consent Management

1. Settings → Consent → Create purposes (analytics, marketing)
2. Map tools to purposes
3. Set behavior: "Do not load until consent granted"

**Programmatic consent:**
```javascript
zaraz.consent.setAll({ analytics: true, marketing: true });
```

## Privacy Features

| Feature | Default |
|---------|---------|
| IP Anonymization | Enabled |
| Cookie Control | Via consent purposes |
| GDPR/CCPA | Consent modal |

## Testing

1. **Preview Mode** - test without publishing
2. **Debug Mode** - `zaraz.debug = true`
3. **Network tab** - filter "zaraz"

## Limits

| Resource | Limit |
|----------|-------|
| Event properties | 100KB |
| Consent purposes | 20 |

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
