---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/post-training-trl-fine-tuning/references/online-rl.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\post-training-trl-fine-tuning\references\online-rl.md
source_ext: .md
source_sha256: cc6d45a2879a33429e9e11d608dbead2a48224a7004fc6f1f0c9a0898b8762c6
text_sha256: 35e0ad19a8e6a4bc2c1a87e1ab5e2bfe31fb74ba07b1f4b161a1c258e0c44958
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# online-rl.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/post-training-trl-fine-tuning/references/online-rl.md`
- Extract: `text`
- SHA256: `cc6d45a2879a33429e9e11d608dbead2a48224a7004fc6f1f0c9a0898b8762c6`

## Content

# Online RL Methods

Guide to online reinforcement learning with PPO, GRPO, RLOO, and OnlineDPO.

## Overview

Online RL generates completions during training and optimizes based on rewards.

## PPO (Proximal Policy Optimization)

Classic RL algorithm for LLM alignment.

### Basic Usage

```bash
python -m trl.scripts.ppo \
    --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
    --reward_model_path reward-model \
    --dataset_name trl-internal-testing/descriptiveness-sentiment-trl-style \
    --output_dir model-ppo \
    --learning_rate 3e-6 \
    --per_device_train_batch_size 64 \
    --total_episodes 10000 \
    --num_ppo_epochs 4 \
    --kl_coef 0.05
```

### Key Parameters

- `kl_coef`: KL penalty (0.05-0.2)
- `num_ppo_epochs`: Epochs per batch (2-4)
- `cliprange`: PPO clip (0.1-0.3)
- `vf_coef`: Value function coef (0.1)

## GRPO (Group Relative Policy Optimization)

Memory-efficient online RL.

### Basic Usage

```python
from trl import GRPOTrainer, GRPOConfig
from datasets import load_dataset

# Define reward function
def reward_func(completions, **kwargs):
    return [len(set(c.split())) for c in completions]

config = GRPOConfig(
    output_dir="model-grpo",
    num_generations=4,  # Completions per prompt
    max_new_tokens=128
)

trainer = GRPOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=reward_func,
    args=config,
    train_dataset=load_dataset("trl-lib/tldr", split="train")
)
trainer.train()
```

### Key Parameters

- `num_generations`: 2-8 completions
- `max_new_tokens`: 64-256
- Learning rate: 1e-5 to 1e-4

## Memory Comparison

| Method | Memory (7B) | Speed | Use Case |
|--------|-------------|-------|----------|
| PPO | 40GB | Medium | Maximum control |
| GRPO | 24GB | Fast | **Memory-constrained** |
| OnlineDPO | 28GB | Fast | No reward model |

## References

- PPO paper: https://arxiv.org/abs/1707.06347
- GRPO paper: https://arxiv.org/abs/2402.03300
- TRL docs: https://huggingface.co/docs/trl/

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
