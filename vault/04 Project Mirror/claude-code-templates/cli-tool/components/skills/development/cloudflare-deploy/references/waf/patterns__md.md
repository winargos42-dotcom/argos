---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/waf/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\waf\patterns.md
source_ext: .md
source_sha256: 72c40e63892e3db742afe8ca3f34cc112865d3c17f31a33d3528950f3708a69b
text_sha256: 8fc5fab71800154d1128725274bcfe1a59b3e667c2c0f841a96f643e5da89ba1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/waf/patterns.md`
- Extract: `text`
- SHA256: `72c40e63892e3db742afe8ca3f34cc112865d3c17f31a33d3528950f3708a69b`

## Content

# Common Patterns

## Deploy Managed Rulesets

```typescript
// Deploy Cloudflare Managed Ruleset (default)
await client.rulesets.create({
  zone_id: 'zone_id',
  kind: 'zone',
  phase: 'http_request_firewall_managed',
  name: 'Cloudflare Managed Ruleset',
  rules: [{
    action: 'execute',
    action_parameters: {
      id: 'efb7b8c949ac4650a09736fc376e9aee', // Cloudflare Managed
      // Or: '4814384a9e5d4991b9815dcfc25d2f1f' for OWASP CRS
      // Or: 'c2e184081120413c86c3ab7e14069605' for Exposed Credentials
    },
    expression: 'true', // All requests
    // Or: 'http.request.uri.path starts_with "/api"' for specific paths
    enabled: true,
  }],
});
```

## Override Managed Ruleset

```typescript
await client.rulesets.create({
  zone_id: 'zone_id',
  phase: 'http_request_firewall_managed',
  rules: [{
    action: 'execute',
    action_parameters: {
      id: 'efb7b8c949ac4650a09736fc376e9aee',
      overrides: {
        // Override specific rules
        rules: [
          { id: '5de7edfa648c4d6891dc3e7f84534ffa', action: 'log' },
          { id: '75a0060762034b9dad4e883afc121b4c', enabled: false },
        ],
        // Override categories: wordpress, sqli, xss, rce, etc.
        categories: [
          { category: 'wordpress', enabled: false },
          { category: 'sqli', action: 'log' },
        ],
      },
    },
    expression: 'true',
  }],
});
```

## Custom Rules

```typescript
await client.rulesets.create({
  zone_id: 'zone_id',
  kind: 'zone',
  phase: 'http_request_firewall_custom',
  name: 'Custom WAF Rules',
  rules: [
    // Attack score-based
    { action: 'block', expression: 'cf.waf.score gt 50', enabled: true },
    { action: 'challenge', expression: 'cf.waf.score gt 20', enabled: true },
    
    // Specific attack types
    { action: 'block', expression: 'cf.waf.score.sqli gt 30 or cf.waf.score.xss gt 30', enabled: true },
    
    // Geographic blocking
    { action: 'block', expression: 'ip.geoip.country in {"CN" "RU"}', enabled: true },
  ],
});
```

## Rate Limiting

```typescript
await client.rulesets.create({
  zone_id: 'zone_id',
  kind: 'zone',
  phase: 'http_ratelimit',
  name: 'Rate Limits',
  rules: [
    // Per-IP global limit
    {
      action: 'block',
      expression: 'true',
      action_parameters: {
        ratelimit: {
          characteristics: ['cf.colo.id', 'ip.src'],
          period: 60,
          requests_per_period: 100,
          mitigation_timeout: 600,
        },
      },
    },
    
    // Login endpoint (stricter)
    {
      action: 'block',
      expression: 'http.request.uri.path eq "/api/login"',
      action_parameters: {
        ratelimit: {
          characteristics: ['ip.src'],
          period: 60,
          requests_per_period: 5,
          mitigation_timeout: 600,
        },
      },
    },
    
    // API writes only (using counting_expression)
    {
      action: 'block',
      expression: 'http.request.uri.path starts_with "/api"',
      action_parameters: {
        ratelimit: {
          characteristics: ['cf.colo.id', 'ip.src'],
          period: 60,
          requests_per_period: 50,
          counting_expression: 'http.request.method ne "GET"',
        },
      },
    },
  ],
});
```

## Skip Rules

```typescript
await client.rulesets.create({
  zone_id: 'zone_id',
  kind: 'zone',
  phase: 'http_request_firewall_custom',
  name: 'Skip Rules',
  rules: [
    // Skip static assets (current ruleset only)
    {
      action: 'skip',
      action_parameters: { ruleset: 'current' },
      expression: 'http.request.uri.path matches "\\.(jpg|css|js|woff2?)$"',
    },
    
    // Skip all WAF phases for trusted IPs
    {
      action: 'skip',
      action_parameters: {
        phases: ['http_request_firewall_managed', 'http_ratelimit'],
      },
      expression: 'ip.src in {192.0.2.0/24}',
    },
  ],
});
```

## Complete Setup Example

Combine all three phases for comprehensive protection:

```typescript
const client = new Cloudflare({ apiToken: process.env.CF_API_TOKEN });
const zoneId = process.env.ZONE_ID;

// 1. Custom rules (execute first)
await client.rulesets.create({
  zone_id: zoneId,
  phase: 'http_request_firewall_custom',
  rules: [
    { action: 'skip', action_parameters: { phases: ['http_request_firewall_managed', 'http_ratelimit'] }, expression: 'ip.src in {192.0.2.0/24}' },
    { action: 'block', expression: 'cf.waf.score gt 50' },
    { action: 'managed_challenge', expression: 'cf.waf.score gt 20' },
  ],
});

// 2. Managed ruleset (execute second)
await client.rulesets.create({
  zone_id: zoneId,
  phase: 'http_request_firewall_managed',
  rules: [{
    action: 'execute',
    action_parameters: { id: 'efb7b8c949ac4650a09736fc376e9aee', overrides: { categories: [{ category: 'wordpress', enabled: false }] } },
    expression: 'true',
  }],
});

// 3. Rate limiting (execute third)
await client.rulesets.create({
  zone_id: zoneId,
  phase: 'http_ratelimit',
  rules: [
    { action: 'block', expression: 'true', action_parameters: { ratelimit: { characteristics: ['cf.colo.id', 'ip.src'], period: 60, requests_per_period: 100, mitigation_timeout: 600 } } },
    { action: 'block', expression: 'http.request.uri.path eq "/api/login"', action_parameters: { ratelimit: { characteristics: ['ip.src'], period: 60, requests_per_period: 5, mitigation_timeout: 600 } } },
  ],
});
```

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
