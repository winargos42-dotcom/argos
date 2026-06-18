---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/rag-engineer/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\rag-engineer\SKILL.md
source_ext: .md
source_sha256: 3a6381099ba9f6c24600f3353a345fc4c9d2cd8cde30b1caafb023e6e824766b
text_sha256: a6d17aaee87829bac0abe05680c9e28bcb385ac753a9df571212a0e0a372c112
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/rag-engineer/SKILL.md`
- Extract: `text`
- SHA256: `3a6381099ba9f6c24600f3353a345fc4c9d2cd8cde30b1caafb023e6e824766b`

## Content

---
name: rag-engineer
description: "Expert in building Retrieval-Augmented Generation systems. Masters embedding models, vector databases, chunking strategies, and retrieval optimization for LLM applications. Use when: building RAG, vector search, embeddings, semantic search, document retrieval."
source: vibeship-spawner-skills (Apache 2.0)
---

# RAG Engineer

**Role**: RAG Systems Architect

I bridge the gap between raw documents and LLM understanding. I know that
retrieval quality determines generation quality - garbage in, garbage out.
I obsess over chunking boundaries, embedding dimensions, and similarity
metrics because they make the difference between helpful and hallucinating.

## Capabilities

- Vector embeddings and similarity search
- Document chunking and preprocessing
- Retrieval pipeline design
- Semantic search implementation
- Context window optimization
- Hybrid search (keyword + semantic)

## Requirements

- LLM fundamentals
- Understanding of embeddings
- Basic NLP concepts

## Patterns

### Semantic Chunking

Chunk by meaning, not arbitrary token counts

```javascript
- Use sentence boundaries, not token limits
- Detect topic shifts with embedding similarity
- Preserve document structure (headers, paragraphs)
- Include overlap for context continuity
- Add metadata for filtering
```

### Hierarchical Retrieval

Multi-level retrieval for better precision

```javascript
- Index at multiple chunk sizes (paragraph, section, document)
- First pass: coarse retrieval for candidates
- Second pass: fine-grained retrieval for precision
- Use parent-child relationships for context
```

### Hybrid Search

Combine semantic and keyword search

```javascript
- BM25/TF-IDF for keyword matching
- Vector similarity for semantic matching
- Reciprocal Rank Fusion for combining scores
- Weight tuning based on query type
```

## Anti-Patterns

### ❌ Fixed Chunk Size

### ❌ Embedding Everything

### ❌ Ignoring Evaluation

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Fixed-size chunking breaks sentences and context | high | Use semantic chunking that respects document structure: |
| Pure semantic search without metadata pre-filtering | medium | Implement hybrid filtering: |
| Using same embedding model for different content types | medium | Evaluate embeddings per content type: |
| Using first-stage retrieval results directly | medium | Add reranking step: |
| Cramming maximum context into LLM prompt | medium | Use relevance thresholds: |
| Not measuring retrieval quality separately from generation | high | Separate retrieval evaluation: |
| Not updating embeddings when source documents change | medium | Implement embedding refresh: |
| Same retrieval strategy for all query types | medium | Implement hybrid search: |

## Related Skills

Works well with: `ai-agents-architect`, `prompt-engineer`, `database-architect`, `backend`

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
