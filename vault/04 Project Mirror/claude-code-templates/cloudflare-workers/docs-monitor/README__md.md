---
argos_import: project_file
source_path: claude-code-templates/cloudflare-workers/docs-monitor/README.md
source_abs: F:\debug\argoss\claude-code-templates\cloudflare-workers\docs-monitor\README.md
source_ext: .md
source_sha256: 8b33e3d19392e0376016a9534d43c1e232e96dee38f5f6617df5e1412dd0b752
text_sha256: 5442159a7c16b8f9fc96f32ccaf787e455c889b13301ae121dc6c4a1cb08024e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# README.md

- Source: `claude-code-templates/cloudflare-workers/docs-monitor/README.md`
- Extract: `text`
- SHA256: `8b33e3d19392e0376016a9534d43c1e232e96dee38f5f6617df5e1412dd0b752`

## Content

# Claude Code Docs Monitor

Cloudflare Worker that monitors Claude Code documentation at https://code.claude.com/docs and sends Telegram notifications when changes are detected.

## 🌟 Features

- ✅ **Automatic monitoring** every 6 hours (configurable)
- ✅ **Change detection** using SHA-256 hash
- ✅ **Telegram notifications** with change details
- ✅ **Content cleaning** to avoid false positives (ignores scripts, styles, analytics)
- ✅ **HTTP endpoint** for manual triggers and status checks
- ✅ **100% Serverless** - runs on Cloudflare Edge
- ✅ **Free** within Cloudflare's free tier

## 📋 Prerequisites

1. **Cloudflare Account** (free): https://dash.cloudflare.com/sign-up
2. **Telegram Bot**:
   - Talk to [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow instructions
   - Save the **token** it gives you
3. **Your Telegram Chat ID**:
   - Talk to [@userinfobot](https://t.me/userinfobot)
   - Send `/start` and it will give you your **chat ID**

## 🚀 Installation (100% CLI)

### 1. Install Wrangler CLI

```bash
npm install -g wrangler

# Or using the local project
cd cloudflare-workers/docs-monitor
npm install
```

### 2. Authenticate with Cloudflare

```bash
wrangler login
```

This will open your browser for authentication.

### 3. Create KV Namespace

The worker needs KV (Key-Value) storage to save state:

```bash
# Create the namespace
wrangler kv:namespace create DOCS_MONITOR_KV

# Expected output:
# 🌀 Creating namespace with title "claude-docs-monitor-DOCS_MONITOR_KV"
# ✨ Success!
# Add the following to your configuration file in your kv_namespaces array:
# { binding = "DOCS_MONITOR_KV", id = "xxxxxxxxxxxxxx" }
```

**IMPORTANT**: Copy the `id` it gives you and paste it in `wrangler.toml`:

```toml
\[\[kv_namespaces\]\]
binding = "DOCS_MONITOR_KV"
id = "YOUR_KV_ID_HERE"  # ← Replace with your ID
```

### 4. Configure Secrets (CLI)

Set your Telegram credentials as secrets:

```bash
# Telegram bot token
wrangler secret put TELEGRAM_BOT_TOKEN
# When prompted, paste: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Your Telegram Chat ID
wrangler secret put TELEGRAM_CHAT_ID
# When prompted, paste: 123456789

# (Optional) Secret for manual trigger
wrangler secret put TRIGGER_SECRET
# When prompted, paste any random string: my-super-secret-123
```

### 5. Deploy (CLI)

```bash
npm run deploy

# Or directly:
wrangler deploy
```

Done! Your worker is deployed and running 🎉

## 🔧 Configuration

### Change monitoring frequency

Edit `wrangler.toml`:

```toml
[triggers]
# Every 6 hours (default)
crons = ["0 */6 * * *"]

# Every 4 hours
crons = ["0 */4 * * *"]

# Every 2 hours
crons = ["0 */2 * * *"]

# Every hour
crons = ["0 * * * *"]

# Every 30 minutes (for development)
crons = ["*/30 * * * *"]
```

After changing, redeploy:

```bash
npm run deploy
```

### Monitor multiple URLs

To monitor more sites:

1. **Option A**: Duplicate the worker
   ```bash
   cp -r docs-monitor github-releases-monitor
   # Edit index.js to change the URL
   # Change the name in wrangler.toml
   ```

2. **Option B**: Modify `index.js` to accept multiple URLs
   ```javascript
   const urls = [
     'https://code.claude.com/docs',
     'https://github.com/anthropics/claude-code/releases',
   ];
   ```

## 🎯 Usage (All via CLI)

### Check monitor status

```bash
curl https://claude-docs-monitor.YOUR-USERNAME.workers.dev/status
```

Response:
```json
{
  "status": "running",
  "lastHash": "a1b2c3d4...",
  "lastChecked": "2026-01-01T10:00:00.000Z",
  "lastChange": "2025-12-28T14:30:00.000Z",
  "monitoredUrl": "https://code.claude.com/docs"
}
```

### Manual trigger

To force an immediate check:

```bash
curl -X POST https://claude-docs-monitor.YOUR-USERNAME.workers.dev/trigger \
  -H "Authorization: Bearer YOUR_TRIGGER_SECRET"
```

### View logs in real-time (CLI)

```bash
npm run tail

# Or directly:
wrangler tail
```

### Local development (CLI)

```bash
npm run dev

# Test cron job locally
npm run test
```

## 📊 Monitoring (CLI)

### View logs via CLI

```bash
# Real-time logs
wrangler tail

# View recent deployments
wrangler deployments list

# View specific deployment
wrangler deployments view <deployment-id>

# List secrets
wrangler secret list

# Delete a secret
wrangler secret delete SECRET_NAME
```

### View KV data (CLI)

```bash
# List all KV namespaces
wrangler kv:namespace list

# List keys in namespace
wrangler kv:key list --namespace-id=YOUR_KV_ID

# Get a specific key value
wrangler kv:key get last_hash --namespace-id=YOUR_KV_ID

# Put a value (for testing)
wrangler kv:key put test_key "test_value" --namespace-id=YOUR_KV_ID

# Delete a key
wrangler kv:key delete test_key --namespace-id=YOUR_KV_ID
```

## 🐛 Troubleshooting

### No notifications received

1. **Verify secrets**:
   ```bash
   # List configured secrets
   wrangler secret list
   ```

2. **Test bot manually**:
   ```bash
   curl https://api.telegram.org/botYOUR_BOT_TOKEN/getMe
   # Should return bot info
   ```

3. **Verify chat ID**:
   ```bash
   # Send a test message
   curl -X POST https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage \
     -d chat_id=YOUR_CHAT_ID \
     -d text="Test"
   ```

### Worker doesn't execute cron

- Cron triggers **only work in production** (after deploy)
- They don't work in `wrangler dev`
- Check via CLI: `wrangler tail` to see cron executions

### Error: "KV namespace not found"

- Make sure you created the KV namespace: `wrangler kv:namespace create DOCS_MONITOR_KV`
- Verify the `id` in `wrangler.toml` is correct
- Redeploy after changing config: `wrangler deploy`

### Update worker after changes

```bash
# After editing index.js or wrangler.toml
wrangler deploy

# View deployment status
wrangler deployments list
```

## 💰 Costs

**Completely FREE** in Cloudflare's free tier:

- ✅ Workers: 100,000 requests/day
- ✅ Cron Triggers: Unlimited
- ✅ KV Storage: 100k reads/day, 1k writes/day
- ✅ CPU Time: 10ms/request (sufficient)

For this use case (~4 executions/day):
- **Requests**: 4/day → 0.004% of limit
- **KV Writes**: 4/day → 0.4% of limit
- **KV Reads**: 4/day → 0.004% of limit

**Cost: $0.00/month** 🎉

## 🔒 Security

- ✅ Secrets stored securely in Cloudflare (via CLI)
- ✅ Trigger endpoint protected with token
- ✅ No sensitive information in logs
- ✅ HTTPS by default for all communications
- ✅ No dashboard access needed - everything via CLI

## 📚 Resources

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Cron Expression Generator](https://crontab.guru/)

## 🤝 Contributing

This worker is part of the [claude-code-templates](https://github.com/danipower/claude-code-templates) project.

## 📝 License

MIT

---

**Made with ❤️ for the Claude Code community**

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
