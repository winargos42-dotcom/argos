---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/images/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\images\README.md
source_ext: .md
source_sha256: 6d1564e69130323a713da087b288ac503ba71eb47831d70877486127da59e63d
text_sha256: 2df48cf4d8d5269c55a2c2e94ec331c576200db80cb33bdb3f08f104fee88676
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/images/README.md`
- Extract: `text`
- SHA256: `6d1564e69130323a713da087b288ac503ba71eb47831d70877486127da59e63d`

## Content

# Cloudflare Images Skill Reference

**Cloudflare Images** is an end-to-end image management solution providing storage, transformation, optimization, and delivery at scale via Cloudflare's global network.

## Quick Decision Tree

**Need to:**
- **Transform in Worker?** → [api.md](api.md#workers-binding-api-2026-primary-method) (Workers Binding API)
- **Upload from Worker?** → [api.md](api.md#upload-from-worker) (REST API)
- **Upload from client?** → [patterns.md](patterns.md#upload-from-client-direct-creator-upload) (Direct Creator Upload)
- **Set up variants?** → [configuration.md](configuration.md#variants-configuration)
- **Serve responsive images?** → [patterns.md](patterns.md#responsive-images)
- **Add watermarks?** → [patterns.md](patterns.md#watermarking)
- **Fix errors?** → [gotchas.md](gotchas.md#common-errors)

## Reading Order

**For building image upload/transform feature:**
1. [configuration.md](configuration.md) - Setup Workers binding
2. [api.md](api.md#workers-binding-api-2026-primary-method) - Learn transform API
3. [patterns.md](patterns.md#upload-from-client-direct-creator-upload) - Direct upload pattern
4. [gotchas.md](gotchas.md) - Check limits and errors

**For URL-based transforms:**
1. [configuration.md](configuration.md#variants-configuration) - Create variants
2. [api.md](api.md#url-transform-api) - URL syntax
3. [patterns.md](patterns.md#responsive-images) - Responsive patterns

**For troubleshooting:**
1. [gotchas.md](gotchas.md#common-errors) - Error messages
2. [gotchas.md](gotchas.md#limits) - Size/format limits

## Core Methods

| Method | Use Case | Location |
|--------|----------|----------|
| `env.IMAGES.input().transform()` | Transform in Worker | [api.md:11](api.md) |
| REST API `/images/v1` | Upload images | [api.md:57](api.md) |
| Direct Creator Upload | Client-side upload | [api.md:127](api.md) |
| URL transforms | Static image delivery | [api.md:112](api.md) |

## In This Reference

- **[api.md](api.md)** - Complete API: Workers binding, REST endpoints, URL transforms
- **[configuration.md](configuration.md)** - Setup: wrangler.toml, variants, auth, signed URLs
- **[patterns.md](patterns.md)** - Patterns: responsive images, watermarks, format negotiation, caching
- **[gotchas.md](gotchas.md)** - Troubleshooting: limits, errors, best practices

## Key Features

- **Automatic Optimization** - AVIF/WebP format negotiation
- **On-the-fly Transforms** - Resize, crop, blur, sharpen via URL or API
- **Workers Binding** - Transform images in Workers (2026 primary method)
- **Direct Upload** - Secure client-side uploads without backend proxy
- **Global Delivery** - Cached at 300+ Cloudflare data centers
- **Watermarking** - Overlay images programmatically

## See Also

- [Official Docs](https://developers.cloudflare.com/images/)
- [Workers Examples](https://developers.cloudflare.com/images/tutorials/)

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
