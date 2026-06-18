---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ddos/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ddos\README.md
source_ext: .md
source_sha256: f41c92f7a4a1201ed81241d57786c2c732479b1c6b9afb1381eb2e45859516d9
text_sha256: 63018c3c2d25ce26a0f1b80dd60bd2d3c5193a26bf96979ef624030ab766c4a8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ddos/README.md`
- Extract: `text`
- SHA256: `f41c92f7a4a1201ed81241d57786c2c732479b1c6b9afb1381eb2e45859516d9`

## Content

# Cloudflare DDoS Protection

Autonomous, always-on protection against DDoS attacks across L3/4 and L7.

## Protection Types

- **HTTP DDoS (L7)**: Protects HTTP/HTTPS traffic, phase `ddos_l7`, zone/account level
- **Network DDoS (L3/4)**: UDP/SYN/DNS floods, phase `ddos_l4`, account level only
- **Adaptive DDoS**: Learns 7-day baseline, detects deviations, 4 profile types (Origins, User-Agents, Locations, Protocols)

## Plan Availability

| Feature | Free | Pro | Business | Enterprise | Enterprise Advanced |
|---------|------|-----|----------|------------|---------------------|
| HTTP DDoS (L7) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Network DDoS (L3/4) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Override rules | 1 | 1 | 1 | 1 | 10 |
| Custom expressions | ✗ | ✗ | ✗ | ✗ | ✓ |
| Log action | ✗ | ✗ | ✗ | ✗ | ✓ |
| Adaptive DDoS | ✗ | ✗ | ✗ | ✓ | ✓ |
| Alert filters | Basic | Basic | Basic | Advanced | Advanced |

## Actions & Sensitivity

- **Actions**: `block`, `managed_challenge`, `challenge`, `log` (Enterprise Advanced only)
- **Sensitivity**: `default` (high), `medium`, `low`, `eoff` (essentially off)
- **Override**: By category/tag or individual rule ID
- **Scope**: Zone-level overrides take precedence over account-level

## Reading Order

| File | Purpose | Start Here If... |
|------|---------|------------------|
| [configuration.md](./configuration.md) | Dashboard setup, rule structure, adaptive profiles | You're setting up DDoS protection for the first time |
| [api.md](./api.md) | API endpoints, SDK usage, ruleset ID discovery | You're automating configuration or need programmatic access |
| [patterns.md](./patterns.md) | Protection strategies, defense-in-depth, dynamic response | You need implementation patterns or layered security |
| [gotchas.md](./gotchas.md) | False positives, tuning, error handling | You're troubleshooting or optimizing existing protection |

## See Also
- [waf](../waf/) - Application-layer security rules
- [bot-management](../bot-management/) - Bot detection and mitigation

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
