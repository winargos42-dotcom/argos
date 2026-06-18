---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/claude-opus-4-5-migration/references/effort.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\claude-opus-4-5-migration\references\effort.md
source_ext: .md
source_sha256: d3e15875e1ed734d46a5c2f2ec987288ee7f94eb4b11d7058aaf0acabe332ccd
text_sha256: 1d10254a2089682bedc2dcc68243221f9b67f852fdf8e8992fa3eb1f731763ca
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# effort.md

- Source: `claude-code-templates/cli-tool/components/skills/development/claude-opus-4-5-migration/references/effort.md`
- Extract: `text`
- SHA256: `d3e15875e1ed734d46a5c2f2ec987288ee7f94eb4b11d7058aaf0acabe332ccd`

## Content

# Effort Parameter (Beta)

**Add effort set to `"high"` during migration.** This is the default configuration for best performance with Opus 4.5.

## Overview

Effort controls how eagerly Claude spends tokens. It affects all tokens: thinking, text responses, and function calls.

| Effort | Use Case |
|--------|----------|
| `high` | Best performance, deep reasoning (default) |
| `medium` | Balance of cost/latency vs. performance |
| `low` | Simple, high-volume queries; significant token savings |

## Implementation

Requires beta flag `effort-2025-11-24` in API calls.

**Python SDK:**
```python
response = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=1024,
    betas=["effort-2025-11-24"],
    output_config={
        "effort": "high"  # or "medium" or "low"
    },
    messages=[...]
)
```

**TypeScript SDK:**
```typescript
const response = await client.messages.create({
  model: "claude-opus-4-5-20251101",
  max_tokens: 1024,
  betas: ["effort-2025-11-24"],
  output_config: {
    effort: "high"  // or "medium" or "low"
  },
  messages: [...]
});
```

**Raw API:**
```json
{
  "model": "claude-opus-4-5-20251101",
  "max_tokens": 1024,
  "anthropic-beta": "effort-2025-11-24",
  "output_config": {
    "effort": "high"
  },
  "messages": [...]
}
```

## Effort vs. Thinking Budget

Effort is independent of thinking budget:

- High effort + no thinking = more tokens, but no thinking tokens
- High effort + 32k thinking = more tokens, but thinking capped at 32k

## Recommendations

1. First determine effort level, then set thinking budget
2. Best performance: high effort + high thinking budget
3. Cost/latency optimization: medium effort
4. Simple high-volume queries: low effort

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
