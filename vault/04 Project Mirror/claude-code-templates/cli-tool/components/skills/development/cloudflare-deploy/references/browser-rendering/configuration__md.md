---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/browser-rendering/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\browser-rendering\configuration.md
source_ext: .md
source_sha256: 5f7eb283ebc46411450f6004f39a122597032f9101c07448f5733dcad4fbb73c
text_sha256: db9206a7f14bf13d5f8ade9875927662796016c52b0221b54c3e08238890b952
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/browser-rendering/configuration.md`
- Extract: `text`
- SHA256: `5f7eb283ebc46411450f6004f39a122597032f9101c07448f5733dcad4fbb73c`

## Content

# Configuration & Setup

## Installation

```bash
npm install @cloudflare/puppeteer  # or @cloudflare/playwright
```

**Use Cloudflare packages** - standard `puppeteer`/`playwright` won't work in Workers.

## wrangler.json

```json
{
  "name": "browser-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "browser": {
    "binding": "MYBROWSER"
  }
}
```

**Required:** `nodejs_compat` flag and `browser.binding`.

## TypeScript

```typescript
interface Env {
  MYBROWSER: Fetcher;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // ...
  }
} satisfies ExportedHandler<Env>;
```

## Development

```bash
wrangler dev --remote  # --remote required for browser binding
```

**Local mode does NOT support Browser Rendering** - must use `--remote`.

## REST API

No wrangler config needed. Get API token with "Browser Rendering - Edit" permission.

```bash
curl -X POST \
  'https://api.cloudflare.com/client/v4/accounts/{accountId}/browser-rendering/screenshot' \
  -H 'Authorization: Bearer TOKEN' \
  -d '{"url": "https://example.com"}' --output screenshot.png
```

## Requirements

| Requirement | Value |
|-------------|-------|
| Node.js compatibility | `nodejs_compat` flag |
| Compatibility date | 2023-03-01+ |
| Module format | ES modules only |
| Browser | Chromium 119+ (no Firefox/Safari) |

**Not supported:** WebGL, WebRTC, extensions, `file://` protocol, Service Worker syntax.

## Troubleshooting

| Error | Solution |
|-------|----------|
| `MYBROWSER is undefined` | Use `wrangler dev --remote` |
| `nodejs_compat not enabled` | Add to `compatibility_flags` |
| `Module not found` | `npm install @cloudflare/puppeteer` |
| `Browser Rendering not available` | Enable in dashboard |

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
