---
argos_import: sharedmemory_mirror
source_path: shared/ARGOS_LINKS.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\ARGOS_LINKS.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: shared/ARGOS_LINKS.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\ARGOS_LINKS.md`
- Category: [[SharedMemory Hub]]

## Content

# ARGOS — Карта связей (Hub файл)

## Центральные узлы

### Ноутбук X230
- \[\[project_laptop_setup\]\] — настройка X230, Arch Linux
- \[\[project_argos_laptop\]\] — ARGOS на ноутбуке
- \[\[project_obsidian\]\] — синхронизация Obsidian
- \[\[project_mcp\]\] — MCP серверы

### ПК Windows
- \[\[project_argos\]\] — основной проект F:\debug\argoss
- \[\[project_3gpu\]\] — 3 GPU: RX580/Vega11/RX560
- \[\[project_argos_training\]\] — обучение модели (A100 → V100)

### Orange Pi One
- \[\[project_orangepi\]\] — Armbian, IoT агент, Cloudflare туннель

### Устройства IoT
- ESP32-2432S024: 192.168.1.211 (ILI9341 дисплей, temp сенсор)
- ESP8266 NodeMCU: 192.168.1.181 (OLED, WiFi мост)
- Pico RP2040: /dev/ttyACM0 (MicroPython)
- XGecu T48: USB программатор

## Cloudflare туннели
| Хост | Назначение |
|------|-----------|
| ssh-laptop.argosssss.win | SSH ноутбук |
| ssh-pc.argosssss.win | SSH ПК |
| ssh-orangepi.argosssss.win | SSH Orange Pi |
| mcp.argosssss.win | ARGOS MCP ПК |
| api.argosssss.win | ARGOS API ПК |
| myollama123.ngrok.io | Ollama ПК (ngrok) |

## Ollama модели (ПК)
- ds-coder-v2, deepseek-v2:16b, qwen2.5:3b, llama3.2
- Доступ: ngrok или SSH туннель localhost:12434

## Обучение модели
- Dataset: AvaSiG/argos-dataset (HF)
- Colab: ARGOS_A100_Train_Final.ipynb
- Выход: AvaSiG/argos-mistral-12b → GGUF Q4_K_M
- Для V100: ollama create argos-v2 -f Modelfile

## Сеть
- ПК: 192.168.1.66
- Ноутбук: 192.168.1.53
- Orange Pi: 192.168.2.168 (LAN через ноутбук)
- ESP32: 192.168.1.211
- ESP8266: 192.168.1.181

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[SharedMemory Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `shared/ARGOS_LINKS.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[SharedMemory Hub]]
