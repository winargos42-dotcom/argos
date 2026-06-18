---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/argo-smart-routing/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\argo-smart-routing\patterns.md
source_ext: .md
source_sha256: b793b458e3704a5c5e9fc8efb6245e7bf840c5d4b8f7b54865ebf2d90af3dd17
text_sha256: 8f0e0d9abdc17971afc802c23a04bf8780365031e5c4241cf084b0ad97c3707e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/argo-smart-routing/patterns.md`
- Extract: `text`
- SHA256: `b793b458e3704a5c5e9fc8efb6245e7bf840c5d4b8f7b54865ebf2d90af3dd17`

## Content

# Integration Patterns

## Enable Argo + Tiered Cache

```typescript
async function enableOptimalPerformance(client: Cloudflare, zoneId: string) {
  await Promise.all([
    client.argo.smartRouting.edit({ zone_id: zoneId, value: 'on' }),
    client.argo.tieredCaching.edit({ zone_id: zoneId, value: 'on' }),
  ]);
}
```

**Flow:** Visitor → Edge (Lower-Tier) → [Cache Miss] → Upper-Tier → [Cache Miss + Argo] → Origin

**Impact:** Argo ~30% latency reduction + Tiered Cache 50-80% origin offload

## Usage Analytics (GraphQL)

```graphql
query ArgoAnalytics($zoneTag: string!) {
  viewer {
    zones(filter: { zoneTag: $zoneTag }) {
      httpRequestsAdaptiveGroups(limit: 1000) {
        sum { argoBytes, bytes }
      }
    }
  }
}
```

**Billing:** ~$0.10/GB. DDoS-mitigated and WAF-blocked traffic NOT charged.

## Spectrum TCP Integration

Enable Argo for non-HTTP traffic (databases, game servers, IoT):

```typescript
// Update existing app
await client.spectrum.apps.update(appId, { zone_id: zoneId, argo_smart_routing: true });

// Create new app with Argo
await client.spectrum.apps.create({
  zone_id: zoneId,
  dns: { type: 'CNAME', name: 'tcp.example.com' },
  origin_direct: ['tcp://origin.example.com:3306'],
  protocol: 'tcp/3306',
  argo_smart_routing: true,
});
```

**Use cases:** MySQL/PostgreSQL (3306/5432), game servers, MQTT (1883), SSH (22)

## Pre-Flight Validation

```typescript
async function validateArgoEligibility(client: Cloudflare, zoneId: string) {
  const status = await client.argo.smartRouting.get({ zone_id: zoneId });
  const zone = await client.zones.get({ zone_id: zoneId });
  
  const issues: string[] = [];
  if (!status.editable) issues.push('Zone not editable');
  if (['free', 'pro'].includes(zone.plan.legacy_id)) issues.push('Requires Business+ plan');
  if (zone.status !== 'active') issues.push('Zone not active');
  
  return { canEnable: issues.length === 0, issues };
}
```

## Post-Enable Verification

```typescript
async function verifyArgoEnabled(client: Cloudflare, zoneId: string): Promise<boolean> {
  await new Promise(r => setTimeout(r, 2000)); // Wait for propagation
  const status = await client.argo.smartRouting.get({ zone_id: zoneId });
  return status.value === 'on';
}
```

## Full Setup Pattern

```typescript
async function setupArgo(client: Cloudflare, zoneId: string) {
  // 1. Validate
  const { canEnable, issues } = await validateArgoEligibility(client, zoneId);
  if (!canEnable) throw new Error(issues.join(', '));
  
  // 2. Enable both features
  await Promise.all([
    client.argo.smartRouting.edit({ zone_id: zoneId, value: 'on' }),
    client.argo.tieredCaching.edit({ zone_id: zoneId, value: 'on' }),
  ]);
  
  // 3. Verify
  const [argo, cache] = await Promise.all([
    client.argo.smartRouting.get({ zone_id: zoneId }),
    client.argo.tieredCaching.get({ zone_id: zoneId }),
  ]);
  
  return { argo: argo.value === 'on', tieredCache: cache.value === 'on' };
}
```

**When to combine:** High-traffic sites (>1TB/mo), global users, cacheable content.

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
