---
argos_import: sharedmemory_mirror
source_path: claude/project_p2p.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_p2p.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_p2p.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_p2p.md`
- Category: [[Claude Hub]]

## Content

---
name: ARGOS P2P сеть
description: P2P mesh между ПК и ноутбуком — brain, узлы, heartbeat сервисы, MCP endpoints
type: project
originSessionId: 5ed653bc-fa99-4e63-8c6d-8622bd52d48d
---
## Архитектура (настроено 2026-05-03)

**Brain:** ноутбук `127.0.0.1:5001` (argos_brain_api.py, слушает 0.0.0.0:5001)
- API: `/brain/nodes`, `/brain/register`, `/brain/heartbeat`, `/p2p/status`

## Узлы

| node_id | address | capabilities | статус |
|---------|---------|--------------|--------|
| argos-laptop | 192.168.1.53:8000 | p2p, mcp, compute, ai | online |
| argos-pc | 192.168.1.66:8000 | p2p, mcp, compute, gpu, ai | online |

## Heartbeat сервисы

**Ноутбук** — systemd user service:
- Файл: `~/.config/systemd/user/argos-p2p-agent.service`
- ARGOS_BRAIN_URL=http://127.0.0.1:5001
- Автозапуск: enabled, каждые 30s

**ПК (Windows)** — Task Scheduler:
- Задача: `ARGOS-P2P-Agent`
- Скрипт: `F:\debug\argoss\start_p2p_agent.ps1`
- ARGOS_BRAIN_URL=http://192.168.1.53:5001
- Автозапуск: AtLogOn, restart x3

## MCP cross-node

- Ноутбук → ПК: `http://192.168.1.66:8000/mcp`
- ПК → ноутбук: `http://192.168.1.53:8000/mcp`

## SSH к ПК (с ноутбука)

```bash
ssh -i /home/ava/.ssh/id_ed25519 AvA@192.168.1.66   # локально
ssh argos-pc                                          # через Cloudflare
```

**Why:** единая P2P сеть ARGOS-узлов с автоматической регистрацией и heartbeat.
**How to apply:** brain живёт на ноутбуке; при проблемах с ПК — проверить Task Scheduler "ARGOS-P2P-Agent" и BRAIN_URL=192.168.1.53:5001.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_p2p.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
