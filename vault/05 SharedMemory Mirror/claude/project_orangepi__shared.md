---
argos_import: sharedmemory_mirror
source_path: claude/project_orangepi.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_orangepi.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_orangepi.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_orangepi.md`
- Category: [[Claude Hub]]

## Content

---
name: Orange Pi One — полная настройка
description: Orange Pi One на Armbian, SSH, IoT агент, Cloudflare туннель, USB устройства
type: project
---
## Состояние — ЗАПУЩЕНА ✅ (2026-05-04)

### Доступ
- SSH локально: `ssh orangepione` (192.168.2.168, ключ ava)
- SSH из интернета: `ssh orangepi-tunnel` → `ssh-orangepi.argosssss.win`
- root/ava пароль: `argos2024`

### Сеть
- LAN: 192.168.2.168/24 (DHCP от ноутбука enp0s25)
- Интернет: NAT через ноутбук (wlp3s0 → enp0s25, iptables MASQUERADE)
- **NB**: При ребуте ноутбука надо повторно: `ip addr add 192.168.2.1/24 dev enp0s25 && iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -o wlp3s0 -j MASQUERADE`

### Система
- OS: Armbian 6.12.74-current-sunxi (Ubuntu Noble), armv7l
- Board: Orange Pi One (Allwinner H3, 512MB RAM, 29G SD)
- Температура: ~59°C idle

### GPIO/I2C/UART
- Overlays: `i2c0 i2c1 spi-spidev uart1 uart2` (в /boot/armbianEnv.txt)
- `/dev/i2c-0` — доступен
- `/dev/ttyUSB0`, `/dev/ttyUSB1` — CH340 (NodeMCU v3 + CC2350)
- `/dev/ttyS0-7` — аппаратные UART
- SPI `/dev/spidev*` — после ребута

### USB устройства
- CH340 ×2: NodeMCU v3 + CC2350 Zigbee донгл
- WiFi адаптер — не определён (нужны драйвера)

### Сервисы
- `argos-iot.service` — IoT агент на :7777 (JSON статус)
- `cloudflared.service` — туннель orangepi (bf451038...), lax07/phx01

### Cloudflare
- Туннель: `orangepi` ID: `bf451038-e9d0-4a55-8bfd-95f6af283c59`
- DNS: `ssh-orangepi.argosssss.win`

**Why:** IoT шлюз ARGOS — GPIO, I2C, UART, Zigbee, NodeMCU.
**How to apply:** `curl http://192.168.2.168:7777` — статус агента. Для работы с железом — orangepi_bridge.py на OPi.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_orangepi.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
