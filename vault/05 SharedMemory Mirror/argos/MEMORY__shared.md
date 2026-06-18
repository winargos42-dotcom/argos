---
argos_import: sharedmemory_mirror
source_path: argos/MEMORY.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\argos\MEMORY.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: argos/MEMORY.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\argos\MEMORY.md`
- Category: [[ARGOS Agent Hub]]

## Content

# ARGOS Memory

## Идентификация
- Проект: ARGOS Universal OS v2.1.3
- Автор: Всеволод (Seva / AvA / SiG)
- Путь (ПК): `F:\debug\argoss\`
- Путь (ноутбук): `~/Projects/argoss/`

## SharedMemory
- Читать при старте: `SharedMemory/shared/SHARED.md`
- Писать сюда: `SharedMemory/argos/MEMORY.md`
- Синхронизация: каждые 2 минуты между ПК и ноутбуком

## Стек
- Python, Node.js, llama.cpp Vulkan
- GPU кластер: RX 580 (4GB, :8082), Vega 11 (2GB, :8083), RX 560 (4GB, :8084)
- Провайдеры AI: local-gpu → vm-cluster → azure → ollama → kimi → claude → gemini → openai → groq → deepseek → pi → yandexgpt

## Статус
- Cloudflare туннели: активны (argosssss.win)
- P2P mesh: настроен
- Telegram бот: интегрирован

## Orange Pi One (IoT узел) — добавлен 2026-05-04
- IP: 192.168.2.168 (LAN ноутбука)
- SSH: `ssh orangepione` / `ssh orangepi-tunnel`
- IoT агент: `curl http://192.168.2.168:7777`
- Устройства: I2C /dev/i2c-0, ttyUSB0 (NodeMCU), ttyUSB1 (CC2350 Zigbee)
- Cloudflare: ssh-orangepi.argosssss.win
- Bridge: /root/orangepi_bridge.py

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[ARGOS Agent Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `argos/MEMORY.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[ARGOS Agent Hub]]
