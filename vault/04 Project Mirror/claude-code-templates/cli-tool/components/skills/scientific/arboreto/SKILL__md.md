---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/arboreto/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\arboreto\SKILL.md
source_ext: .md
source_sha256: bcecad73c5577ba4e684ae77c676e045c1ca8392ca620d83a3acef358972286e
text_sha256: 5723a054405c0506581a0b27490b7316eb0c35312568373e95ac7779d368abf1
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/arboreto/SKILL.md`
- Extract: `text`
- SHA256: `bcecad73c5577ba4e684ae77c676e045c1ca8392ca620d83a3acef358972286e`

## Content

---
name: arboreto
description: Infer gene regulatory networks (GRNs) from gene expression data using scalable algorithms (GRNBoost2, GENIE3). Use when analyzing transcriptomics data (bulk RNA-seq, single-cell RNA-seq) to identify transcription factor-target gene relationships and regulatory interactions. Supports distributed computation for large-scale datasets.
---

# Arboreto

## Overview

Arboreto is a computational library for inferring gene regulatory networks (GRNs) from gene expression data using parallelized algorithms that scale from single machines to multi-node clusters.

**Core capability**: Identify which transcription factors (TFs) regulate which target genes based on expression patterns across observations (cells, samples, conditions).

## Quick Start

Install arboreto:
```bash
uv pip install arboreto
```

Basic GRN inference:
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load expression data (genes as columns)
    expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')

    # Infer regulatory network
    network = grnboost2(expression_data=expression_matrix)

    # Save results (TF, target, importance)
    network.to_csv('network.tsv', sep='\t', index=False, header=False)
```

**Critical**: Always use `if __name__ == '__main__':` guard because Dask spawns new processes.

## Core Capabilities

### 1. Basic GRN Inference

For standard GRN inference workflows including:
- Input data preparation (Pandas DataFrame or NumPy array)
- Running inference with GRNBoost2 or GENIE3
- Filtering by transcription factors
- Output format and interpretation

**See**: `references/basic_inference.md`

**Use the ready-to-run script**: `scripts/basic_grn_inference.py` for standard inference tasks:
```bash
python scripts/basic_grn_inference.py expression_data.tsv output_network.tsv --tf-file tfs.txt --seed 777
```

### 2. Algorithm Selection

Arboreto provides two algorithms:

**GRNBoost2 (Recommended)**:
- Fast gradient boosting-based inference
- Optimized for large datasets (10k+ observations)
- Default choice for most analyses

**GENIE3**:
- Random Forest-based inference
- Original multiple regression approach
- Use for comparison or validation

Quick comparison:
```python
from arboreto.algo import grnboost2, genie3

# Fast, recommended
network_grnboost = grnboost2(expression_data=matrix)

# Classic algorithm
network_genie3 = genie3(expression_data=matrix)
```

**For detailed algorithm comparison, parameters, and selection guidance**: `references/algorithms.md`

### 3. Distributed Computing

Scale inference from local multi-core to cluster environments:

**Local (default)** - Uses all available cores automatically:
```python
network = grnboost2(expression_data=matrix)
```

**Custom local client** - Control resources:
```python
from distributed import LocalCluster, Client

local_cluster = LocalCluster(n_workers=10, memory_limit='8GB')
client = Client(local_cluster)

network = grnboost2(expression_data=matrix, client_or_address=client)

client.close()
local_cluster.close()
```

**Cluster computing** - Connect to remote Dask scheduler:
```python
from distributed import Client

client = Client('tcp://scheduler:8786')
network = grnboost2(expression_data=matrix, client_or_address=client)
```

**For cluster setup, performance optimization, and large-scale workflows**: `references/distributed_computing.md`

## Installation

```bash
uv pip install arboreto
```

**Dependencies**: scipy, scikit-learn, numpy, pandas, dask, distributed

## Common Use Cases

### Single-Cell RNA-seq Analysis
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load single-cell expression matrix (cells x genes)
    sc_data = pd.read_csv('scrna_counts.tsv', sep='\t')

    # Infer cell-type-specific regulatory network
    network = grnboost2(expression_data=sc_data, seed=42)

    # Filter high-confidence links
    high_confidence = network[network['importance'] > 0.5]
    high_confidence.to_csv('grn_high_confidence.tsv', sep='\t', index=False)
```

### Bulk RNA-seq with TF Filtering
```python
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load data
    expression_data = pd.read_csv('rnaseq_tpm.tsv', sep='\t')
    tf_names = load_tf_names('human_tfs.txt')

    # Infer with TF restriction
    network = grnboost2(
        expression_data=expression_data,
        tf_names=tf_names,
        seed=123
    )

    network.to_csv('tf_target_network.tsv', sep='\t', index=False)
```

### Comparative Analysis (Multiple Conditions)
```python
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Infer networks for different conditions
    conditions = ['control', 'treatment_24h', 'treatment_48h']

    for condition in conditions:
        data = pd.read_csv(f'{condition}_expression.tsv', sep='\t')
        network = grnboost2(expression_data=data, seed=42)
        network.to_csv(f'{condition}_network.tsv', sep='\t', index=False)
```

## Output Interpretation

Arboreto returns a DataFrame with regulatory links:

| Column | Description |
|--------|-------------|
| `TF` | Transcription factor (regulator) |
| `target` | Target gene |
| `importance` | Regulatory importance score (higher = stronger) |

**Filtering strategy**:
- Top N links per target gene
- Importance threshold (e.g., > 0.5)
- Statistical significance testing (permutation tests)

## Integration with pySCENIC

Arboreto is a core component of the SCENIC pipeline for single-cell regulatory network analysis:

```python
# Step 1: Use arboreto for GRN inference
from arboreto.algo import grnboost2
network = grnboost2(expression_data=sc_data, tf_names=tf_list)

# Step 2: Use pySCENIC for regulon identification and activity scoring
# (See pySCENIC documentation for downstream analysis)
```

## Reproducibility

Always set a seed for reproducible results:
```python
network = grnboost2(expression_data=matrix, seed=777)
```

Run multiple seeds for robustness analysis:
```python
from distributed import LocalCluster, Client

if __name__ == '__main__':
    client = Client(LocalCluster())

    seeds = [42, 123, 777]
    networks = []

    for seed in seeds:
        net = grnboost2(expression_data=matrix, client_or_address=client, seed=seed)
        networks.append(net)

    # Combine networks and filter consensus links
    consensus = analyze_consensus(networks)
```

## Troubleshooting

**Memory errors**: Reduce dataset size by filtering low-variance genes or use distributed computing

**Slow performance**: Use GRNBoost2 instead of GENIE3, enable distributed client, filter TF list

**Dask errors**: Ensure `if __name__ == '__main__':` guard is present in scripts

**Empty results**: Check data format (genes as columns), verify TF names match gene names

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
