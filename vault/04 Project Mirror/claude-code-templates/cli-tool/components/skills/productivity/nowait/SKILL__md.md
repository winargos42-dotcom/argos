---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/nowait/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\nowait\SKILL.md
source_ext: .md
source_sha256: 764adc5dbe2f614eebe89848bb0e51ee51045d7022b9c3c0439efd4b0b5d019f
text_sha256: fd71e79f36014d423e296fa7e71e48aa5ec437c15a8d096033766a898afc8a25
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/nowait/SKILL.md`
- Extract: `text`
- SHA256: `764adc5dbe2f614eebe89848bb0e51ee51045d7022b9c3c0439efd4b0b5d019f`

## Content

---
name: nowait-reasoning-optimizer
description: Implements the NOWAIT technique for efficient reasoning in R1-style LLMs. Use when optimizing inference of reasoning models (QwQ, DeepSeek-R1, Phi4-Reasoning, Qwen3, Kimi-VL, QvQ), reducing chain-of-thought token usage by 27-51% while preserving accuracy. Triggers on "optimize reasoning", "reduce thinking tokens", "efficient inference", "suppress reflection tokens", or when working with verbose CoT outputs.
---

# NOWAIT Reasoning Optimizer

Implements the NOWAIT technique from the paper "Wait, We Don't Need to 'Wait'! Removing Thinking Tokens Improves Reasoning Efficiency" (Wang et al., 2025).

## Overview

NOWAIT is a training-free inference-time intervention that suppresses self-reflection tokens (e.g., "Wait", "Hmm", "Alternatively") during generation, reducing chain-of-thought (CoT) trajectory length by **27-51%** without compromising model utility.

## When to Use

- Deploying R1-style reasoning models with limited compute
- Reducing inference latency for production systems
- Optimizing token costs for reasoning tasks
- Working with verbose CoT outputs that need streamlining

## Supported Models

| Model Series | Type | Token Reduction |
|--------------|------|-----------------|
| QwQ-32B | RL-based | 16-31% |
| Phi4-Reasoning-Plus | RL-based | 23-28% |
| Qwen3-32B | RL-based | 13-16% |
| Kimi-VL-A3B | Multimodal | 40-60% |
| QvQ-72B-Preview | Multimodal | 20-30% |

**Important**: NOWAIT works best with RL-based models. Distilled models (Qwen3-4B/8B/14B) show degraded performance when reflection tokens are suppressed.

## Quick Start

### 1. Basic Implementation

```python
from scripts.nowait_processor import NOWAITLogitProcessor

# Initialize processor for your model's tokenizer
processor = NOWAITLogitProcessor(tokenizer)

# Use during generation
outputs = model.generate(
    inputs,
    logits_processor=[processor],
    max_new_tokens=32768
)
```

### 2. Keywords Suppressed

See `references/keywords.md` for the complete list. Core keywords:

```
wait, alternatively, hmm, but, however, check, 
double-check, maybe, verify, again, oh, ah
```

## How It Works

1. **Initialize Keywords**: Identify reflection keywords from empirical analysis
2. **Expand to Token Variants**: Map keywords to all token variants in vocabulary (e.g., "wait" → " wait", "Wait", " Wait", ".wait", "WAIT")
3. **Suppress During Inference**: Set logits of reflection tokens to large negative values during decoding

```
Logits (Before)         Logits (After)
Wait     0.8     →     Wait     -inf
First    0.6     →     First    0.6
Hmm      0.5     →     Hmm      -inf
Let      0.4     →     Let      0.4
```

## Key Findings

### Why It Works

- NOWAIT doesn't eliminate self-reflection entirely—it guides models to skip **unnecessary** "waiting" reasoning
- Models still perform essential verification at key decision points
- Results in more linear, straightforward reasoning paths

### RL vs Distilled Models

| Model Type | NOWAIT Effect | Recommendation |
|------------|---------------|----------------|
| RL-based (QwQ, Phi4, Qwen3-32B) | Stable accuracy, significant token reduction | ✅ Recommended |
| Distilled (Qwen3-4B/8B/14B) | Accuracy degradation on hard tasks | ⚠️ Use with caution |

Distilled models rely heavily on CoT structure from training data—removing reflection tokens disrupts their reasoning patterns.

## Integration Examples

### HuggingFace Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from scripts.nowait_processor import NOWAITLogitProcessor

model = AutoModelForCausalLM.from_pretrained("Qwen/QwQ-32B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/QwQ-32B")

processor = NOWAITLogitProcessor(tokenizer)

response = model.generate(
    tokenizer(prompt, return_tensors="pt").input_ids,
    logits_processor=[processor],
    max_new_tokens=32768,
    do_sample=True,
    temperature=0.7
)
```

### vLLM

```python
from vllm import LLM, SamplingParams
from scripts.nowait_processor import get_nowait_bad_words_ids

llm = LLM(model="Qwen/QwQ-32B")
bad_words_ids = get_nowait_bad_words_ids(llm.get_tokenizer())

sampling_params = SamplingParams(
    max_tokens=32768,
    bad_words_ids=bad_words_ids
)
```

## Expected Results

| Task Type | Original Tokens | NOWAIT Tokens | Reduction |
|-----------|-----------------|---------------|-----------|
| Math (AIME) | 15,000 | 10,500 | 30% |
| Visual QA (MMMU) | 2,900 | 1,450 | 50% |
| Video QA (MMVU) | 1,700 | 1,250 | 27% |

## Limitations

- Less effective on very simple problems where CoT overhead is already minimal
- Distilled models may suffer accuracy loss on challenging tasks
- Some domains may require model-specific keyword tuning

## References

- Paper: arXiv:2506.08343v2
- Complete keyword list: `references/keywords.md`
- Implementation: `scripts/nowait_processor.py`

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
