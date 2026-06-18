---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/data-processing-nemo-curator/references/deduplication.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\data-processing-nemo-curator\references\deduplication.md
source_ext: .md
source_sha256: 9a7cd819fc042efcf3fa027a29f30595133c85df831bbfd5ece6f892c21180a1
text_sha256: ca5594ba9ee317726f7f5932d89f82b7be0b2db9744e41b935f541bd13f2fa0a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# deduplication.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/data-processing-nemo-curator/references/deduplication.md`
- Extract: `text`
- SHA256: `9a7cd819fc042efcf3fa027a29f30595133c85df831bbfd5ece6f892c21180a1`

## Content

# Deduplication Guide

Complete guide to exact, fuzzy, and semantic deduplication.

## Exact deduplication

Remove documents with identical content.

```python
from nemo_curator.modules import ExactDuplicates

# Exact deduplication
exact_dedup = ExactDuplicates(
    id_field="id",
    text_field="text",
    hash_method="md5"  # or "sha256"
)

deduped = exact_dedup(dataset)
```

**Performance**: ~16× faster on GPU vs CPU

## Fuzzy deduplication

Remove near-duplicate documents using MinHash + LSH.

```python
from nemo_curator.modules import FuzzyDuplicates

fuzzy_dedup = FuzzyDuplicates(
    id_field="id",
    text_field="text",
    num_hashes=260,        # MinHash permutations (more = accurate)
    num_buckets=20,        # LSH buckets (more = faster, less recall)
    hash_method="md5",
    jaccard_threshold=0.8  # Similarity threshold
)

deduped = fuzzy_dedup(dataset)
```

**Parameters**:
- `num_hashes`: 128-512 (default 260)
- `num_buckets`: 10-50 (default 20)
- `jaccard_threshold`: 0.7-0.9 (default 0.8)

**Performance**: 16× faster on 8TB dataset (120h → 7.5h)

## Semantic deduplication

Remove semantically similar documents using embeddings.

```python
from nemo_curator.modules import SemanticDuplicates

semantic_dedup = SemanticDuplicates(
    id_field="id",
    text_field="text",
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    embedding_batch_size=256,
    threshold=0.85,  # Cosine similarity threshold
    device="cuda"
)

deduped = semantic_dedup(dataset)
```

**Models**:
- `all-MiniLM-L6-v2`: Fast, 384 dims
- `all-mpnet-base-v2`: Better quality, 768 dims
- Custom models supported

## Comparison

| Method | Speed | Recall | Use Case |
|--------|-------|--------|----------|
| Exact | Fastest | 100% | Exact matches only |
| Fuzzy | Fast | ~95% | Near-duplicates (recommended) |
| Semantic | Slow | ~90% | Paraphrases, rewrites |

## Best practices

1. **Start with exact dedup** - Remove obvious duplicates
2. **Use fuzzy for large datasets** - Best speed/quality trade-off
3. **Semantic for high-value data** - Expensive but thorough
4. **GPU acceleration required** - 10-16× speedup

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
