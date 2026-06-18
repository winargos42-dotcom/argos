# ARGOS Unified State 2026-05-04

Обновлено: `2026-05-04 17:50`
Оператор: `Всеволод (Seva / AvA / SiG)`
Режим: `production`

## Канонические точки

- Проект: `F:\debug\argoss`
- Vault: `F:\debug\аргос`
- SharedMemory: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory`
- Рабочая память ARGOS DB: `F:\debug\argoss\data\memory.db`
- MCP endpoint: `http://127.0.0.1:8000/mcp`

## Текущее положение дел

- ARGOS v2.1.3, MCP :8000 -- РАБОТАЕТ
- Навыки: 50 загружено (48 src/skills + 8 manifest)
- AI-провайдеры: DeepSeek, Gemini (6 ключей), Grok, Kimi, Ollama
- Эволюция: приоритет evolution, 10 принятых циклов
- Память: 6172 факта, 603 заметки, 9798 рёбер знаний
- Датасет: 3619 записей raw, 2128 clean
- MCP: 18 tools OK, 15+ fast-path команд
- Obsidian: vault F:\debug\аргос, 100+ заметок, зеркало 5364 файла

## 3x GPU (llama-server Vulkan) -- НАСТРОЕН

| Порт | GPU | Vulkan | VRAM | Модель | Роль | tok/s |
|------|-----|--------|------|--------|------|-------|
| 8082 | RX 580 | Vulkan0 | 4GB | qwen2.5:3b | smart | 21.8 |
| 8083 | Vega 11 | Vulkan2 | 25GB | tinyllama | fast | 26.7 |
| 8084 | RX 560 | Vulkan1 | 4GB | qwen2.5:3b | code | 14.5 |

- Backend: llama-server (Vulkan), NOT Ollama HIP
- ВАЖНО: перед стартом чистить VRAM (убить ollama + llama-server)
- Скрипт: `scripts/three_gpu_start.ps1`
- MCP tool: `gpu_status` (status/start/stop/benchmark)
- Ollama :11434 убивается при старте GPU (освобождение VRAM)

## Colab Training -- ГОТОВО К ЗАПУСКУ

- HF: AvaSiG/argos-dataset (private), 2128 примеров
- Notebook: colab/ARGOS_Train_Colab.ipynb
- Два пути: canonical (0.5B/1.5B) + Unsloth (7B)
- HF токен: OK (write)

## Изменения за сегодня

- [02:15-02:32] MCP тесты, IoT bugfix, Colab prep
- [03:26-03:38] Эволюция ускорена, env-fix cloudflare/image
- [03:51-04:48] Obsidian MCP tools, project mirror (5363 docs), ARGOSS MCP tools
- [11:18-11:20] Полный MCP аудит: 15/15 tools, 11/11 fast-path
- [11:25-11:50] 3x GPU настроен: Vulkan mapping исправлен, ollama_three.py v3, clean_vram
- [11:40-11:41] Memory web объединена, SharedMemory зеркалирована

## Известные риски

- CPU ~100% при тяжёлых прогонах
- RX 580 VRAM = 4GB, требует очистки перед стартом
- SHARED.md перезаписывается sync с ноутбука каждые 2 мин
- Upstream image backend может отвечать ошибкой (внешний фактор)

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
