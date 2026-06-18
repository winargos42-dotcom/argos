---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/images/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\images\patterns.md
source_ext: .md
source_sha256: 9464be3d6c7dbd0c0c981cf6510cdfbb89c17615cfc87f9d1939ef30e5fcbb9b
text_sha256: b1cfebd7afdd7024e581e4a1002a304af0c00e630d4cd4623e97caae1c02fcd1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/images/patterns.md`
- Extract: `text`
- SHA256: `9464be3d6c7dbd0c0c981cf6510cdfbb89c17615cfc87f9d1939ef30e5fcbb9b`

## Content

# Common Patterns

## URL Transform Options

```
width=<PX>   height=<PX>   fit=scale-down|contain|cover|crop|pad
quality=85   format=auto|webp|avif|jpeg|png   dpr=2
gravity=auto|face|left|right|top|bottom   sharpen=2   blur=10
rotate=90|180|270   background=white   metadata=none|copyright|keep
```

## Responsive Images (srcset)

```html
<img src="https://imagedelivery.net/{hash}/{id}/width=800"
  srcset=".../{id}/width=400 400w, .../{id}/width=800 800w, .../{id}/width=1200 1200w"
  sizes="(max-width: 600px) 400px, 800px" />
```

## Format Negotiation

```typescript
async fetch(request: Request, env: Env): Promise<Response> {
  const accept = request.headers.get('Accept') || '';
  const format = /image\/avif/.test(accept) ? 'avif' : /image\/webp/.test(accept) ? 'webp' : 'jpeg';
  return env.IMAGES.input(buffer).transform({ format, quality: 85 }).output().response();
}
```

## Direct Creator Upload

```typescript
// Backend: Generate upload URL
const response = await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/images/v2/direct_upload`,
  { method: 'POST', headers: { 'Authorization': `Bearer ${env.API_TOKEN}` },
    body: JSON.stringify({ requireSignedURLs: false, metadata: { userId } }) }
);

// Frontend: Upload to returned uploadURL
const formData = new FormData();
formData.append('file', file);
await fetch(result.uploadURL, { method: 'POST', body: formData });
// Use: https://imagedelivery.net/{hash}/${result.id}/public
```

## Transform & Store to R2

```typescript
async fetch(request: Request, env: Env): Promise<Response> {
  const file = (await request.formData()).get('image') as File;
  const transformed = await env.IMAGES
    .input(await file.arrayBuffer())
    .transform({ width: 800, format: 'avif', quality: 80 })
    .output();
  await env.R2.put(`images/${Date.now()}.avif`, transformed.response().body);
  return Response.json({ success: true });
}
```

## Watermarking

```typescript
const watermark = await env.ASSETS.fetch(new URL('/watermark.png', request.url));
const result = await env.IMAGES
  .input(await image.arrayBuffer())
  .draw(env.IMAGES.input(watermark.body).transform({ width: 100 }), { bottom: 20, right: 20, opacity: 0.7 })
  .transform({ format: 'avif' })
  .output();
return result.response();
```

## Device-Based Transforms

```typescript
const ua = request.headers.get('User-Agent') || '';
const isMobile = /Mobile|Android|iPhone/i.test(ua);
return env.IMAGES.input(buffer)
  .transform({ width: isMobile ? 400 : 1200, quality: isMobile ? 75 : 85, format: 'avif' })
  .output().response();
```

## Caching Strategy

```typescript
async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
  const cache = caches.default;
  let response = await cache.match(request);
  if (!response) {
    response = await env.IMAGES.input(buffer).transform({ width: 800, format: 'avif' }).output().response();
    response = new Response(response.body, { headers: { ...response.headers, 'Cache-Control': 'public, max-age=86400' } });
    ctx.waitUntil(cache.put(request, response.clone()));
  }
  return response;
}
```

## Batch Processing

```typescript
const results = await Promise.all(images.map(buffer =>
  env.IMAGES.input(buffer).transform({ width: 800, fit: 'cover', format: 'avif' }).output()
));
```

## Error Handling

```typescript
try {
  return (await env.IMAGES.input(buffer).transform({ width: 800 }).output()).response();
} catch (error) {
  console.error('Transform failed:', error);
  return new Response('Image processing failed', { status: 500 });
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
