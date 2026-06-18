---
argos_import: project_file
source_path: config/COLAB_GUIDE.md
source_abs: F:\debug\argoss\config\COLAB_GUIDE.md
source_ext: .md
source_sha256: 73889f09c0e6907f83028f8a877ef5fedb01caaceb8ad0f5ea6e8cd2f6f62414
text_sha256: 73889f09c0e6907f83028f8a877ef5fedb01caaceb8ad0f5ea6e8cd2f6f62414
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 09:39:52
---

# COLAB_GUIDE.md

- Source: `config/COLAB_GUIDE.md`
- Extract: `text`
- SHA256: `73889f09c0e6907f83028f8a877ef5fedb01caaceb8ad0f5ea6e8cd2f6f62414`

## Content

# ARGOS Fine-Tuning — Google Colab Alternative

Если Kaggle и GCP не работают, используй Google Colab:

## Быстрый старт:

1. Открой: https://colab.research.google.com
2. File → Upload notebook → выбери `config/colab_finetune.ipynb`
3. Runtime → Change runtime type → GPU (T4)
4. Runtime → Run all

## Или создай новый notebook:

```python
# Ячейка 1: Установка
!pip install unsloth transformers datasets accelerate bitsandbytes -q

# Ячейка 2: Загрузка датасета
import json
from datasets import load_dataset

# Скачать с Kaggle (если датасет public)
!kaggle datasets download -d poldop/argos-training-dataset-v1 -p /content

# Или загрузить вручную через Files (слева)
dataset = load_dataset('json', data_files='/content/train.jsonl', split='train')

# Ячейка 3: Обучение
from unsloth import FastLanguageModel
from transformers import TrainingArguments, Trainer

model, tokenizer = FastLanguageModel.from_pretrained(
    'mistralai/Mistral-Nemo-Instruct-2407',
    max_seq_length=1024,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(model, r=8, lora_alpha=16)

# ... (стандартный код обучения)
```

## Преимущества Colab:
- Не нужна верификация телефона
- Бесплатный T4 GPU
- 12 часов сессии
- Можно скачать результат

## Недостатки:
- Может отключить GPU если долго неактивен
- Нужно держать вкладку открытой

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
