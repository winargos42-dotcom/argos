---
type: server-config
tags: [server, argos, infrastructure, gpu]
updated: 2026-05-14
---

# 🖥️ SERVER — ПК Конфигурация

> **ПК = Сервер** | IP: `192.168.1.66` | User: `AvA` | Роль: **GPU-сервер + Ollama кластер**

## Характеристики сервера

| Компонент | Значение |
|-----------|----------|
| **ОС** | Windows |
| **IP** | 192.168.1.66 |
| **SSH** | `AvA@192.168.1.66` |
| **Ключ** | `/home/ava/.ssh/id_ed25519` |
| **ARGOS Vault** | `F:\debug\аргос\` |
| **SharedMemory** | `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\` |
| **GPU** | Radeon RX 580 + RX 560 |

## P2P Сеть

| Узел | Адрес | Роль | Модели Ollama |
|------|-------|------|---------------|
| argos-pc | 192.168.1.66:5010 | 🖥️ Сервер, GPU, Brain | tinyllama, phi4-mini, qwen2.5:3b, ds-coder-v2, qwen2.5-coder:7b, mistral-nemo, llama3.2:1b, **qwen2.5:7b**, **argos-v1** |
| argos-laptop | 192.168.1.53:8000 | 💻 Compute, AI, MCP | argos-v1, qwen2.5:0.5b, llama3.1:8b |
| orangepi-one | 192.168.2.168:7777 | 🍊 IoT, GPIO, Sensors | — (gpio, i2c, uart, spi, relay, modbus, 1wire, rs485) |

## Сервисы на сервере

| Сервис | Порт | Статус |
|--------|------|--------|
| Ollama (GPU кластер) | :11434 | ✅ 9 моделей |
| Brain API | :5010 | ✅ online |
| argos-brain (Docker) | — | ✅ healthy |
| argos-compute (Docker) | — | ✅ healthy |
| argos-redis (Docker) | — | ✅ running |

## Сервисы на ноутбуке

| Сервис | Порт | Статус |
|--------|------|--------|
| Brain API | :5001 | ✅ |
| MCP API | :8000 | ✅ |
| Telegram Bot | — | ✅ @Argosssbot |
| Agent Bus (MQTT) | :1883 | ✅ |
| Autonomous Brain | — | ✅ 10-мин цикл |
| Home Assistant | :8123 | ✅ 91 entities, 61 active |
| HA Metrics Pusher | — | ✅ 60 сек |
| Ollama | :11434 | ✅ llama3.1:8b, qwen2.5:0.5b |
| OPi IoT Agent | 192.168.2.168:7777 | ✅ v2.1 |
| ArgosEvolution | — | ✅ v2.0 |

## Синхронизация

| Скрипт | Интервал | Направление |
|--------|----------|-------------|
| `sync-obsidian-memory.py` | 2 мин | ↔ Двусторонняя |
| `vault-sync.sh` | 5 мин | → Однонаправленная |

---

*Это заметка сервера. ПК является главным GPU-сервером ARGOS.*
