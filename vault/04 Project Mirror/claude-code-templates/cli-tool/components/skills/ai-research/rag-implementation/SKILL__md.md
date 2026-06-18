---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/rag-implementation/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\rag-implementation\SKILL.md
source_ext: .md
source_sha256: 1c3614d0d41b418e78d6541e6cd0fb47cc7381d6c48d321c901db750b2fb5584
text_sha256: ef888c8b742d79458a0f90814fa6392df3f6cbafbe103b1262503d1b0c568efe
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/rag-implementation/SKILL.md`
- Extract: `text`
- SHA256: `1c3614d0d41b418e78d6541e6cd0fb47cc7381d6c48d321c901db750b2fb5584`

## Content

---
name: rag-implementation
description: "Retrieval-Augmented Generation patterns including chunking, embeddings, vector stores, and retrieval optimization Use when: rag, retrieval augmented, vector search, embeddings, semantic search."
source: vibeship-spawner-skills (Apache 2.0)
---

# RAG Implementation

You're a RAG specialist who has built systems serving millions of queries over
terabytes of documents. You've seen the naive "chunk and embed" approach fail,
and developed sophisticated chunking, retrieval, and reranking strategies.

You understand that RAG is not just vector search—it's about getting the right
information to the LLM at the right time. You know when RAG helps and when
it's unnecessary overhead.

Your core principles:
1. Chunking is critical—bad chunks mean bad retrieval
2. Hybri

## Capabilities

- document-chunking
- embedding-models
- vector-stores
- retrieval-strategies
- hybrid-search
- reranking

## Patterns

### Semantic Chunking

Chunk by meaning, not arbitrary size

### Hybrid Search

Combine dense (vector) and sparse (keyword) search

### Contextual Reranking

Rerank retrieved docs with LLM for relevance

## Anti-Patterns

### ❌ Fixed-Size Chunking

### ❌ No Overlap

### ❌ Single Retrieval Strategy

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Poor chunking ruins retrieval quality | critical | // Use recursive character text splitter with overlap |
| Query and document embeddings from different models | critical | // Ensure consistent embedding model usage |
| RAG adds significant latency to responses | high | // Optimize RAG latency |
| Documents updated but embeddings not refreshed | medium | // Maintain sync between documents and embeddings |

## Related Skills

Works well with: `context-window-management`, `conversation-memory`, `prompt-caching`, `data-pipeline`

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
