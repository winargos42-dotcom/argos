---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/images/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\images\configuration.md
source_ext: .md
source_sha256: 3d6b121f9cd311774f3b3889b6e4ebe2bf35ca6a04f4200bac50054b927df72c
text_sha256: e4c66bfcbf49b9c0cef84d66c7f8b49ce4520c92190661d13c409eaa0825c8f2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/images/configuration.md`
- Extract: `text`
- SHA256: `3d6b121f9cd311774f3b3889b6e4ebe2bf35ca6a04f4200bac50054b927df72c`

## Content

# Configuration

## Wrangler Integration

### Workers Binding Setup

Add to `wrangler.toml`:

```toml
name = "my-image-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[images]
binding = "IMAGES"
```

Access in Worker:

```typescript
interface Env {
  IMAGES: ImageBinding;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return await env.IMAGES
      .input(imageBuffer)
      .transform({ width: 800 })
      .output()
      .response();
  }
};
```

### Upload via Script

Wrangler doesn't have built-in Images commands, use REST API:

```typescript
// scripts/upload-image.ts
import fs from 'fs';
import FormData from 'form-data';

async function uploadImage(filePath: string) {
  const accountId = process.env.CLOUDFLARE_ACCOUNT_ID!;
  const apiToken = process.env.CLOUDFLARE_API_TOKEN!;
  
  const formData = new FormData();
  formData.append('file', fs.createReadStream(filePath));
  
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${accountId}/images/v1`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiToken}`,
      },
      body: formData,
    }
  );
  
  const result = await response.json();
  console.log('Uploaded:', result);
}

uploadImage('./photo.jpg');
```

### Environment Variables

Store account hash for URL construction:

```toml
[vars]
IMAGES_ACCOUNT_HASH = "your-account-hash"
ACCOUNT_ID = "your-account-id"
```

Access in Worker:

```typescript
const imageUrl = `https://imagedelivery.net/${env.IMAGES_ACCOUNT_HASH}/${imageId}/public`;
```

## Variants Configuration

Variants are named presets for transformations.

### Create Variant (Dashboard)

1. Navigate to Images → Variants
2. Click "Create Variant"
3. Set name (e.g., `thumbnail`)
4. Configure: `width=200,height=200,fit=cover`

### Create Variant (API)

```bash
curl -X POST \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1/variants \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "thumbnail",
    "options": {
      "width": 200,
      "height": 200,
      "fit": "cover"
    },
    "neverRequireSignedURLs": true
  }'
```

### Use Variant

```
https://imagedelivery.net/{account_hash}/{image_id}/thumbnail
```

### Common Variant Presets

```json
{
  "thumbnail": {
    "width": 200,
    "height": 200,
    "fit": "cover"
  },
  "avatar": {
    "width": 128,
    "height": 128,
    "fit": "cover",
    "gravity": "face"
  },
  "hero": {
    "width": 1920,
    "height": 1080,
    "fit": "cover",
    "quality": 90
  },
  "mobile": {
    "width": 640,
    "fit": "scale-down",
    "quality": 80,
    "format": "avif"
  }
}
```

## Authentication

### API Token (Recommended)

Generate at: Dashboard → My Profile → API Tokens

Required permissions:
- Account → Cloudflare Images → Edit

```bash
curl -H "Authorization: Bearer {api_token}" \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1
```

### API Key (Legacy)

```bash
curl -H "X-Auth-Email: {email}" \
     -H "X-Auth-Key: {api_key}" \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1
```

## Signed URLs

For private images, enable signed URLs:

```bash
# Upload with signed URLs required
curl -X POST \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1 \
  -H "Authorization: Bearer {api_token}" \
  -F file=@private.jpg \
  -F requireSignedURLs=true
```

Generate signed URL:

```typescript
import { createHmac } from 'crypto';

function signUrl(imageId: string, variant: string, expiry: number, key: string): string {
  const path = `/${imageId}/${variant}`;
  const toSign = `${path}${expiry}`;
  const signature = createHmac('sha256', key)
    .update(toSign)
    .digest('hex');
  
  return `https://imagedelivery.net/{hash}${path}?exp=${expiry}&sig=${signature}`;
}

// Sign URL valid for 1 hour
const signedUrl = signUrl('image-id', 'public', Date.now() + 3600, env.SIGNING_KEY);
```

## Local Development

```bash
npx wrangler dev --remote
```

Must use `--remote` for Images binding access.

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
