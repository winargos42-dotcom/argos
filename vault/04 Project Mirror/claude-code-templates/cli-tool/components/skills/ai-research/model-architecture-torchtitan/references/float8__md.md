---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/model-architecture-torchtitan/references/float8.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\model-architecture-torchtitan\references\float8.md
source_ext: .md
source_sha256: 4837ac23c3867d7649ea92933ea7d62a2ed84a9664194f509bdd5ae36e387692
text_sha256: 33f05eacea84e571e4fc77fa39a1ec751c740645af14832322f80f63cdbe6ab8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# float8.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/model-architecture-torchtitan/references/float8.md`
- Extract: `text`
- SHA256: `4837ac23c3867d7649ea92933ea7d62a2ed84a9664194f509bdd5ae36e387692`

## Content

# Float8 Training in TorchTitan

Float8 training provides substantial speedups for models where GEMMs are large enough that the FP8 tensorcore speedup outweighs dynamic quantization overhead.

## Hardware Requirements

- NVIDIA H100 or newer GPUs (FP8 Tensor Cores)
- Blackwell GPUs for MXFP8 training

## Installation

```bash
USE_CPP=0 pip install git+https://github.com/pytorch/ao.git
```

## Usage: Tensorwise Scaling

Standard Float8 with tensorwise dynamic scaling:

```bash
CONFIG_FILE="./torchtitan/models/llama3/train_configs/llama3_8b.toml" ./run_train.sh \
  --model.converters="quantize.linear.float8" \
  --quantize.linear.float8.enable_fsdp_float8_all_gather \
  --quantize.linear.float8.precompute_float8_dynamic_scale_for_fsdp \
  --compile.enable
```

### Key Arguments

| Argument | Description |
|----------|-------------|
| `--model.converters="quantize.linear.float8"` | Swap `nn.Linear` with `Float8Linear` |
| `--quantize.linear.float8.enable_fsdp_float8_all_gather` | Communicate in float8 to save bandwidth |
| `--quantize.linear.float8.precompute_float8_dynamic_scale_for_fsdp` | Single all-reduce for all AMAX/scales |
| `--compile.enable` | Required - fuses float8 scaling/casting kernels |

## Usage: Rowwise Scaling

Higher accuracy than tensorwise scaling:

```bash
CONFIG_FILE="./torchtitan/models/llama3/train_configs/llama3_8b.toml" ./run_train.sh \
  --model.converters="quantize.linear.float8" \
  --quantize.linear.float8.recipe_name rowwise \
  --compile.enable
```

## Filtering Layers

Not all layers benefit from Float8. Filter small layers:

```bash
--quantize.linear.float8.filter_fqns="attention.wk,attention.wv,output"
```

### Auto-filtering

Automatically skip layers too small to benefit:

```bash
--quantize.linear.float8.filter_fqns="auto_filter_small_kn"
```

Thresholds based on H100 microbenchmarks where speedup > overhead.

## TOML Configuration

```toml
[model]
converters = ["quantize.linear.float8"]

[quantize.linear.float8]
enable_fsdp_float8_all_gather = true
precompute_float8_dynamic_scale_for_fsdp = true
filter_fqns = ["output", "auto_filter_small_kn"]

[compile]
enable = true
components = ["model", "loss"]
```

## How Float8 Works with Distributed Training

### Single Device

Cast input and weight to float8 inside forward before calling `torch._scaled_mm`:

```python
# Float8 matmul requires scales
torch._scaled_mm(input_fp8, weight_fp8, scale_a=scale_input, scale_b=scale_weight)
```

### FSDP + Float8

1. Cast sharded high-precision weights (1/N per rank) to float8
2. Perform float8 all-gather (saves bandwidth vs bf16/fp32)
3. Communicate `max(abs)` across ranks for scale computation
4. At forward start, have unsharded float8 weights ready

**Net benefit**: Float8 all-gather + amax communication can beat bf16/fp32 all-gather, depending on world size and message size.

### TP + Float8

- **Input**: Cast sharded input to float8, all-gather in float8
- **Weights**: Communicate `max(abs)` for sharded weights
- **Matmul**: Float8 input (unsharded) x float8 weight (sharded) with global scales

## Scaling Strategies

| Strategy | Status | Description |
|----------|--------|-------------|
| Tensorwise dynamic | Stable | Single scale per tensor |
| Rowwise dynamic | Alpha | Scale per row, higher accuracy |

## Performance Gains

From benchmarks on H100:

| Configuration | TPS/GPU | vs Baseline |
|---------------|---------|-------------|
| FSDP only | 5,762 | - |
| FSDP + compile | 6,667 | +16% |
| FSDP + compile + Float8 | 8,532 | +48% |

## Determining Float8 Benefit

Check [torchao microbenchmarks](https://github.com/pytorch/ao/tree/main/torchao/float8#performance) for forward+backward pass speedups on "layer norm => linear => sigmoid" for different M,N,K sizes.

Rule of thumb: GEMMs with K,N > 4096 typically benefit from Float8.

## MXFP8 Training (Blackwell)

For NVIDIA Blackwell GPUs, TorchTitan supports MXFP8 (Microscaling FP8) for both dense and MoE models. See [docs/mxfp8.md](https://github.com/pytorch/torchtitan/blob/main/docs/mxfp8.md) for details.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
