---
argos_import: sharedmemory_mirror
source_path: shared/REMOTE-ACCESS.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\REMOTE-ACCESS.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: shared/REMOTE-ACCESS.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\REMOTE-ACCESS.md`
- Category: [[SharedMemory Hub]]

## Content

# Удалённый доступ через Cloudflare Tunnel

## Подключение к Windows PC из интернета

```bash
# Настроить ~/.ssh/config (один раз):
Host argos-pc
  HostName ssh-pc.argosssss.win
  User AvA
  ProxyCommand cloudflared access ssh --hostname %h

# Подключиться:
ssh argos-pc
```

## Подключение к Arch ноутбуку из интернета

```bash
Host argos-laptop
  HostName ssh-laptop.argosssss.win
  User ava
  ProxyCommand cloudflared access ssh --hostname %h

ssh argos-laptop
```

## Статус туннелей

| Хост | Машина | Сервис |
|------|--------|--------|
| ssh-pc.argosssss.win | Windows PC | SSH :22 |
| ssh-laptop.argosssss.win | Arch ноутбук | SSH :22 |
| api.argosssss.win | Windows PC | ARGOS API :5010 |
| app.argosssss.win | Windows PC | Dashboard :8081 |
| argosssss.win | Windows PC | Dashboard :8081 |

## Проверка статуса

```bash
# Ноутбук:
systemctl --user status cloudflared

# ПК (через SSH):
ssh AvA@192.168.1.66 'powershell -Command "(Get-Service cloudflared).Status"'
```

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[SharedMemory Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `shared/REMOTE-ACCESS.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[SharedMemory Hub]]
