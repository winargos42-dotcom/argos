---
argos_import: sharedmemory_mirror
source_path: claude/project_roadmap.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_roadmap.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_roadmap.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_roadmap.md`
- Category: [[Claude Hub]]

## Content

---
name: Дорожная карта ARGOS и системы
description: Поэтапный план развития ARGOS + инфраструктуры + железа на 2026 год
type: project
originSessionId: f0e9ecac-e2f3-4284-a912-79646f263ea0
---
## Точка отсчёта (2026-05-03)

**Железо:** X230 ноутбук (i5-3320M) + ПК (Ryzen 5 3350G, 48GB, RX580+RX560+Vega11)
**ARGOS:** v2.1.4, 5 Azure нод (2 offline), 10+ AI провайдеров
**Проблемы:** галлюцинации навыков, ANTHROPIC_API_KEY пустой, 2 ноды offline, Docker на ноутбуке не запущен

---

## Фаза 0 — Прямо сейчас (до перезагрузки ноутбука)

- [ ] Перезагрузить ноутбук → ядро 7.0.3-arch1-2, thinkfan, Docker

---

## Фаза 1 — Стабилизация (май 2026, после перезагрузки)

### Ноутбук
- [ ] Запустить Home Assistant Container (Docker, :8123)
- [ ] Прошить Orange Pi One → Armbian (sunxi-tools, USB FEL mode)
- [ ] Протестировать все навыки ARGOS на ноутбуке (`python test_all_skills.py`)

### ПК — ARGOS критические фиксы
- [ ] Добавить `ANTHROPIC_API_KEY` в .env → включить Claude как провайдера
- [ ] Починить SE VM WireGuard (`wg/setup_se_wg.sh`)
- [ ] Запустить AU VM (deallocated)
- [ ] Пополнить xAI кредиты → включить Grok

### ARGOS архитектура (борьба с галлюцинациями)
- [ ] Расширить `_DIRECT_PREFIXES` и `_is_raw_shell` в `core.py`
- [ ] Добавить тест-сьют: "эта команда должна выполниться реально, не LLM"
- [ ] Каждый навык — `assert` что результат содержит реальные данные (не шаблон LLM)

---

## Фаза 2 — Развитие (май–июнь 2026)

### Home Assistant интеграция с ARGOS
- [ ] ARGOS skill `smart_environments` → управление HA через REST API
- [ ] HA автоматизации через ARGOS Telegram бот
- [ ] Orange Pi One → GPIO сенсоры → HA → ARGOS

### ARGOS новые навыки
- [ ] `v100_monitor` — мониторинг температуры/загрузки V100 (заготовить заранее)
- [ ] `image_gen` — доделать ComfyUI интеграцию (`setup_comfyui.ps1`)
- [ ] `obsidian_skill` — синхронизация заметок через ARGOS
- [ ] Скачать image models (`scripts/download_image_models.py`)

### Инфраструктура
- [ ] Настроить мониторинг всех 5 Azure нод в Dashboard
- [ ] Автоперезапуск deallocated нод через ARGOS scheduler
- [ ] Cloudflare туннель для HA: `ha.argosssss.win → :8123`

---

## Фаза 3 — Подготовка к V100 (до ~2026-06-03)

### ПК физически
- [ ] Переставить RX 580 из PCIEX16_1 в PCIEX16_3 (x4)
- [ ] Освободить PCIEX16_1 (x8) для V100
- [ ] Проверить 8-pin PCIe кабель от БП (1000W — достаточно)

### Программная подготовка
- [ ] Установить NVIDIA драйвер (Data Center edition) на Windows
- [ ] Установить CUDA Toolkit 12.x
- [ ] Подготовить `argoss/config/gpu_v100.yaml` — конфиг нового GPU
- [ ] Обновить AI failover: `local-gpu-cuda (V100)` → приоритет выше AMD

### Модели под V100 (16GB VRAM)
- [ ] Скачать Mistral 7B / LLaMA 3 8B в FP16 (умещаются в 16GB)
- [ ] Попробовать LLaMA 3 70B Q4 (~35GB) — не влезет, нужен offload
- [ ] Скачать SDXL для image gen (6GB VRAM, остаток на LLM)

---

## Фаза 4 — После V100 (июнь 2026+)

### GPU кластер с V100 как мастером
- [ ] V100 (CUDA, :8082) → основной inference провайдер
- [ ] RX 580 (ROCm) → второй GPU для параллельных задач
- [ ] RX 560 + Vega 11 → мелкие задачи / резерв
- [ ] Общий VRAM кластера: 16 + 4 + 4 + 2 = **26 GB**

### ARGOS v3.0 цели
- [ ] Полноценный CUDA inference без offload до 13B FP16
- [ ] LoRA дообучение на V100 (скрипты уже есть: `train_argos_lora.bat`)
- [ ] Мультимодальность: vision + image gen + audio в одном пайплайне
- [ ] ARC-AGI: автономный агент решает задачи без подсказок (2000 задач скачаны)
- [ ] Quantum: qiskit задачи через IBM Runtime

### IoT экосистема
- [ ] Orange Pi One → MQTT брокер → Home Assistant → ARGOS
- [ ] ESP32 устройства через ARGOS `esp32_usb_bridge`
- [ ] Умный дом: автоматизации на базе ARGOS AI решений

---

## KPI / Метрики успеха

| Метрика | Сейчас | Цель |
|---------|--------|------|
| Навыки без галлюцинаций | ~11/30 | 25/30 |
| VRAM локальный | 10 GB (3 GPU AMD) | 26 GB (+V100) |
| Inference скорость 7B | ~8 tok/s | ~50 tok/s (V100) |
| Онлайн провайдеры | 8/11 | 11/11 |
| Azure ноды online | 3/5 | 5/5 |
| Home Assistant | ❌ | ✅ |
| Orange Pi | ❌ | ✅ |

**Why:** системный план нужен чтобы двигаться последовательно, не перепрыгивая задачи.
**How to apply:** в начале каждой сессии — сверяться с фазой и не браться за Фазу 3 пока не закрыта Фаза 1.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_roadmap.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
