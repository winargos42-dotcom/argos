---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/dynamic-routing.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\ai-gateway\dynamic-routing.md
source_ext: .md
source_sha256: 605d7a64e1db579f6212d3a189203dff4e3029ccc1301dee99385f463f851b56
text_sha256: 56f3539a61bae2fda7d8a98c81ed14e820caf733f27e6cce2fffeeaf7a6c1db5
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# dynamic-routing.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/ai-gateway/dynamic-routing.md`
- Extract: `text`
- SHA256: `605d7a64e1db579f6212d3a189203dff4e3029ccc1301dee99385f463f851b56`

## Content

# Dynamic Routing

Configure complex routing in dashboard without code changes. Use route names instead of model names.

## Usage

```typescript
const response = await client.chat.completions.create({
  model: 'dynamic/smart-chat', // Route name from dashboard
  messages: [{ role: 'user', content: 'Hello!' }]
});
```

## Node Types

| Node | Purpose | Use Case |
|------|---------|----------|
| **Conditional** | Branch on metadata | Paid vs free users, geo routing |
| **Percentage** | A/B split traffic | Model testing, gradual rollouts |
| **Rate Limit** | Enforce quotas | Per-user/team limits |
| **Budget Limit** | Cost quotas | Per-user spending caps |
| **Model** | Call provider | Final destination |

## Metadata

Pass via header (max 5 entries, flat only):
```typescript
headers: {
  'cf-aig-metadata': JSON.stringify({
    userId: 'user-123',
    tier: 'pro',
    region: 'us-east'
  })
}
```

## Common Patterns

**Multi-model fallback:**
```
Start → GPT-4 → On error: Claude → On error: Llama
```

**Tiered access:**
```
Conditional: tier == 'enterprise' → GPT-4 (no limit)
Conditional: tier == 'pro' → Rate Limit 1000/hr → GPT-4o
Conditional: tier == 'free' → Rate Limit 10/hr → GPT-4o-mini
```

**Gradual rollout:**
```
Percentage: 10% → New model, 90% → Old model
```

**Cost-based fallback:**
```
Budget Limit: $100/day per teamId
  < 80%: GPT-4
  >= 80%: GPT-4o-mini
  >= 100%: Error
```

## Version Management

- Save changes as new version
- Test with `model: 'dynamic/route@v2'`
- Roll back by deploying previous version

## Monitoring

Dashboard → Gateway → Dynamic Routes:
- Request count per path
- Success/error rates
- Latency/cost by path

## Limitations

- Max 5 metadata entries
- Values: string/number/boolean/null only
- No nested objects
- Route names: alphanumeric + hyphens

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
