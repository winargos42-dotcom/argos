---
argos_import: project_file
source_path: COLAB_LORA_PREP.md
source_abs: F:\debug\argoss\COLAB_LORA_PREP.md
source_ext: .md
source_sha256: d74493115caf60aad463a3745264aa6529ca5b2973a6747e704cf70b95ad8006
text_sha256: d74493115caf60aad463a3745264aa6529ca5b2973a6747e704cf70b95ad8006
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# COLAB_LORA_PREP.md

- Source: `COLAB_LORA_PREP.md`
- Extract: `text`
- SHA256: `d74493115caf60aad463a3745264aa6529ca5b2973a6747e704cf70b95ad8006`

## Content

# ARGOS Colab LoRA Prep

Актуальная схема подготовки собственной модели ARGOS в Google Colab.

## Что использовать

- Тренер: `src/argos_lora_trainer.py`
- Датасет: `data/evolver_dataset.jsonl`
- Рабочая память ARGOS: `data/memory.db`
- Рекомендуемая базовая модель по умолчанию: `Qwen/Qwen2.5-0.5B-Instruct`
- Более качественная альтернатива: `Qwen/Qwen2.5-1.5B-Instruct`

## Что уже проверено локально

- ARGOS API отвечает на `http://localhost:8001/health`
- MCP endpoint отвечает на `http://localhost:8001/mcp`
- Датасет `data/evolver_dataset.jsonl` присутствует
- Локальные venv сейчас ссылаются на отсутствующий системный Python, поэтому основной путь для fine-tuning на этой машине пока лучше считать через Colab

## Preflight перед Colab

1. Убедиться, что в `data/evolver_dataset.jsonl` нет мусорных или системных записей
2. Подготовить Hugging Face token для скачивания базовой модели
3. Выбрать профиль GPU в Colab: лучше `T4`, `L4` или выше
4. Скопировать репозиторий в `/content/argoss`

## Минимальная установка в Colab

```bash
git clone https://github.com/thoresensandmann432-source/argoss.git /content/argoss
cd /content/argoss
pip install -U pip
pip install torch transformers peft trl datasets accelerate sentencepiece gguf psutil
```

## Быстрый smoke-run в Colab

```bash
cd /content/argoss
python src/argos_lora_trainer.py --quick
```

Это прогонит короткое обучение для проверки пайплайна.

## Полу-боевой запуск

```bash
cd /content/argoss
python src/argos_lora_trainer.py --examples 500 --epochs 1.0
```

## Если нужна более сильная база

```bash
cd /content/argoss
python src/argos_lora_trainer.py --model Qwen/Qwen2.5-1.5B-Instruct --examples 500 --epochs 1.0
```

## Что получится на выходе

- LoRA adapter: `models/argos-lora-adapter`
- Merged model: `models/argos-merged`
- GGUF export: `models/argos-gguf`

## Что ещё нужно держать в голове

- Старый `argos_colab.ipynb` содержит устаревшие ссылки и смешивает `Argoss`/`SiGtRiP`
- Для обучения канонической точкой сейчас является именно `src/argos_lora_trainer.py`, а не старые bootstrap-ячейки
- После стабилизации Colab-сценария стоит собрать отдельный чистый notebook только под LoRA pipeline, без legacy launcher-логики

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
