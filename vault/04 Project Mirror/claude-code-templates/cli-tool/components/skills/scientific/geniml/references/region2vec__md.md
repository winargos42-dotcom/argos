---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/geniml/references/region2vec.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\geniml\references\region2vec.md
source_ext: .md
source_sha256: ffe8415ea1950889bde8f22d3aef4b3e3fda62ae018658ed97374e7ca5e07256
text_sha256: 225b691d65d220df3f92979215eb659ec232152d110190a1a9887bc3929eba4e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:49
---

# region2vec.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/geniml/references/region2vec.md`
- Extract: `text`
- SHA256: `ffe8415ea1950889bde8f22d3aef4b3e3fda62ae018658ed97374e7ca5e07256`

## Content

# Region2Vec: Genomic Region Embeddings

## Overview

Region2Vec generates unsupervised embeddings of genomic regions and region sets from BED files. It maps genomic regions to a vocabulary, creates sentences through concatenation, and applies word2vec training to learn meaningful representations.

## When to Use

Use Region2Vec when working with:
- BED file collections requiring dimensionality reduction
- Genomic region similarity analysis
- Downstream ML tasks requiring region feature vectors
- Comparative analysis across multiple genomic datasets

## Workflow

### Step 1: Prepare Data

Gather BED files in a source folder. Optionally specify a file list (default uses all files in the directory). Prepare a universe file as the reference vocabulary for tokenization.

### Step 2: Tokenization

Run hard tokenization to convert genomic regions into tokens:

```python
from geniml.tokenization import hard_tokenization

src_folder = '/path/to/raw/bed/files'
dst_folder = '/path/to/tokenized_files'
universe_file = '/path/to/universe_file.bed'

hard_tokenization(src_folder, dst_folder, universe_file, 1e-9)
```

The final parameter (1e-9) is the p-value threshold for tokenization overlap significance.

### Step 3: Train Region2Vec Model

Execute Region2Vec training on the tokenized files:

```python
from geniml.region2vec import region2vec

region2vec(
    token_folder=dst_folder,
    save_dir='./region2vec_model',
    num_shufflings=1000,
    embedding_dim=100,
    context_len=50,
    window_size=5,
    init_lr=0.025
)
```

## Key Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `init_lr` | Initial learning rate | 0.01 - 0.05 |
| `window_size` | Context window size | 3 - 10 |
| `num_shufflings` | Number of shuffling iterations | 500 - 2000 |
| `embedding_dim` | Dimension of output embeddings | 50 - 300 |
| `context_len` | Context length for training | 30 - 100 |

## CLI Usage

```bash
geniml region2vec --token-folder /path/to/tokens \
  --save-dir ./region2vec_model \
  --num-shuffle 1000 \
  --embed-dim 100 \
  --context-len 50 \
  --window-size 5 \
  --init-lr 0.025
```

## Best Practices

- **Parameter tuning**: Frequently tune `init_lr`, `window_size`, `num_shufflings`, and `embedding_dim` for optimal performance on your specific dataset
- **Universe file**: Use a comprehensive universe file that covers all regions of interest in your analysis
- **Validation**: Always validate tokenization output before proceeding to training
- **Resources**: Training can be computationally intensive; monitor memory usage with large datasets

## Output

The trained model saves embeddings that can be used for:
- Similarity searches across genomic regions
- Clustering region sets
- Feature vectors for downstream ML tasks
- Visualization via dimensionality reduction (t-SNE, UMAP)

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
