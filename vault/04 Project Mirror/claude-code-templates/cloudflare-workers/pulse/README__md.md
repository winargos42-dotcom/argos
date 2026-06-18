---
argos_import: project_file
source_path: claude-code-templates/cloudflare-workers/pulse/README.md
source_abs: F:\debug\argoss\claude-code-templates\cloudflare-workers\pulse\README.md
source_ext: .md
source_sha256: 19a75186c02b808a2baab194057eabe71f9d21b276cde83ed665d7e8519b4f1e
text_sha256: f1a78328189f0e7d4434bfd213e3947a7434dd3104df42a8f6044aafa3131323
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# README.md

- Source: `claude-code-templates/cloudflare-workers/pulse/README.md`
- Extract: `text`
- SHA256: `19a75186c02b808a2baab194057eabe71f9d21b276cde83ed665d7e8519b4f1e`

## Content

# Pulse — Weekly KPI Report (Cloudflare Worker)

Collects metrics from GitHub, Discord, Supabase, Vercel, and Google Analytics every Sunday at 14:00 UTC and sends a consolidated report via Telegram.

## Setup

### 1. Install dependencies

```bash
cd cloudflare-workers/pulse
npm install
```

### 2. Configure secrets

Set each secret using `wrangler secret put`:

```bash
# Telegram (same bot/chat as docs-monitor)
wrangler secret put TELEGRAM_BOT_TOKEN
wrangler secret put TELEGRAM_CHAT_ID

# GitHub
wrangler secret put GITHUB_TOKEN          # PAT with public_repo scope

# Supabase
wrangler secret put SUPABASE_URL          # https://xxx.supabase.co
wrangler secret put SUPABASE_SERVICE_ROLE_KEY

# Discord
wrangler secret put DISCORD_BOT_TOKEN
wrangler secret put DISCORD_GUILD_ID

# Vercel
wrangler secret put VERCEL_TOKEN          # Personal access token
wrangler secret put VERCEL_PROJECT_ID     # aitmpl project ID

# Manual trigger auth
wrangler secret put TRIGGER_SECRET

# Optional — Google Analytics (add later)
wrangler secret put GA_PROPERTY_ID
wrangler secret put GA_SERVICE_ACCOUNT_JSON  # Base64-encoded service account JSON
```

### 3. Deploy

```bash
wrangler deploy
```

## Usage

### Automatic (Cron)

Runs every Sunday at 14:00 UTC (11:00 AM Chile). No action needed after deploy.

### Manual trigger

```bash
# Full report
curl -X POST https://pulse-weekly-report.YOUR_SUBDOMAIN.workers.dev/trigger \
  -H "Authorization: Bearer YOUR_TRIGGER_SECRET"

# Single source only
curl -X POST "https://pulse-weekly-report.YOUR_SUBDOMAIN.workers.dev/trigger?source=github" \
  -H "Authorization: Bearer YOUR_TRIGGER_SECRET"

# Dry run (don't send to Telegram)
curl -X POST "https://pulse-weekly-report.YOUR_SUBDOMAIN.workers.dev/trigger?send=false" \
  -H "Authorization: Bearer YOUR_TRIGGER_SECRET"
```

### Status

```bash
curl https://pulse-weekly-report.YOUR_SUBDOMAIN.workers.dev/status
```

## Local development

```bash
npm run dev              # Start local dev server
npm run test             # Test cron trigger locally
```

## Report format

```
📊 PULSE — Weekly Report
📅 Jan 25, 2026 - Jan 31, 2026

⭐ GITHUB
├ Stars: 1,234 (+45)
├ Forks: 156 (+8)
├ Issues: 12 open (3 new, 2 closed)
└ PRs: 5 opened, 4 merged

💬 DISCORD
├ Members: 890 (+23)
├ Active: ~145
└ Messages: 312

📦 DOWNLOADS
├ Total: 45,678 (+1,234)
├ Top: frontend-developer (89)
├ By type: agents 65% | commands 20% | settings 15%
└ Countries: US 40% | DE 15% | BR 10% | UK 8% | CL 5%

🚀 VERCEL
├ Deploys: 12 (11 ✅ 1 ❌)
└ Latest: 2h ago ✅

📈 ANALYTICS
├ Visitors: 3,456
├ Pageviews: 12,345
├ Top: / (4,567) | /agents (2,345) | /commands (1,234)
└ Referrers: google (45%) | github (30%) | direct (15%)
```

Sources that fail gracefully show `⚠️ Unavailable` instead.

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
