# 2026-06-03 — Настройка автоматического сжатия контекста Hermes

## Автор
Hermes Agent (Telegram session, модель kimi-k2.6:cloud)

## Что сделано
Оптимизированы параметры автоматического сжатия контекста в `~/.hermes/config.yaml` для интенсивных сессий с тулколлами (terminal, browser, read_file, search_files).

### Изменения

| Параметр | Было | Стало |
|----------|------|-------|
| `compression.threshold` | 0.50 (~32K токенов) | **0.35 (~22K токенов)** |
| `compression.target_ratio` | 0.20 | **0.25** |
| `compression.protect_last_n` | 20 | **10** |
| `aux.compression.provider` | google (gemini-pro, без ключа) | **ollama-launch** |
| `aux.compression.model` | gemini-pro | **qwen2.5:0.5b** |
| `aux.compression.base_url` | — | **http://127.0.0.1:11434/v1** |
| `aux.compression.api_key` | — | **ollama** |

### Почему именно так

1. **threshold 0.35** — при 64K контексте (kimi-k2.6) сжатие срабатывает на ~22K вместо 32K. Это предотвращает частые 413/обрезки при интенсивных раундах тулколлов (terminal + browser + read_file накапливают быстро).

2. **target_ratio 0.25** — чуть больше хвоста сохраняется для контекста последних действий (20% → 25% от threshold = ~5.5K токенов хвоста).

3. **protect_last_n 10** — меньше сообщений защищено в хвосте. При длинных тулколлах 20 сообщений в хвосте = слишком много, 10 = оптимально для баланса между контекстом и размером.

4. **Ollama qwen2.5:0.5b для саммаризации** — была проблема: `aux.compression.provider: google` без API ключа = саммаризация падала или использовала fallback. Теперь локальная qwen2.5:0.5b на localhost:11434 — быстрая, безлимитная, не требует API ключа.

## Текущие провайдеры (Ollama localhost)
- minimax-m3:cloud
- argos-v2:latest
- argos-v1:latest
- qwen2.5:0.5b ← используется для compression
- llama3.1:8b

## Brain API состояние
- Laptop :5001 — online, 30 нод в реестре
- Только `orangepi-orangepione` online (локальный)
- Остальные 29 нод offline (argos-pc, GCP ноды, entity-* agents)
- Порты ПК Orion: :5010 brain ✓, :8000 proxy ✓, :8082 llama Vulkan0 ✓, :8083/8084 DOWN

## Связанные задачи
- [[2026-06-03]] — общий daily log
- [[WORKING]] — активные задачи
- [[STATUS]] — состояние системы

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
