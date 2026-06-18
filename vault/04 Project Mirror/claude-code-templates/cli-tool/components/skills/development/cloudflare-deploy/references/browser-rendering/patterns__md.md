---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/browser-rendering/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\browser-rendering\patterns.md
source_ext: .md
source_sha256: 628cffb203727686e3f5256b4bc44afe738d645b805285a56afdf9320222884a
text_sha256: ed518864d14d821619b23d0a6e4fe0b39b64c8da98ad17d3da07b4b42d35c161
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/browser-rendering/patterns.md`
- Extract: `text`
- SHA256: `628cffb203727686e3f5256b4bc44afe738d645b805285a56afdf9320222884a`

## Content

# Browser Rendering Patterns

## Basic Worker

```typescript
import puppeteer from "@cloudflare/puppeteer";

export default {
  async fetch(request, env) {
    const browser = await puppeteer.launch(env.MYBROWSER);
    try {
      const page = await browser.newPage();
      await page.goto("https://example.com");
      return new Response(await page.content());
    } finally {
      await browser.close(); // ALWAYS in finally
    }
  }
};
```

## Session Reuse

Keep sessions alive for performance:
```typescript
let sessionId = await env.SESSION_KV.get("browser-session");
if (sessionId) {
  browser = await puppeteer.connect(env.MYBROWSER, sessionId);
} else {
  browser = await puppeteer.launch(env.MYBROWSER, { keep_alive: 600000 });
  await env.SESSION_KV.put("browser-session", browser.sessionId(), { expirationTtl: 600 });
}
// Don't close browser to keep session alive
```

## Common Operations

| Task | Code |
|------|------|
| Screenshot | `await page.screenshot({ type: "png", fullPage: true })` |
| PDF | `await page.pdf({ format: "A4", printBackground: true })` |
| Extract data | `await page.evaluate(() => document.querySelector('h1').textContent)` |
| Fill form | `await page.type('#input', 'value'); await page.click('button')` |
| Wait nav | `await Promise.all([page.waitForNavigation(), page.click('a')])` |

## Parallel Scraping

```typescript
const pages = await Promise.all(urls.map(() => browser.newPage()));
await Promise.all(pages.map((p, i) => p.goto(urls[i])));
const titles = await Promise.all(pages.map(p => p.title()));
```

## Playwright Selectors

```typescript
import { launch } from "@cloudflare/playwright";
const browser = await launch(env.MYBROWSER);
await page.getByRole("button", { name: "Sign in" }).click();
await page.getByLabel("Email").fill("user@example.com");
await page.getByTestId("submit-button").click();
```

## Incognito Contexts

Isolated sessions without multiple browsers:
```typescript
const ctx1 = await browser.createIncognitoBrowserContext();
const ctx2 = await browser.createIncognitoBrowserContext();
// Each has isolated cookies/storage
```

## Quota Check

```typescript
const limits = await puppeteer.limits(env.MYBROWSER);
if (limits.remaining < 60000) return new Response("Quota low", { status: 429 });
```

## Error Handling

```typescript
try {
  await page.goto(url, { timeout: 30000, waitUntil: "networkidle0" });
} catch (e) {
  if (e.message.includes("timeout")) return new Response("Timeout", { status: 504 });
  if (e.message.includes("Session limit")) return new Response("Too many sessions", { status: 429 });
} finally {
  if (browser) await browser.close();
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
