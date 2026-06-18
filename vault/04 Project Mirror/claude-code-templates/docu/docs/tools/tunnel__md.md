---
argos_import: project_file
source_path: claude-code-templates/docu/docs/tools/tunnel.md
source_abs: F:\debug\argoss\claude-code-templates\docu\docs\tools\tunnel.md
source_ext: .md
source_sha256: 0c2a2633dc55b111d5c215ae2a22a294c7c4d471c6796a91a42261c8b49d40cc
text_sha256: 845eb4014fd52ace7741fd6500ae27411a38ff3026726f2cd67daf228a1f1b30
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:55
---

# tunnel.md

- Source: `claude-code-templates/docu/docs/tools/tunnel.md`
- Extract: `text`
- SHA256: `0c2a2633dc55b111d5c215ae2a22a294c7c4d471c6796a91a42261c8b49d40cc`

## Content

---
sidebar_position: 5
---

# Cloudflare Tunnel

Secure remote access to your Claude Code tools from anywhere.

## Launch Commands

### With Chats
```bash
npx claude-code-templates@latest --chats --tunnel
```

## How It Works

1. **Tool starts locally** - Analytics or chats interface launches
2. **Tunnel created** - Secure connection through Cloudflare
3. **Public URL generated** - Shareable HTTPS link provided
4. **Global access** - Use from any device with internet

## 🔧 Troubleshooting

### Common Issues

**Tunnel won't start:**
```bash
# Check internet connection
ping cloudflare.com

# Verify tool is running locally first
npx claude-code-templates@latest --chats
```

---

**Next:** Explore [E2B Sandbox](./sandbox) for secure cloud execution environments.

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
