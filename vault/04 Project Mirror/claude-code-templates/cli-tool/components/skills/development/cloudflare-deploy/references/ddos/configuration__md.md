---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ddos/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ddos\configuration.md
source_ext: .md
source_sha256: 950556e02cfeac45e55bad22fcbb54763d9e563a586a7987d8941991325e3004
text_sha256: 0d0fae2b22edba2d40fddbbcec3f0c63651a25a0115e708edfc8b4e4c584c925
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ddos/configuration.md`
- Extract: `text`
- SHA256: `950556e02cfeac45e55bad22fcbb54763d9e563a586a7987d8941991325e3004`

## Content

# DDoS Configuration

## Dashboard Setup

1. Navigate to Security > DDoS
2. Select HTTP DDoS or Network-layer DDoS
3. Configure sensitivity & action per ruleset/category/rule
4. Apply overrides with optional expressions (Enterprise Advanced)
5. Enable Adaptive DDoS toggle (Enterprise/Enterprise Advanced, requires 7 days traffic history)

## Rule Structure

```typescript
interface DDoSOverride {
  description: string;
  rules: Array<{
    action: "execute";
    expression: string; // Custom expression (Enterprise Advanced) or "true" for all
    action_parameters: {
      id: string; // Managed ruleset ID (discover via api.md)
      overrides: {
        sensitivity_level?: "default" | "medium" | "low" | "eoff";
        action?: "block" | "managed_challenge" | "challenge" | "log"; // log = Enterprise Advanced only
        categories?: Array<{
          category: string; // e.g., "http-flood", "udp-flood"
          sensitivity_level?: string;
        }>;
        rules?: Array<{
          id: string;
          action?: string;
          sensitivity_level?: string;
        }>;
      };
    };
  }>;
}
```

## Expression Availability

| Plan | Custom Expressions | Example |
|------|-------------------|---------|
| Free/Pro/Business | ✗ | Use `"true"` only |
| Enterprise | ✗ | Use `"true"` only |
| Enterprise Advanced | ✓ | `ip.src in {...}`, `http.request.uri.path matches "..."` |

## Sensitivity Mapping

| UI | API | Threshold |
|----|-----|-----------|
| High | `default` | Most aggressive |
| Medium | `medium` | Balanced |
| Low | `low` | Less aggressive |
| Essentially Off | `eoff` | Minimal mitigation |

## Common Categories

- `http-flood`, `http-anomaly` (L7)
- `udp-flood`, `syn-flood`, `dns-flood` (L3/4)

## Override Precedence

Multiple override layers apply in this order (higher precedence wins):

```
Zone-level > Account-level
Individual Rule > Category > Global sensitivity/action
```

**Example**: Zone rule for `/api/*` overrides account-level global settings.

## Adaptive DDoS Profiles

**Availability**: Enterprise, Enterprise Advanced  
**Learning period**: 7 days of traffic history required

| Profile Type | Description | Detects |
|--------------|-------------|---------|
| **Origins** | Traffic patterns per origin server | Anomalous requests to specific origins |
| **User-Agents** | Traffic patterns per User-Agent | Malicious/anomalous user agent strings |
| **Locations** | Traffic patterns per geo-location | Attacks from specific countries/regions |
| **Protocols** | Traffic patterns per protocol (L3/4) | Protocol-specific flood attacks |

Configure by targeting specific adaptive rule IDs via API (see api.md#typed-override-examples).

## Alerting

Configure via Notifications:
- Alert types: `http_ddos_attack_alert`, `layer_3_4_ddos_attack_alert`, `advanced_*` variants
- Filters: zones, hostnames, RPS/PPS/Mbps thresholds, IPs, protocols
- Mechanisms: email, webhooks, PagerDuty

See [api.md](./api.md#alert-configuration) for API examples.

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
