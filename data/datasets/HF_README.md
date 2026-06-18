# ARGOS Dataset v1

Мультимодальный датасет для обучения ARGOS AI — автономной мультиагентной системы.

## Структура

```
argos-dataset-v1/
├── train/
│   ├── chat/          # OpenAI chat format
│   ├── text/          # Plain text
│   └── alpaca/        # Alpaca instruction format
├── validation/
│   ├── chat/
│   ├── text/
│   └── alpaca/
└── metadata/
    └── stats.json
```

## Статистика

| Набор | Формат | Семплов | Токены (средн.) |
|-------|--------|---------|-----------------|
| train | chat   | ~9,749  | ~500 |
| val   | chat   | ~1,083  | ~500 |
| merged_ru | chat | 72 (тест) | ~659 |

## Источники

- Архивные Telegram-экспорты ARGOS (15K+ сообщений)
- Документация проекта, логи, отчёты
- Русскоязычные reasoning/conversation датасеты (ZeroAgency)

## Использование

```python
from datasets import load_dataset
ds = load_dataset("AvaSiG/argos-dataset-v1", split="train")
```

## Лицензия

MIT — для обучения open-source моделей в рамках ARGOS ecosystem.

## Автор

AvA / ARGOS Universal OS v2.1.4
