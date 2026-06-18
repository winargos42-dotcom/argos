---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/turn/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\turn\README.md
source_ext: .md
source_sha256: 563471176abd1e88186f427a86c76f129b18ed01d6ffd7cdd0bfba94308fe934
text_sha256: 9b1e36931f40b1faf3c8f24f89acb12c4f4223de0afc83e6b8de636f4730d542
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/turn/README.md`
- Extract: `text`
- SHA256: `563471176abd1e88186f427a86c76f129b18ed01d6ffd7cdd0bfba94308fe934`

## Content

# Cloudflare TURN Service

Expert guidance for implementing Cloudflare TURN Service in WebRTC applications.

## Overview

Cloudflare TURN (Traversal Using Relays around NAT) Service is a managed relay service for WebRTC applications. TURN acts as a relay point for traffic between WebRTC clients and SFUs, particularly when direct peer-to-peer communication is obstructed by NATs or firewalls. The service runs on Cloudflare's global anycast network across 310+ cities.

## Key Characteristics

- **Anycast Architecture**: Automatically connects clients to the closest Cloudflare location
- **Global Network**: Available across Cloudflare's entire network (excluding China Network)
- **Zero Configuration**: No need to manually select regions or servers
- **Protocol Support**: STUN/TURN over UDP, TCP, and TLS
- **Free Tier**: Free when used with Cloudflare Calls SFU, otherwise $0.05/GB outbound

## In This Reference

| File | Purpose |
|------|---------|
| [api.md](./api.md) | Credentials API, TURN key management, types, constraints |
| [configuration.md](./configuration.md) | Worker setup, wrangler.jsonc, env vars, IP allowlisting |
| [patterns.md](./patterns.md) | Implementation patterns, use cases, integration examples |
| [gotchas.md](./gotchas.md) | Troubleshooting, limits, security, common mistakes |

## Reading Order

| Task | Files to Read | Est. Tokens |
|------|---------------|-------------|
| Quick start | README only | ~500 |
| Generate credentials | README → api | ~1300 |
| Worker integration | README → configuration → patterns | ~2000 |
| Debug connection | gotchas | ~700 |
| Security review | api → gotchas | ~1500 |
| Enterprise firewall | configuration | ~600 |

## Service Addresses and Ports

### STUN over UDP
- **Primary**: `stun.cloudflare.com:3478/udp`
- **Alternate**: `stun.cloudflare.com:53/udp` (blocked by browsers, not recommended)

### TURN over UDP
- **Primary**: `turn.cloudflare.com:3478/udp`
- **Alternate**: `turn.cloudflare.com:53/udp` (blocked by browsers)

### TURN over TCP
- **Primary**: `turn.cloudflare.com:3478/tcp`
- **Alternate**: `turn.cloudflare.com:80/tcp`

### TURN over TLS
- **Primary**: `turn.cloudflare.com:5349/tcp`
- **Alternate**: `turn.cloudflare.com:443/tcp`

## Quick Start

1. **Create TURN key via API**: see [api.md#create-turn-key](./api.md#create-turn-key)
2. **Generate credentials**: see [api.md#generate-temporary-credentials](./api.md#generate-temporary-credentials)
3. **Configure Worker**: see [configuration.md#cloudflare-worker-integration](./configuration.md#cloudflare-worker-integration)
4. **Implement client**: see [patterns.md#basic-turn-configuration-browser](./patterns.md#basic-turn-configuration-browser)

## When to Use TURN

- **Restrictive NATs**: Symmetric NATs that block direct connections
- **Corporate firewalls**: Environments blocking WebRTC ports
- **Mobile networks**: Carrier-grade NAT scenarios
- **Predictable connectivity**: When reliability > efficiency

## Related Cloudflare Services

- **Cloudflare Calls SFU**: Managed Selective Forwarding Unit (TURN free when used with SFU)
- **Cloudflare Stream**: Video streaming with WHIP/WHEP support
- **Cloudflare Workers**: Backend for credential generation
- **Cloudflare KV**: Credential caching
- **Cloudflare Durable Objects**: Session state management

## Additional Resources

- [Cloudflare Calls Documentation](https://developers.cloudflare.com/calls/)
- [Cloudflare TURN Service Docs](https://developers.cloudflare.com/realtime/turn/)
- [Cloudflare API Reference](https://developers.cloudflare.com/api/resources/calls/subresources/turn/)
- [Orange Meets (Open Source Example)](https://github.com/cloudflare/orange)

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
