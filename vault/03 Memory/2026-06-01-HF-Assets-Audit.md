# HF Assets Audit — 2026-06-01

> Автоматический аудит активов HuggingFace для ARGOS через mempalace (vertex память).

## Репозитории (User: AvaSiG)

### Модели (6)
| Модель | Pipeline | Downloads | Likes | Формат |
|--------|----------|-----------|-------|--------|
| `AvaSiG/argos-v1` | text-generation | 49 | 0 | adapter + GGUF (Q8_0) |
| `AvaSiG/argos-v1-gguf` | — | 118 | 0 | Q4_K_M.gguf |
| `AvaSiG/argos-mistral-nemo-12b` | — | 33 | 0 | adapter + Q4_K_M.gguf |
| `AvaSiG/argos-mistral-12b` | — | 7 | 0 | adapter + Q4_K_M.gguf |
| `AvaSiG/argos-mistral-nemo-12b-v100` | — | 0 | 0 | 5x safetensors (GGUF) |
| `AvaSiG/all-MiniLM-L6-v2` | sentence-similarity | 0 | 0 | ONNX + PyTorch |

### Датасеты (3)
| Датасет | Записей | Размер | Downloads | Теги |
|---------|---------|--------|-----------|------|
| `AvaSiG/argos-dataset` | ~1230 диалогов | 18.7 MB | 123 | ru, apache-2.0, argos |
| `AvaSiG/argos-quantum-train-v2` | 17,197 | 35.4 MB | 34 | ru, mit, quantum, consciousness |
| `AvaSiG/argos-canonical` | 5742 (train:5570, val:172) | — | 21 | json, 1K<n<10K |

### Spaces (2)
- `AvaSiG/Argos` — Docker Space (SDK: docker)
- `AvaSiG/sentence-transformers-all-MiniLM-L6-v2` — Space для эмбеддингов

## Локальные датасеты (~/Projects/argoss/data)
| Файл | Размер | Описание |
|------|--------|----------|
| `evolver_dataset.jsonl` | 280 MB | Evolver dataset |
| `argos_quantum_train.jsonl` | 36 MB | Quantum train |
| `argos_full_dataset.jsonl` | 7.5 MB | Full dataset |
| `argos_dal_full_dataset.jsonl` | 7.7 MB | DAL full |
| `argos_all_combined.jsonl` | 6.6 MB | Combined |
| `argos_final_train.jsonl` | 7.1 MB | Final train |
| `argos_canonical.jsonl` | 11 MB | Canonical |
| `argos_canonical_train.jsonl` | 11 MB | Canonical train |
| `argos_train_mistral.jsonl` | 1.1 MB | Mistral train |
| и др. | — | — |

## Выводы
- Основная production-модель: `argos-v1` (Qwen2.5 1.5B + LoRA/adapter).
- Самый большой локальный датасет: `evolver_dataset.jsonl` (280 MB).
- Самый популярный датасет на HF: `argos-dataset` (123 downloads).
- `argos-mistral-nemo-12b-v100` — zero downloads, требует продвижения.
- Нет spaces для инференса (только для embeddings).

## Рекомендации
1. Обновить README для `argos-mistral-nemo-12b-v100` — добавить примеры использования.
2. Создать HF Dataset Card для `argos-canonical` — сейчас описание минимальное.
3. Рассмотреть создание Inference API Space для `argos-v1`.
4. Синхронизировать локальный `evolver_dataset.jsonl` с HF (сейчас не загружен).

---
*Сгенерировано: 2026-06-01*
*Агент: Claude Code (vertex mempalace probe)*
