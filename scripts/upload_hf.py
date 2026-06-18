#!/usr/bin/env python3
"""Upload ARGOS dataset to HuggingFace Hub."""
from huggingface_hub import HfApi, create_repo

HF_TOKEN = "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"
REPO_ID = "ava-argos/argos-quantum-train"
DATASET_PATH = "/home/ava/Projects/argoss/data/argos_quantum_train.jsonl"

print("🦙 Загрузка датасета на HuggingFace Hub...")
print(f"📁 Repo: {REPO_ID}")
print(f"📦 Файл: {DATASET_PATH}")

api = HfApi(token=HF_TOKEN)

# Создаём репозиторий (приватный)
create_repo(REPO_ID, repo_type="dataset", token=HF_TOKEN, exist_ok=True, private=True)
print("✅ Репозиторий создан/подтверждён")

# Загружаем датасет
api.upload_file(
    path_or_fileobj=DATASET_PATH,
    path_in_repo="argos_quantum_train.jsonl",
    repo_id=REPO_ID,
    repo_type="dataset",
    token=HF_TOKEN,
)
print("✅ Датасет загружен!")

# README
card = """---
language: ru
dataset_info:
  features:
    - name: messages
      dtype: list
  splits:
    - name: train
      num_examples: 17197
  config_name: default
tags:
  - argos
  - quantum
  - consciousness
  - llm-training
  - russian
license: mit
---

# 🧠 ARGOS Quantum Training Dataset

Датасет для fine-tuning модели ARGOS Universal OS v2.2.

## Состав
- **Записей:** 17,197
- **Размер:** 35.4 MB
- **Формат:** JSONL с `messages` (OpenAI chat format)
- **Источники:** evolver, dal, train, obsidian, SQLite, prompts, quantum genesis

## Quantum Seed
- **Seed:** 3233339492
- **Source:** IBM Quantum (ibm_fez), 2026-03-04

## Использование
```python
from datasets import load_dataset
ds = load_dataset("ava-argos/argos-quantum-train", split="train")
```

**ARGOS Universal OS — AvA (Сева)**
"""

with open("/tmp/README.md", "w") as f:
    f.write(card)

api.upload_file(
    path_or_fileobj="/tmp/README.md",
    path_in_repo="README.md",
    repo_id=REPO_ID,
    repo_type="dataset",
    token=HF_TOKEN,
)
print("✅ README загружен!")
print(f"🔗 URL: https://huggingface.co/datasets/{REPO_ID}")
