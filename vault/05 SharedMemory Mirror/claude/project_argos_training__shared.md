---
argos_import: sharedmemory_mirror
source_path: claude/project_argos_training.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos_training.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_argos_training.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos_training.md`
- Category: [[Claude Hub]]

## Content

---
name: ARGOS LoRA обучение — v2 для V100
description: Датасет v2 загружен на HF, Colab для Mistral NeMo 12B готов
type: project
---
## Статус (2026-05-08)

| Задача | Статус |
|--------|--------|
| Датасет v1 (1230 прим.) | ✅ был |
| Датасет v2 (940 уникал. + 145 синтетич.) | ✅ загружен |
| argos_train_v2.jsonl | ✅ HF |
| argos_val_v2.jsonl | ✅ HF |
| Colab MistralNeMo12B | ✅ создан |
| Текущий прогон | A100 (Mistral NeMo 12B, Colab) |

## HuggingFace
- Dataset: `AvaSiG/argos-dataset` (приватный)
- Токен: `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` (актуальный на 2026-05-08)
- Файлы: argos_train_v2.jsonl (940), argos_val_v2.jsonl (50)
- Формат: messages [{role,content}] ChatML

## Colab
- Старый: `colab/ARGOS_Train_Colab.ipynb` (Qwen2.5-7B, T4)
- Новый: `colab/ARGOS_Train_MistralNeMo12B.ipynb` (Mistral NeMo 12B, V100/A100)
- HF_TOKEN secret в Colab обновить на: `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`

## После обучения
```bash
ollama create argos-v2 -f Modelfile
# В .env: OLLAMA_MODEL=argos-v2
```

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_argos_training.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
