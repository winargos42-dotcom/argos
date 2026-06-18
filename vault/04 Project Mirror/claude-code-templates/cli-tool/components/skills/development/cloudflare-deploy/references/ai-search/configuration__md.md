---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-search/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ai-search\configuration.md
source_ext: .md
source_sha256: f6b54e16be518896bac6a84f58ed6a9dc45104e733dc6cfe891af04c86f5f256
text_sha256: 59af92d0c3b196bea13ac72e18b42db528721f8971c7d335b27951b77aa4ddb0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-search/configuration.md`
- Extract: `text`
- SHA256: `f6b54e16be518896bac6a84f58ed6a9dc45104e733dc6cfe891af04c86f5f256`

## Content

# AI Search Configuration

## Worker Setup

```jsonc
// wrangler.jsonc
{
  "ai": { "binding": "AI" }
}
```

```typescript
interface Env {
  AI: Ai;
}

const answer = await env.AI.autorag("my-instance").aiSearch({
  query: "How do I configure caching?",
  model: "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
});
```

## Data Sources

### R2 Bucket

Dashboard: AI Search → Create Instance → Select R2 bucket

**Supported formats:** `.md`, `.txt`, `.html`, `.pdf`, `.doc`, `.docx`, `.csv`, `.json`

**Auto-indexed metadata:** `filename`, `folder`, `timestamp`

### Website Crawler

Requirements:
- Domain on Cloudflare
- `sitemap.xml` at root
- Bot protection must allow `CloudflareAISearch` user agent

## Path Filtering (R2)

```
docs/**/*.md          # All .md in docs/ recursively
**/*.draft.md         # Exclude (use in exclude patterns)
```

## Indexing

- **Automatic:** Every 6 hours
- **Force Sync:** Dashboard button (30s rate limit between syncs)
- **Pause:** Settings → Pause Indexing (existing index remains searchable)

## Service API Token

Dashboard: AI Search → Instance → Use AI Search → API → Create Token

Permissions:
- **Read** - search operations
- **Edit** - instance management

Store securely:
```bash
wrangler secret put AI_SEARCH_TOKEN
```

## Multi-Environment

```toml
# wrangler.toml
[env.production.vars]
AI_SEARCH_INSTANCE = "prod-docs"

[env.staging.vars]
AI_SEARCH_INSTANCE = "staging-docs"
```

```typescript
const answer = await env.AI.autorag(env.AI_SEARCH_INSTANCE).aiSearch({ query });
```

## Monitoring

```typescript
const instances = await env.AI.autorag("_").listInstances();
console.log(instances.find(i => i.name === "docs"));
```

Dashboard shows: files indexed, status, last index time, storage usage.

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
