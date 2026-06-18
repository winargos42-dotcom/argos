---
argos_import: sharedmemory_mirror
source_path: claude/project_3gpu.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_3gpu.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_3gpu.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_3gpu.md`
- Category: [[Claude Hub]]

## Content

---
name: 3-GPU Setup (Windows PC)
description: Конфигурация трёх GPU для Ollama на Windows PC — маршрутизация fast/code/smart
type: project
originSessionId: 1a9b4f86-6098-48b9-b93e-c96d9d974f6d
---
## Конфигурация

| Порт | GPU | Модель | Роль | HIP_VISIBLE_DEVICES |
|------|-----|--------|------|---------------------|
| 8082 | RX 580 4GB | qwen2.5:3b | smart (основная) | 0 |
| 8083 | Vega 11 2GB | tinyllama | fast (быстрая) | 2 |
| 8084 | RX 560 4GB | qwen2.5:3b | code (кодирование) | 1 |

## Файлы (F:\debug\argoss\)
- `src/ollama_three.py` — ThreeGPUManager
- `src/ollama_autoselect.py` — автоопределение GPU
- `scripts/ollama_three_gpu.bat` — запуск 3 инстансов
- `config/gpu_ollama.json` — конфиг GPU

## Маршрутизация (_classify)
- **fast**: prompt < 30 символов или слова привет/да/нет → Vega 11
- **code**: ключевые слова (python, код, debug) → RX 560
- **smart**: остальное, prompt > 300 символов → RX 580
- Fallback: следующий GPU по order_map

**Why:** три GPU = параллельный инференс, маршрутизация по сложности запроса.
**How to apply:** при работе с Ollama на ПК учитывать, что ThreeGPUManager — первый в цепочке ai_router.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_3gpu.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
