---
argos_import: sharedmemory_mirror
source_path: shared/SHARED.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\SHARED.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: shared/SHARED.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\SHARED.md`
- Category: [[SharedMemory Hub]]

## Content

# Shared Memory — Общая память

Этот файл читают все участники: Claude Code, ARGOS, OpenCode, Ollama.

## Кто я (пользователь)
- Имя: AvA / Seva / SiG
- Проект: ARGOS — автономная AI-экосистема
- Машины: Windows PC (192.168.1.66) + Arch Linux ноутбук
- Опыт: 2 месяца кода, строит с нуля

## Активный проект
- Path (Windows): `F:\debug\argoss\`
- Path (Arch): `~/Projects/argoss/` (скопирован с ПК)
- Стек: Python, Node.js, llama.cpp Vulkan, AMD GPU x3, Telegram, P2P mesh

## MCP серверы
- ARGOS PC: `http://192.168.1.66:8000/mcp`
- ARGOS ноутбук: `http://192.168.1.53:8000/mcp` (если запущен)
- Ollama PC: `http://192.168.1.66:11434`

## Сеть
- ПК IP: 192.168.1.66
- Ноутбук IP: 192.168.1.53
- SSH ПК локально: `ssh AvA@192.168.1.66`
- SSH через интернет: `ssh argos-pc` / `ssh argos-laptop` (через cloudflared)

## GPU кластер (Windows PC)
- GPU0: RX 580 4GB → qwen2.5-3b (порт 8082)
- GPU1: Vega 11 2GB → tinyllama (порт 8083)  
- GPU2: RX 560 4GB → phi4-mini (порт 8084)
- Статус: в процессе настройки запуска

## Пути SharedMemory
- Ноутбук (Arch): `~/Documents/MyObsidianVault/SharedMemory/`
- ПК (Windows): `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\`
- Синхронизация: автоматически каждые 2 минуты через systemd (ноутбук ↔ ПК)
- Скрипт: `~/.local/bin/sync-obsidian-memory.py`

## Правила для всех агентов
- Язык: русский
- Действовать без лишних уточнений
- Писать память в свою папку `SharedMemory/[имя]/` (claude/, argos/, opencode/, ollama/)
- Читать `SharedMemory/shared/SHARED.md` при старте
- Новые агенты: создать папку `SharedMemory/[имя]/` и файл `MEMORY.md` в ней

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[SharedMemory Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `shared/SHARED.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[SharedMemory Hub]]
