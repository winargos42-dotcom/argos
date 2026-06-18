---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/perplexity/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\perplexity\SKILL.md
source_ext: .md
source_sha256: cabc8f5988e529d07b77fbc5bd4d75c47a4b1da2c15b3681fb5e988825bbbf2b
text_sha256: e7c8c405d1ee8cec6e06efd5fe4ca9a2dccbf6318728fe3dacdb0cd2f9470b89
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/perplexity/SKILL.md`
- Extract: `text`
- SHA256: `cabc8f5988e529d07b77fbc5bd4d75c47a4b1da2c15b3681fb5e988825bbbf2b`

## Content

---
name: perplexity
description: Web search and research using Perplexity AI. Use when user says "search", "find", "look up", "ask", "research", or "what's the latest" for generic queries. NOT for library/framework docs (use Context7) or workspace questions.
---

# Perplexity Tools

Use ONLY when user says "search", "find", "look up", "ask", "research", or "what's the latest" for generic queries. NOT for library/framework docs (use Context7), gt CLI (use Graphite MCP), or workspace questions (use Nx MCP).

## Quick Reference

**Which Perplexity tool?**
- Need search results/URLs? → **Perplexity Search**
- Need conversational answer? → **Perplexity Ask**
- Need deep research? → **Researcher agent** (`/research <topic>`)

**NOT Perplexity - use these instead:**
- Library/framework docs → **Context7 MCP**
- Graphite `gt` CLI → **Graphite MCP**
- THIS workspace → **Nx MCP**
- Specific URL → **URL Crawler**

## Perplexity Search

**When to use:**
- Generic searches, finding resources
- Current best practices, recent information
- Tutorial/blog post discovery
- User says "search for...", "find...", "look up..."

**Default parameters (ALWAYS USE):**
```typescript
mcp__perplexity__perplexity_search({
  query: "your search query",
  max_results: 3,           // Default is 10 - too many!
  max_tokens_per_page: 512  // Reduce per-result content
})
```

**When to increase limits:**
Only if:
- User explicitly needs comprehensive results
- Initial search found nothing useful
- Complex topic needs multiple sources

```typescript
// Increased limits (use sparingly)
mcp__perplexity__perplexity_search({
  query: "complex topic",
  max_results: 5,
  max_tokens_per_page: 1024
})
```

## Perplexity Ask

**When to use:**
- Need conversational explanation, not search results
- Synthesize information from web
- Explain concepts with current context

**Usage:**
```typescript
mcp__perplexity__perplexity_ask({
  messages: [
    {
      role: "user",
      content: "Explain how postgres advisory locks work"
    }
  ]
})
```

**NOT for:**
- Library documentation (use Context7)
- Deep multi-source research (use researcher agent)

## Prohibited Tool

**NEVER use:** `mcp__perplexity__perplexity_research`

**Use instead:** Researcher agent (`/research <topic>`)
- Token cost: 30-50k tokens
- Provides multi-source synthesis with citations
- Use sparingly for complex questions only

## Tool Selection Chain

**Priority order:**
1. **Context7 MCP** - Library/framework docs
2. **Graphite MCP** - Any `gt` CLI mention
3. **Nx MCP** - THIS workspace questions
4. **Perplexity Search** - Generic searches
5. **Perplexity Ask** - Conversational answers
6. **Researcher agent** - Deep multi-source research
7. **WebSearch** - Last resort (after Perplexity exhausted)

## Examples

**✅ CORRECT - Use Perplexity Search:**
- "Find postgres migration best practices"
- "Search for React testing tutorials"
- "Look up latest trends in microservices"

**✅ CORRECT - Use Perplexity Ask:**
- "Explain how postgres advisory locks work"
- "What are the trade-offs of microservices?"

**❌ WRONG - Use Context7 instead:**
- "Search for React hooks documentation" → Context7 MCP
- "Find Next.js routing docs" → Context7 MCP
- "Look up Temporal workflow API" → Context7 MCP

**❌ WRONG - Use Graphite MCP instead:**
- "Search for gt stack commands" → Graphite MCP
- "Find gt branch workflow" → Graphite MCP

**❌ WRONG - Use Nx MCP instead:**
- "Search for build config" (in THIS workspace) → Nx MCP
- "Find project dependencies" (in THIS workspace) → Nx MCP

## Key Points

- **Default to limited results** - avoid context bloat
- **Library docs = Context7** - ALWAYS try Context7 first
- **"gt" = Graphite MCP** - ANY "gt" mention uses Graphite
- **Deep research = /research** - NOT perplexity_research tool
- **Fallback chain** - Search → Ask → WebSearch (last resort)

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
