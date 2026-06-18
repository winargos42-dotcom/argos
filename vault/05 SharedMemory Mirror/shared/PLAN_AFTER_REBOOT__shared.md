---
argos_import: sharedmemory_mirror
source_path: shared/PLAN_AFTER_REBOOT.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\PLAN_AFTER_REBOOT.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: shared/PLAN_AFTER_REBOOT.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\shared\PLAN_AFTER_REBOOT.md`
- Category: [[SharedMemory Hub]]

## Content

# План действий после перезагрузки X230
**Создан:** 2026-05-03  
**Выполнить сразу после `sudo reboot`**

---

## 1. Проверка системы (автоматически)
```bash
uname -r                    # должно быть 7.0.3-arch1-2
systemctl status thinkfan   # должен быть active (running)
systemctl status bluetooth  # active
ls /dev/ttyUSB* /dev/ttyACM*  # должны появиться CH340 и Pico
lsusb                       # все USB устройства
```

---

## 2. USB устройства — проверка и настройка

### Orange Pi One (FEL → прошивка Armbian)
```bash
# Проверить что FEL виден
sunxi-fel version
# Ожидается: AWUSBFEX soc=00001680(H3) ...

# Прошить Armbian через SD карту (если есть):
xz -dc ~/Downloads/orangepi/Armbian_26.2.1_Orangepione_noble_current_6.12.74_minimal.img.xz \
  | sudo dd of=/dev/sdX bs=4M status=progress

# ИЛИ прошить через FEL (без SD):
cd ~/Downloads/orangepi
sunxi-fel spl u-boot-sunxi-with-spl.bin
# (далее по инструкции FEL boot)
```

### Raspberry Pi Pico (RP2040)
```bash
ls /dev/ttyACM*             # должен появиться /dev/ttyACM0
# Прошить MicroPython если нужно:
# mpremote connect /dev/ttyACM0 repl
```

### CH340 UART адаптеры
```bash
ls /dev/ttyUSB*             # /dev/ttyUSB0, ttyUSB1
# Подключение к Orange Pi UART (115200):
# screen /dev/ttyUSB0 115200
# minicom -D /dev/ttyUSB0 -b 115200
```

---

## 3. ARGOS — запуск на ноутбуке
```bash
cd ~/Projects/argoss
source .venv/bin/activate
nohup python main.py --no-gui > logs/argos_laptop.log 2>&1 &
# Проверка:
curl http://127.0.0.1:8000/mcp
```

### Проверить память ARGOS
```bash
source .venv/bin/activate && python3 -c "
import sqlite3
db = sqlite3.connect('data/memory.db')
for (t,) in db.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall():
    print(t, ':', db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0])
"
# Ожидается: facts ~7916, knowledge_edges ~15143
```

---

## 4. SharedMemory — синхронизация
```bash
python3 ~/.local/bin/sync-obsidian-memory.py
# Проверить таймер:
systemctl --user status sync-obsidian-memory.timer
```

---

## 5. Orange Pi One — настройка после прошивки
```bash
# После загрузки Armbian найти IP:
nmap -sn 192.168.1.0/24 | grep -A1 "OrangePi\|Allwinner"

# Подключиться:
ssh root@<ip>   # пароль: 1234 (первый вход — сменить!)

# Установить Python + ARGOS агент:
apt update && apt install -y python3 python3-pip git
pip3 install aiohttp requests python-dotenv

# Скопировать агент с ноутбука:
scp -r ~/Projects/argoss/src/connectivity/orangepi_bridge.py root@<ip>:~/
```

---

## 6. Cloudflare SSH (опционально)
```bash
cloudflared access login ssh-pc.argosssss.win
# После логина через браузер:
ssh argos-pc   # подключение к ПК через интернет
```

---

## 7. Проверка thinkfan
```bash
systemctl status thinkfan
cat /proc/acpi/ibm/fan    # должен показать уровень вентилятора
sensors                   # температуры
```

---

## Контрольный список ✅

- [ ] `uname -r` → 7.0.3-arch1-2
- [ ] thinkfan активен
- [ ] `/dev/ttyUSB0`, `/dev/ttyUSB1` появились
- [ ] `/dev/ttyACM0` появился (Pico)
- [ ] `sunxi-fel version` → H3 определён
- [ ] ARGOS запущен, MCP отвечает
- [ ] Память: 7916 фактов, 15143 рёбра
- [ ] SharedMemory синхронизирован с ПК
- [ ] Orange Pi прошит (если SD карта есть)

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[SharedMemory Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `shared/PLAN_AFTER_REBOOT.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[SharedMemory Hub]]
