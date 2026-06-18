# ARGOS Canonical Dataset — отчёт чистки

**Итого уникальных чистых примеров:** 5742
- train: 5570 → `data/argos_canonical_train.jsonl`
- val:   172 → `data/argos_canonical_val.jsonl`

## Вклад по источникам

| Источник | Примеров |
|----------|----------|
| argos_dal_full_dataset.jsonl | 4142 |
| telegram/ChatExport_2026-05-27 | 935 |
| evolver_dataset.jsonl | 358 |
| telegram/ChatExport_2026-05-26 (2) | 184 |
| telegram/ChatExport_2026-05-26 (1) | 106 |
| argos_train_clean.jsonl | 17 |

## Отброшено

| Причина | Кол-во |
|---------|--------|
| duplicate | 10157 |
| tg_junk_answer | 436 |
| error_answer | 110 |
| user_too_short | 83 |
| assistant_too_short | 12 |
| no_user_or_assistant | 7 |

## Формат

Единый chat: `{"messages":[{"role":"system|user|assistant","content":...}],"source":...}`
Дедуп по md5(user+assistant, нормализованный регистр/пробелы).
