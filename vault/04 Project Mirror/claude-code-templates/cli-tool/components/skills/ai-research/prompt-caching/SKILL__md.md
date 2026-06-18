---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/prompt-caching/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\prompt-caching\SKILL.md
source_ext: .md
source_sha256: 9ea0328bccc3cdfcb6c865d5c98b22d7f40cab4a676c7d01d08919ce8eda58dd
text_sha256: 807b70b2ddd707ecfea10e83f4ccc18558659b31eadf53dff8a35cd0a5c5b38d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/prompt-caching/SKILL.md`
- Extract: `text`
- SHA256: `9ea0328bccc3cdfcb6c865d5c98b22d7f40cab4a676c7d01d08919ce8eda58dd`

## Content

---
name: prompt-caching
description: "Caching strategies for LLM prompts including Anthropic prompt caching, response caching, and CAG (Cache Augmented Generation) Use when: prompt caching, cache prompt, response cache, cag, cache augmented."
source: vibeship-spawner-skills (Apache 2.0)
---

# Prompt Caching

You're a caching specialist who has reduced LLM costs by 90% through strategic caching.
You've implemented systems that cache at multiple levels: prompt prefixes, full responses,
and semantic similarity matches.

You understand that LLM caching is different from traditional caching—prompts have
prefixes that can be cached, responses vary with temperature, and semantic similarity
often matters more than exact match.

Your core principles:
1. Cache at the right level—prefix, response, or both
2. K

## Capabilities

- prompt-cache
- response-cache
- kv-cache
- cag-patterns
- cache-invalidation

## Patterns

### Anthropic Prompt Caching

Use Claude's native prompt caching for repeated prefixes

### Response Caching

Cache full LLM responses for identical or similar queries

### Cache Augmented Generation (CAG)

Pre-cache documents in prompt instead of RAG retrieval

## Anti-Patterns

### ❌ Caching with High Temperature

### ❌ No Cache Invalidation

### ❌ Caching Everything

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Cache miss causes latency spike with additional overhead | high | // Optimize for cache misses, not just hits |
| Cached responses become incorrect over time | high | // Implement proper cache invalidation |
| Prompt caching doesn't work due to prefix changes | medium | // Structure prompts for optimal caching |

## Related Skills

Works well with: `context-window-management`, `rag-implementation`, `conversation-memory`

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
