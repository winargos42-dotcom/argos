---
argos_import: sharedmemory_mirror
source_path: claude/project_pending_tasks.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_pending_tasks.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_pending_tasks.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_pending_tasks.md`
- Category: [[Claude Hub]]

## Content

---
name: Незавершённые задачи (ноутбук)
description: Что нужно сделать после перезагрузки ноутбука X230 — полный чеклист
type: project
originSessionId: 5ed653bc-fa99-4e63-8c6d-8622bd52d48d
---
## Статус на 2026-05-03

Детальный план также в SharedMemory: `shared/PLAN_AFTER_REBOOT.md`

Всё ниже ждёт **перезагрузки ноутбука** (`sudo reboot`).

---

## ▶ СРАЗУ ПОСЛЕ ПЕРЕЗАГРУЗКИ

### 1. thinkfan
```bash
systemctl status thinkfan
```
Должен быть active. Если нет — `journalctl -u thinkfan -n 30`.

### 2. ARGOS — запустить brain + web_server
Эти процессы запущены вручную, сервиса нет — после ребута нужно стартовать руками:
```bash
cd /home/ava/Projects/argoss
source .venv/bin/activate
nohup python argos_brain_api.py > logs/brain.log 2>&1 &
nohup python web_server.py > logs/web.log 2>&1 &
```
Или через main.py:
```bash
python main.py --no-gui --dashboard
```

### 3. ARGOS P2P — проверить heartbeat
systemd сервис `argos-p2p-agent` включён и запустится автоматически.
Но brain должен быть запущен ДО него (шаг 2).
```bash
systemctl --user status argos-p2p-agent
curl -s http://127.0.0.1:5001/brain/nodes
```
Ожидаемый результат: `online=2/2`.

### 4. autoMemoryDirectory — симлинк
Симлинк `/root/Documents/MyObsidianVault/SharedMemory/claude` должен выжить ребут.
Если Claude Code снова показывает `/doctor` — пересоздать:
```bash
mkdir -p /root/Documents/MyObsidianVault/SharedMemory
ln -sfn /home/ava/Documents/MyObsidianVault/SharedMemory/claude /root/Documents/MyObsidianVault/SharedMemory/claude
```

---

## ⏳ ОТЛОЖЕННЫЕ ЗАДАЧИ (в порядке приоритета)

### 5. Home Assistant
Docker настроен, команды готовы:
```bash
systemctl start docker && systemctl enable docker
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
Открыть: `http://localhost:8123`

### 6. Orange Pi One — прошивка Armbian
FEL работает (1f3a:efe8), plugdev + udev настроены. После ребута:
```bash
lsusb | grep 1f3a       # убедиться что виден
sunxi-fel ver           # проверить FEL
```
Детали: `project_orangepi.md`

### 7. ARGOS — тестирование навыков
```bash
cd /home/ava/Projects/argoss && source .venv/bin/activate
python health_check.py
python test_all_skills.py
```

---

**Why:** ноутбук долго не перезагружался — накопились отложенные задачи.
**How to apply:** после ребута выполнять в порядке 1→2→3→4, остальное — по желанию.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_pending_tasks.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
