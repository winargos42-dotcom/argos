---
argos_import: sharedmemory_mirror
source_path: claude/project_homeassistant.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_homeassistant.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_homeassistant.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_homeassistant.md`
- Category: [[Claude Hub]]

## Content

---
name: Установка Home Assistant
description: Контекст установки Home Assistant Container на X230 (Arch Linux) — прервана из-за ядра, ждёт перезагрузки
type: project
originSessionId: f0e9ecac-e2f3-4284-a912-79646f263ea0
---
## Статус: ждёт перезагрузки (2026-05-03)

Установка прервана: Docker не запускается из-за несоответствия ядра.
- Запущено: `7.0.3-arch1-1`
- Модули: `7.0.3-arch1-2`
- Решение: перезагрузиться, потом продолжить.

## Что уже сделано

- `/etc/docker/daemon.json` создан:
  ```json
  { "iptables": true, "ip6tables": false }
  ```
- `/usr/local/bin/iptables` → симлинк на `iptables-legacy` (nftables не работает в этом окружении)
- `/usr/local/bin/iptables-restore` → симлинк на `iptables-legacy-restore`

## После перезагрузки — выполнить

```bash
systemctl start docker
systemctl enable docker

mkdir -p /home/ava/homeassistant

docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Europe/Moscow \
  -v /home/ava/homeassistant:/config \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
```

Веб-интерфейс: `http://localhost:8123`

## Выбранный метод
Home Assistant Container (Docker) — рекомендованный способ на Arch Linux без выделенного железа.

**Why:** пользователь попросил установить Home Assistant, Docker уже установлен (v29.4.1).
**How to apply:** после перезагрузки сразу выполнить команды выше без лишних вопросов.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_homeassistant.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
