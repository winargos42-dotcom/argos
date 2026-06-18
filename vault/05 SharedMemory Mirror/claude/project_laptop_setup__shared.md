---
argos_import: sharedmemory_mirror
source_path: claude/project_laptop_setup.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_laptop_setup.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_laptop_setup.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_laptop_setup.md`
- Category: [[Claude Hub]]

## Content

---
name: Настройка ноутбука Lenovo X230 (Arch Linux)
description: Статус настройки X230 — что установлено, что осталось сделать вручную
type: project
originSessionId: b5042a1a-0388-4f29-acd7-7766930d9f8e
---
## Выполнено (2026-05-02)

### Обновление системы
- `pacman -Syu` — ядро обновлено до 7.0.3-arch1-2, gcc 16, glibc 2.43, tp_smapi обновлён

### Установлены пакеты (pacman)
- `linux-headers` — для DKMS модулей
- `vulkan-intel` — Vulkan для Intel HD 4000
- `sof-firmware`, `alsa-firmware` — аудио прошивки
- `bluez`, `bluez-utils` — Bluetooth
- `pipewire-alsa`, `pipewire-pulse`, `wireplumber` — аудио (PipeWire)
- `thinkfan` 2.0.0 — управление вентилятором (AUR)
- `tlp-rdw` — TLP radio device wizard
- `smartmontools` — здоровье диска
- `fwupd` — обновление прошивок
- `brightnessctl` — яркость экрана
- `acpi`, `acpi_call` — ACPI события и управление батареей
- `i2c-tools` — датчики
- `btop` — системный монитор
- `nmap`, `ffmpeg`, `tk`, `portaudio` — для ARGOS

### TLP
- START_CHARGE_THRESH_BAT0=70 / STOP_CHARGE_THRESH_BAT0=80

### Конфиги (записаны 2026-05-02)
- `/etc/modprobe.d/thinkpad_acpi.conf` — fan_control=1 (вступит после перезагрузки)
- `/etc/thinkfan.conf` — кривая охлаждения для hwmon4

### Сервисы (включены 2026-05-02)
- `bluetooth` ✅ active
- `thinkfan` ✅ enabled (запустится после перезагрузки — нужно новое ядро)
- `fwupd-refresh.timer` ✅ enabled
- `wireplumber` ✅ active (user)
- `pipewire-pulse` ✅ active (user)
- `mkinitcpio -P` ✅ выполнен (initramfs для 7.0.3-arch1-2 готов)

### ARGOS зависимости
- Python venv: `/home/ava/Projects/argoss/.venv` (Python 3.14)
- Установлены через pip в venv: см. project_argos.md

## ⚠️ ОСТАЛОСЬ ОДНО — ПЕРЕЗАГРУЗКА
```bash
sudo reboot
```
После перезагрузки на 7.0.3-arch1-2:
- thinkfan стартует (fan_control=1 применится) — сейчас CPU 87-89°C без охлаждения
- cdc-acm.ko → /dev/ttyACM0 → Raspberry Pi Pico доступен
- ch341.ko → /dev/ttyUSB0/1 → CH340 адаптеры → UART к Orange Pi
- loop.ko → монтирование образов → прошивка SD Orange Pi
- plugdev группа и udev правило для 1f3a:efe8 уже настроены

## Железо X230
- CPU: Intel Core i5-3320M (Ivy Bridge), 4 ядра
- GPU: Intel HD Graphics 4000
- WiFi: Intel Centrino Advanced-N 6205
- Ethernet: Intel 82579LM
- Audio: Intel HDA (7 Series)

**Why:** прокачка ноутбука под ARGOS и разработку.
**How to apply:** thinkfan активируется только после перезагрузки. Всё остальное работает.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_laptop_setup.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
