# 2026-05-06 — План дообучения ARGOS (Obsidian -> A100 -> V100)

## Источники
- [[2026-05-06-Ava-Vertex-Finetune-Thread]]
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://github.com/AlexsJones/llmfit

## Цель
Собрать качественный датасет из Obsidian, обучить модель на облачной A100 (через бонусы), затем запустить локально на V100 в GGUF.

## Pipeline
1. Экспорт заметок из Obsidian в сырой корпус (md/txt/doc).
2. Очистка: дубли, мусор, пустые TODO, служебные ссылки.
3. Преобразование в JSONL instruction/context/response.
4. Train на Vertex AI (предпочтительно Custom Job + автоостановка).
5. Квантование и экспорт GGUF (q4/q6).
6. Локальный runtime на V100 через llama.cpp / Ollama.

## Экономия
- Использовать Custom Job вместо постоянно включенного Notebook.
- Включать idle shutdown.
- Удалять временные диски/ресурсы сразу после job.

## Риски и контроль качества
- Риск: галлюцинации при плохой структуре train данных.
- Контроль: валидационный set + вопросы по фактам из Obsidian.
- Проверка: воспроизводимость ответов и корректные цитаты контекста.

## Блокеры
- Квота A100 (через IAM & Admin > Quotas).
- Проверка зависимостей/скриптов подготовки JSONL.

## Следующий практический шаг
Запустить автоматический rebuild датасета из Obsidian и сохранить train bundle для Colab/Vertex.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
