---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/c3/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\c3\gotchas.md
source_ext: .md
source_sha256: ca24662cfe1b10526d11ca15a6223a47578b21306d718710d1611fe861906a42
text_sha256: 4acfbc2572326cd0be2bdd76bc7c7fb629a68dabb7c98b3fc6bed234d13e72b0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/c3/gotchas.md`
- Extract: `text`
- SHA256: `ca24662cfe1b10526d11ca15a6223a47578b21306d718710d1611fe861906a42`

## Content

# C3 Troubleshooting

## Deployment Issues

### Placeholder IDs

**Error:** "Invalid namespace ID"  
**Fix:** Replace placeholders in wrangler.jsonc with real IDs:
```bash
npx wrangler kv namespace create MY_KV  # Get real ID
```

### Authentication

**Error:** "Not authenticated"  
**Fix:** `npx wrangler login` or set `CLOUDFLARE_API_TOKEN`

### Name Conflict

**Error:** "Worker already exists"  
**Fix:** Change `name` in wrangler.jsonc

## Platform Selection

| Need | Platform |
|------|----------|
| Git integration, branch previews | `--platform=pages` |
| Durable Objects, D1, Queues | Workers (default) |

Wrong platform? Recreate with correct `--platform` flag.

## TypeScript Issues

**"Cannot find name 'KVNamespace'"**
```bash
npm run cf-typegen  # Regenerate types
# Restart TS server in editor
```

**Missing types after config change:** Re-run `npm run cf-typegen`

## Package Manager

**Multiple lockfiles causing issues:**
```bash
rm pnpm-lock.yaml  # If using npm
rm package-lock.json  # If using pnpm
```

## CI/CD

**CI hangs on prompts:**
```bash
npm create cloudflare@latest my-app -- \
  --type=hello-world --lang=ts --no-git --no-deploy
```

**Auth in CI:**
```yaml
env:
  CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
  CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

## Framework-Specific

| Framework | Issue | Fix |
|-----------|-------|-----|
| Next.js | create-next-app failed | `npm cache clean --force`, retry |
| Astro | Adapter missing | Install `@astrojs/cloudflare` |
| Remix | Module errors | Update `@remix-run/cloudflare*` |

## Compatibility Date

**"Feature X requires compatibility_date >= ..."**  
**Fix:** Update `compatibility_date` in wrangler.jsonc to today's date

## Node.js Version

**"Node.js version not supported"**  
**Fix:** Install Node.js 18+ (`nvm install 20`)

## Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| Invalid namespace ID | Placeholder binding | Create resource, update config |
| Not authenticated | No login | `npx wrangler login` |
| Cannot find KVNamespace | Missing types | `npm run cf-typegen` |
| Worker already exists | Name conflict | Change `name` |
| CI hangs | Missing flags | Add --type, --lang, --no-deploy |
| Template not found | Bad name | Check cloudflare/templates |

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
