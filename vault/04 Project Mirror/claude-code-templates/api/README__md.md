---
argos_import: project_file
source_path: claude-code-templates/api/README.md
source_abs: F:\debug\argoss\claude-code-templates\api\README.md
source_ext: .md
source_sha256: 28ea718eee50b532f59f899e6b5232931cd4fce5c1b4c3c0dd1209fcfff74458
text_sha256: 64aba334412b2ca19e8c9bb01e47a5b42fd698c8749413a294877ae0bdaaa12b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:27
---

# README.md

- Source: `claude-code-templates/api/README.md`
- Extract: `text`
- SHA256: `28ea718eee50b532f59f899e6b5232931cd4fce5c1b4c3c0dd1209fcfff74458`

## Content

# API - Vercel Serverless Functions

Critical infrastructure for claude-code-templates component ecosystem.

## ⚠️ CRITICAL ENDPOINTS

These endpoints are essential for component download metrics. **DO NOT BREAK THEM.**

### `/api/track-download-supabase` 🔴

Tracks every component installation from the CLI tool.

**Used by**: `cli-tool/bin/create-claude-config.js`

**Called on**: Every `--agent`, `--command`, `--mcp`, `--hook`, `--setting`, `--skill` installation

**Database**: Supabase (component_downloads, download_stats)

### `/api/discord/interactions` 🟡

Discord bot for component discovery and search.

**Features**: `/search`, `/info`, `/install`, `/popular`, `/random`

### `/api/claude-code-check` 🟢

Monitors Claude Code releases and sends Discord notifications.

**Frequency**: Every 4 hours (Vercel Cron)

**Database**: Neon (claude_code_versions, claude_code_changes)

## 🧪 Testing

**ALWAYS run tests before deploying:**

```bash
# Run all tests
npm test

# Run only critical endpoint tests
npm run test:api

# Watch mode
npm run test:watch

# With coverage
npm run test:coverage
```

## 🚀 Deployment

### Pre-Deployment Checklist

```bash
# 1. Run validation script (from project root)
./scripts/predeploy-check.sh

# 2. If checks pass, deploy
vercel --prod
```

### Manual Deploy Steps

```bash
# 1. Install dependencies
npm install

# 2. Run tests
npm run test:api

# 3. Deploy
cd ..
vercel --prod
```

## 📁 File Structure

```
api/
├── track-download-supabase.js       # Component download tracking (CRITICAL)
├── claude-code-check.js             # Claude Code changelog monitor
├── _parser-claude.js                # Changelog parser utility
├── discord/
│   └── interactions.js              # Discord bot handler
├── claude-code-monitor/
│   ├── README.md                    # Detailed docs
│   ├── check-version.js             # Version checker
│   ├── discord-notifier.js          # Discord notifications
│   ├── parser.js                    # Changelog parser
│   └── webhook.js                   # NPM webhook handler
├── __tests__/
│   └── endpoints.test.js            # Critical endpoint tests
├── jest.config.cjs                  # Jest configuration
├── package.json                     # Dependencies & scripts
└── README.md                        # This file
```

## 🔧 Environment Variables

Required in Vercel Dashboard:

```bash
# Supabase
SUPABASE_URL=xxx
SUPABASE_SERVICE_ROLE_KEY=xxx

# Neon Database
NEON_DATABASE_URL=xxx

# Discord
DISCORD_APP_ID=xxx
DISCORD_BOT_TOKEN=xxx
DISCORD_PUBLIC_KEY=xxx
DISCORD_WEBHOOK_URL_CHANGELOG=xxx
```

## 🐛 Troubleshooting

### Tests Failing?

```bash
# Test against production
API_BASE_URL=https://aitmpl.com npm run test:api

# Check specific endpoint
curl -X POST https://aitmpl.com/api/track-download-supabase \
  -H "Content-Type: application/json" \
  -d '{"type":"agent","name":"test","path":"test/path"}'
```

### Endpoint Not Found After Deploy?

1. Check Vercel function logs: `vercel logs aitmpl.com --follow`
2. Verify file is in `/api` root (not nested)
3. Ensure proper export: `export default async function handler(req, res) {}`

### No Download Tracking Data?

1. Check Vercel logs
2. Verify environment variables are set
3. Test endpoint manually (see above)
4. Check Supabase table: `select * from component_downloads order by created_at desc limit 10;`

## 📊 Monitoring

### Vercel Dashboard

https://vercel.com/dashboard → aitmpl → Functions

### Real-time Logs

```bash
vercel logs aitmpl.com --follow
```

### Database Queries

**Supabase**:
```sql
SELECT type, name, COUNT(*) as downloads
FROM component_downloads
WHERE download_timestamp > NOW() - INTERVAL '7 days'
GROUP BY type, name
ORDER BY downloads DESC;
```

**Neon**:
```sql
SELECT version, published_at, discord_notified
FROM claude_code_versions
ORDER BY published_at DESC;
```

## 🆘 Emergency Rollback

```bash
# 1. List recent deployments
vercel ls

# 2. Promote previous working deployment
vercel promote <previous-deployment-url>
```

## 📖 More Info

See `../CLAUDE.md` section "API Architecture & Deployment" for detailed documentation.

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
