---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/images/api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\images\api.md
source_ext: .md
source_sha256: aa120b76ed5511c9e1b3fb2b63ef08dd7c298009065e0a666d8b1d1c8101f33a
text_sha256: 92c62bd77b133bf58287e93f12dced76725c0dc699b28ecad2acdae709ceea3c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# api.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/images/api.md`
- Extract: `text`
- SHA256: `aa120b76ed5511c9e1b3fb2b63ef08dd7c298009065e0a666d8b1d1c8101f33a`

## Content

# API Reference

## Workers Binding API

```toml
# wrangler.toml
[images]
binding = "IMAGES"
```

### Transform Images

```typescript
const imageResponse = await env.IMAGES
  .input(fileBuffer)
  .transform({ width: 800, height: 600, fit: "cover", quality: 85, format: "avif" })
  .output();
return imageResponse.response();
```

### Transform Options

```typescript
interface TransformOptions {
  width?: number;        height?: number;
  fit?: "scale-down" | "contain" | "cover" | "crop" | "pad";
  quality?: number;      // 1-100
  format?: "avif" | "webp" | "jpeg" | "png";
  dpr?: number;          // 1-3
  gravity?: "auto" | "left" | "right" | "top" | "bottom" | "face" | string;
  sharpen?: number;      // 0-10
  blur?: number;         // 1-250
  rotate?: 90 | 180 | 270;
  background?: string;   // CSS color for pad
  metadata?: "none" | "copyright" | "keep";
  brightness?: number;   contrast?: number;   gamma?: number;  // 0-2
}
```

### Draw/Watermark

```typescript
await env.IMAGES.input(baseImage)
  .draw(env.IMAGES.input(watermark).transform({ width: 100 }), { top: 10, left: 10, opacity: 0.8 })
  .output();
```

## REST API

### Upload Image

```bash
curl -X POST https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1 \
  -H "Authorization: Bearer {token}" -F file=@image.jpg -F metadata='{"key":"value"}'
```

### Other Operations

```bash
GET  /accounts/{account_id}/images/v1/{image_id}      # Get details
DELETE /accounts/{account_id}/images/v1/{image_id}   # Delete
GET  /accounts/{account_id}/images/v1?page=1         # List
```

## URL Transform API

```
https://imagedelivery.net/{hash}/{id}/width=800,height=600,fit=cover,format=avif
```

**Params:** `w=`, `h=`, `fit=`, `q=`, `f=`, `dpr=`, `gravity=`, `sharpen=`, `blur=`, `rotate=`, `background=`, `metadata=`

## Direct Creator Upload

```typescript
// 1. Get upload URL (backend)
const { result } = await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${accountId}/images/v2/direct_upload`,
  { method: 'POST', headers: { 'Authorization': `Bearer ${token}` },
    body: JSON.stringify({ requireSignedURLs: false }) }
).then(r => r.json());

// 2. Client uploads to result.uploadURL
const formData = new FormData();
formData.append('file', file);
await fetch(result.uploadURL, { method: 'POST', body: formData });
```

## Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 5400 | Invalid format | Use JPEG, PNG, GIF, WebP |
| 5401 | Too large | Max 100MB |
| 5403 | Invalid transform | Check params |
| 9413 | Rate limit | Implement backoff |

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
