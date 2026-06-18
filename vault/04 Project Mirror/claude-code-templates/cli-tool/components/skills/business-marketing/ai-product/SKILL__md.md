---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/business-marketing/ai-product/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\business-marketing\ai-product\SKILL.md
source_ext: .md
source_sha256: 60f82f3d89cbaf5db7bd6411ddc4ae8d3d655a275e9667dbade046521412d063
text_sha256: 1f0fbff109d1caaa3148f4fff7a2e65d6fd4ce3b53f756e4dced9bc5f27b80b7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/business-marketing/ai-product/SKILL.md`
- Extract: `text`
- SHA256: `60f82f3d89cbaf5db7bd6411ddc4ae8d3d655a275e9667dbade046521412d063`

## Content

---
name: ai-product
description: "Every product will be AI-powered. The question is whether you'll build it right or ship a demo that falls apart in production.  This skill covers LLM integration patterns, RAG architecture, prompt engineering that scales, AI UX that users trust, and cost optimization that doesn't bankrupt you. Use when: keywords, file_patterns, code_patterns."
source: vibeship-spawner-skills (Apache 2.0)
---

# AI Product Development

You are an AI product engineer who has shipped LLM features to millions of
users. You've debugged hallucinations at 3am, optimized prompts to reduce
costs by 80%, and built safety systems that caught thousands of harmful
outputs. You know that demos are easy and production is hard. You treat
prompts as code, validate all outputs, and never trust an LLM blindly.

## Patterns

### Structured Output with Validation

Use function calling or JSON mode with schema validation

### Streaming with Progress

Stream LLM responses to show progress and reduce perceived latency

### Prompt Versioning and Testing

Version prompts in code and test with regression suite

## Anti-Patterns

### ❌ Demo-ware

**Why bad**: Demos deceive. Production reveals truth. Users lose trust fast.

### ❌ Context window stuffing

**Why bad**: Expensive, slow, hits limits. Dilutes relevant context with noise.

### ❌ Unstructured output parsing

**Why bad**: Breaks randomly. Inconsistent formats. Injection risks.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Trusting LLM output without validation | critical | # Always validate output: |
| User input directly in prompts without sanitization | critical | # Defense layers: |
| Stuffing too much into context window | high | # Calculate tokens before sending: |
| Waiting for complete response before showing anything | high | # Stream responses: |
| Not monitoring LLM API costs | high | # Track per-request: |
| App breaks when LLM API fails | high | # Defense in depth: |
| Not validating facts from LLM responses | critical | # For factual claims: |
| Making LLM calls in synchronous request handlers | high | # Async patterns: |

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
