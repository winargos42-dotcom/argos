---
argos_import: project_file
source_path: claude-code-templates/cli-tool/.claude/sandbox/cloudflare/QUICKSTART.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\.claude\sandbox\cloudflare\QUICKSTART.md
source_ext: .md
source_sha256: ec9621aa1b01eb939139d7f0bb2057b659a683fb83471f8945a503708b16c2f9
text_sha256: 4456a5599734e27546f5bb024b1062bbe623a8134825d443540a12fe6dddef91
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:27
---

# QUICKSTART.md

- Source: `claude-code-templates/cli-tool/.claude/sandbox/cloudflare/QUICKSTART.md`
- Extract: `text`
- SHA256: `ec9621aa1b01eb939139d7f0bb2057b659a683fb83471f8945a503708b16c2f9`

## Content

# Cloudflare Sandbox Quick Start Guide

Get your Cloudflare Claude Code Sandbox running in under 5 minutes.

## Prerequisites Checklist

- [ ] Cloudflare account (sign up at https://dash.cloudflare.com/sign-up)
- [ ] Anthropic API key (get from https://console.anthropic.com/)
- [ ] Node.js 16.17.0+ installed
- [ ] Docker installed and running (for local development)

## Option 1: Deploy to Production (Fastest)

Perfect if you want to skip local testing and deploy directly.

### Step 1: Install Dependencies
```bash
cd .claude/sandbox/cloudflare
npm install
```

### Step 2: Set API Key
```bash
npx wrangler secret put ANTHROPIC_API_KEY
# Paste your Anthropic API key when prompted
```

### Step 3: Deploy
```bash
npx wrangler deploy
```

### Step 4: Wait for Container Provisioning
```bash
# Wait 2-3 minutes, then check:
npx wrangler containers list
# You should see: ✓ Container ready
```

### Step 5: Test Your Deployment
```bash
# Get your worker URL from the deploy output, then:
curl -X POST https://YOUR-WORKER.YOUR-SUBDOMAIN.workers.dev/execute \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the 10th Fibonacci number?"}'
```

Expected response:
```json
{
  "success": true,
  "question": "What is the 10th Fibonacci number?",
  "code": "def fibonacci(n):\n    ...",
  "output": "55\n",
  "error": "",
  "executionTime": 1234
}
```

**Done!** Your sandbox is live at the edge.

---

## Option 2: Local Development First

Perfect if you want to test locally before deploying.

### Step 1: Install Dependencies
```bash
cd .claude/sandbox/cloudflare
npm install
```

### Step 2: Create Local Environment File
```bash
cp .dev.vars.example .dev.vars
# Edit .dev.vars and add your Anthropic API key
```

### Step 3: Start Docker
```bash
# macOS: Open Docker Desktop
# Linux: sudo systemctl start docker
# Windows: Start Docker Desktop

# Verify Docker is running:
docker ps
```

### Step 4: Start Development Server
```bash
npm run dev
```

Wait for:
```
⛅️ wrangler 3.78.12
-------------------
⎔ Starting local server...
[wrangler:inf] Ready on http://localhost:8787
```

### Step 5: Test Locally
```bash
# In a new terminal:
curl -X POST http://localhost:8787/execute \
  -H "Content-Type: application/json" \
  -d '{"question": "Calculate factorial of 5"}'
```

### Step 6: Deploy When Ready
```bash
# Stop the dev server (Ctrl+C)
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler deploy
```

**Done!** You've tested locally and deployed.

---

## Option 3: Using the CLI Tools

Perfect if you prefer command-line interaction.

### Step 1: Setup (same as above)
```bash
cd .claude/sandbox/cloudflare
npm install
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler deploy
```

### Step 2: Use the Launcher
```bash
# Execute a prompt
node launcher.ts "What is 2 to the power of 10?" \
  "" \
  your_anthropic_key \
  https://your-worker.workers.dev
```

### Step 3: Use the Monitor (for debugging)
```bash
# Get detailed execution metrics
node monitor.ts "Calculate factorial of 5" \
  your_anthropic_key \
  https://your-worker.workers.dev
```

**Done!** You're using the CLI tools.

---

## Common Issues & Quick Fixes

### "Container not ready"
**Solution**: Wait 2-3 minutes after first deployment
```bash
npx wrangler containers list
```

### "Docker daemon is not running"
**Solution**: Start Docker Desktop or Docker service
```bash
docker ps  # Should list containers
```

### "ANTHROPIC_API_KEY not configured"
**Solution**: Set the secret
```bash
# Production:
npx wrangler secret put ANTHROPIC_API_KEY

# Local (.dev.vars):
echo "ANTHROPIC_API_KEY=sk-ant-your-key" > .dev.vars
```

### "Worker not found"
**Solution**: Deploy the worker
```bash
npx wrangler deploy
```

### "Execution timeout"
**Solution**: Increase timeout in request
```json
{
  "question": "Your question",
  "timeout": 60000
}
```

---

## Next Steps

### 1. Customize Your Worker
Edit `src/index.ts` to add custom logic:
- Add authentication
- Implement rate limiting
- Add custom error handling
- Create specialized endpoints

### 2. Add Monitoring
```bash
# Watch logs in real-time
npx wrangler tail

# Use the monitor tool
node monitor.ts "your prompt" your_api_key
```

### 3. Test Different Languages
```bash
# Python (default)
curl -X POST https://your-worker.workers.dev/execute \
  -d '{"question": "Fibonacci", "language": "python"}'

# JavaScript
curl -X POST https://your-worker.workers.dev/execute \
  -d '{"question": "Fibonacci", "language": "javascript"}'
```

### 4. Integrate with Your App
```javascript
// Frontend integration
const response = await fetch('https://your-worker.workers.dev/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'Calculate factorial of 5' })
});

const result = await response.json();
console.log(result.output);
```

### 5. Enable Advanced Features
See the main [README.md](./README.md) for:
- Streaming output
- Code Interpreter API
- Caching strategies
- Performance optimization

---

## Resources

- **Documentation**: [README.md](./README.md)
- **Debugging**: [SANDBOX_DEBUGGING.md](./SANDBOX_DEBUGGING.md)
- **Component Info**: [claude-code-sandbox.md](./claude-code-sandbox.md)
- **Cloudflare Docs**: https://developers.cloudflare.com/sandbox/
- **Anthropic Docs**: https://docs.anthropic.com/

---

## Getting Help

1. **Check logs**: `npx wrangler tail`
2. **Use monitor**: `node monitor.ts "test" your_key`
3. **Read debugging guide**: [SANDBOX_DEBUGGING.md](./SANDBOX_DEBUGGING.md)
4. **Check container status**: `npx wrangler containers list`
5. **Test health**: `curl https://your-worker.workers.dev/health`

---

**You're all set! Start executing code with Claude AI on Cloudflare's edge network.**

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
