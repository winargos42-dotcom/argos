---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/browser-rendering/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\browser-rendering\gotchas.md
source_ext: .md
source_sha256: 1f288dcbc5ee18b3d6d0c7794210acb02f971713d4f8639f7224a52e1c8670e7
text_sha256: 31c3e69294545b1f7f9aecc80c3809521efe3b8d4c36bbc47ba8a693a81460ea
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/browser-rendering/gotchas.md`
- Extract: `text`
- SHA256: `1f288dcbc5ee18b3d6d0c7794210acb02f971713d4f8639f7224a52e1c8670e7`

## Content

# Browser Rendering Gotchas

## Tier Limits

| Limit | Free | Paid |
|-------|------|------|
| Daily browser time | 10 min | Unlimited* |
| Concurrent sessions | 3 | 30 |
| Requests/minute | 6 | 180 |
| Session keep-alive | 10 min max | 10 min max |

*Subject to fair-use policy.

**Check quota:**
```typescript
const limits = await puppeteer.limits(env.MYBROWSER);
// { remaining: 540000, total: 600000, concurrent: 2 }
```

## Always Close Browsers

```typescript
const browser = await puppeteer.launch(env.MYBROWSER);
try {
  const page = await browser.newPage();
  await page.goto("https://example.com");
  return new Response(await page.content());
} finally {
  await browser.close(); // ALWAYS in finally
}
```

**Workers vs REST:** REST auto-closes after timeout. Workers must call `close()` or session stays open until `keep_alive` expires.

## Optimize Concurrency

```typescript
// ❌ 3 sessions (hits free tier limit)
const browser1 = await puppeteer.launch(env.MYBROWSER);
const browser2 = await puppeteer.launch(env.MYBROWSER);

// ✅ 1 session, multiple pages
const browser = await puppeteer.launch(env.MYBROWSER);
const page1 = await browser.newPage();
const page2 = await browser.newPage();
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Session limit exceeded | Too many concurrent | Close unused browsers, use pages not browsers |
| Page navigation timeout | Slow page or `networkidle` on busy page | Increase timeout, use `waitUntil: "load"` |
| Session not found | Expired session | Catch error, launch new session |
| Evaluation failed | DOM element missing | Use `?.` optional chaining |
| Protocol error: Target closed | Page closed during operation | Await all ops before closing |

## page.evaluate() Gotchas

```typescript
// ❌ Outer scope not available
const selector = "h1";
await page.evaluate(() => document.querySelector(selector));

// ✅ Pass as argument
await page.evaluate((sel) => document.querySelector(sel)?.textContent, selector);
```

## Performance

**waitUntil options (fastest to slowest):**
1. `domcontentloaded` - DOM ready
2. `load` - load event (default)
3. `networkidle0` - no network for 500ms

**Block unnecessary resources:**
```typescript
await page.setRequestInterception(true);
page.on("request", (req) => {
  if (["image", "stylesheet", "font"].includes(req.resourceType())) {
    req.abort();
  } else {
    req.continue();
  }
});
```

**Session reuse:** Cold start ~1-2s, warm connect ~100-200ms. Store sessionId in KV for reuse.

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
