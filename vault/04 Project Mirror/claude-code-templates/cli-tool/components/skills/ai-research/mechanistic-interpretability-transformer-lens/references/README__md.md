---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/mechanistic-interpretability-transformer-lens/references/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\mechanistic-interpretability-transformer-lens\references\README.md
source_ext: .md
source_sha256: 5900507f0543b1faa43351ee6b416dfb53d627bafc676ffc443b3d5bba4952d0
text_sha256: ebdf1731226920bd3ba3fd8265e033a5e19af48651429023af9ab3ef346766b0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/mechanistic-interpretability-transformer-lens/references/README.md`
- Extract: `text`
- SHA256: `5900507f0543b1faa43351ee6b416dfb53d627bafc676ffc443b3d5bba4952d0`

## Content

# TransformerLens Reference Documentation

This directory contains comprehensive reference materials for TransformerLens.

## Contents

- [api.md](api.md) - Complete API reference for HookedTransformer, ActivationCache, and HookPoints
- [tutorials.md](tutorials.md) - Step-by-step tutorials for common interpretability workflows
- [papers.md](papers.md) - Key research papers and foundational concepts

## Quick Links

- **Official Documentation**: https://transformerlensorg.github.io/TransformerLens/
- **GitHub Repository**: https://github.com/TransformerLensOrg/TransformerLens
- **Model Properties Table**: https://transformerlensorg.github.io/TransformerLens/generated/model_properties_table.html

## Installation

```bash
pip install transformer-lens
```

## Basic Usage

```python
from transformer_lens import HookedTransformer

# Load model
model = HookedTransformer.from_pretrained("gpt2-small")

# Run with activation caching
tokens = model.to_tokens("Hello world")
logits, cache = model.run_with_cache(tokens)

# Access activations
residual = cache["resid_post", 5]  # Layer 5 residual stream
attention = cache["pattern", 3]    # Layer 3 attention patterns
```

## Key Concepts

### HookPoints
Every activation in the transformer has a HookPoint wrapper, enabling:
- Reading activations via `run_with_cache()`
- Modifying activations via `run_with_hooks()`

### Activation Cache
The `ActivationCache` stores all intermediate activations with helper methods for:
- Residual stream decomposition
- Logit attribution
- Layer-wise analysis

### Supported Models (50+)
GPT-2, LLaMA, Mistral, Pythia, GPT-Neo, OPT, Gemma, Phi, and more.

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
