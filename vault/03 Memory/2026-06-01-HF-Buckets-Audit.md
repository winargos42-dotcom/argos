# HF Buckets Audit — AvaSiG

## Ведра (Storage Buckets)

### 1. codeparrot-bucket — 46.4 GB
**Python-код из GitHub (BigQuery)**
- ~22 млн Python файлов
- 180 GB распакованный / 50 GB сжатый (в ведре 46.4 GB)
- 70% дубликатов (рекомендуется использовать `lvwerra/codeparrot-clean`)
- Формат: JSONL gzip (`file-000000000000.json.gz`, ...)
- Поля: `repo_name`, `path`, `copies`, `size`, `content`, `license`
- Источник: BigQuery `bigquery-public-data.github_repos`
- Лицензии: apache-2.0, bsd-3-clause, mit и др.
- Использование: pre-training code LLM (CodeParrot модель)

**Пример записи:**
```json
{
  "repo_name": "kmike/scikit-learn",
  "path": "sklearn/utils/__init__.py",
  "copies": 1,
  "size": 10094,
  "content": "from collections import Sequence...",
  "license": "bsd-3-clause"
}
```

### 2. UltraData-SFT-2605-bucket — 319 GB
**Supervised Fine-Tuning (SFT) датасет**
- Размер категории: 10B–100B токенов
- Конфиги: `Chinese-general`, `IF`, `Knowledge`, `Code`, `Math`, `Multi-lang-*`
- Формат: JSONL split `think` / `no_think`
- Пути: `data/think/Code/*.jsonl`, `data/no_think/Code/*.jsonl`
- Теги: code, reasoning, math, instruction-following
- Лицензия: apache-2.0

### 3. qwen3.7-max-pi-traces-bucket — 9.93 MB
**Трейсы сессий Qwen3.7-max + pi**
- Файлы: `2026-05-22T...jsonl` (timestamped)
- Размер файлов: 300–700 KB каждый
- Формат: JSONL сессии

## Выводы
- **codeparrot-bucket** = основной Python-код датасет для pre-training.
- **UltraData/Code** = SFT данные для instruction tuning с кодом.
- Оба ведра не привязаны к публичным dataset cards (только bucket storage).
- Для обучения ARGOS code-модели: взять `codeparrot-bucket` + UltraData `Code` split.

## Прямые ссылки
- codeparrot-bucket: https://huggingface.co/buckets/AvaSiG/codeparrot-bucket
- UltraData-SFT-2605-bucket: https://huggingface.co/buckets/AvaSiG/UltraData-SFT-2605-bucket
- qwen3.7 traces: https://huggingface.co/buckets/AvaSiG/qwen3.7-max-pi-traces-bucket
