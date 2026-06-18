---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/mechanistic-interpretability-saelens/references/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\mechanistic-interpretability-saelens\references\README.md
source_ext: .md
source_sha256: ac2bb88fd1a67b5106a9166e8f572266094e432f1ae6407f19daa64ded0d6e64
text_sha256: 1ae9c3f499b5db57c344f05a654a8ab012d10dd59c059f55615e0ada28f349e0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/mechanistic-interpretability-saelens/references/README.md`
- Extract: `text`
- SHA256: `ac2bb88fd1a67b5106a9166e8f572266094e432f1ae6407f19daa64ded0d6e64`

## Content

# SAELens Reference Documentation

This directory contains comprehensive reference materials for SAELens.

## Contents

- [api.md](api.md) - Complete API reference for SAE, TrainingSAE, and configuration classes
- [tutorials.md](tutorials.md) - Step-by-step tutorials for training and analyzing SAEs
- [papers.md](papers.md) - Key research papers on sparse autoencoders

## Quick Links

- **GitHub Repository**: https://github.com/jbloomAus/SAELens
- **Neuronpedia**: https://neuronpedia.org (browse pre-trained SAE features)
- **HuggingFace SAEs**: Search for tag `saelens`

## Installation

```bash
pip install sae-lens
```

Requirements: Python 3.10+, transformer-lens>=2.0.0

## Basic Usage

```python
from transformer_lens import HookedTransformer
from sae_lens import SAE

# Load model and SAE
model = HookedTransformer.from_pretrained("gpt2-small", device="cuda")
sae, cfg_dict, sparsity = SAE.from_pretrained(
    release="gpt2-small-res-jb",
    sae_id="blocks.8.hook_resid_pre",
    device="cuda"
)

# Encode activations to sparse features
tokens = model.to_tokens("Hello world")
_, cache = model.run_with_cache(tokens)
activations = cache["resid_pre", 8]

features = sae.encode(activations)  # Sparse feature activations
reconstructed = sae.decode(features)  # Reconstructed activations
```

## Key Concepts

### Sparse Autoencoders
SAEs decompose dense neural activations into sparse, interpretable features:
- **Encoder**: Maps d_model → d_sae (typically 4-16x expansion)
- **ReLU/TopK**: Enforces sparsity
- **Decoder**: Reconstructs original activations

### Training Loss
`Loss = MSE(original, reconstructed) + L1_coefficient × L1(features)`

### Key Metrics
- **L0**: Average number of active features (target: 50-200)
- **CE Loss Score**: Cross-entropy recovered vs original model (target: 80-95%)
- **Dead Features**: Features that never activate (target: <5%)

## Available Pre-trained SAEs

| Release | Model | Description |
|---------|-------|-------------|
| `gpt2-small-res-jb` | GPT-2 Small | Residual stream SAEs |
| `gemma-2b-res` | Gemma 2B | Residual stream SAEs |
| Various | Search HuggingFace | Community-trained SAEs |

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
