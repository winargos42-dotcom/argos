# 2026-05-14 KolibriOS + ColibriAsmEngine — Full Integration

## 🐦 KolibriOS (ОС на ассемблере)

**QEMU i386 в Termux**
- Образ: `~/argos-kolibri/images/kolibri.img` (~10MB)
- Эмуляция: `qemu-system-i386 -m 256 -fda kolibri.img -vnc :1`
- Сеть: NAT + hostfwd TCP :8080→:80
- VNC дисплей: `localhost:5901`

**System wrapper:** `/system/xbin/argos-colibri`

**Команды:**
```bash
# System level (root)
argos-colibri status         # статус образа/QEMU/CLI
argos-colibri start          # запуск KolibriOS
argos-colibri stop           # остановка KolibriOS

# Termux
kolibri-os                   # запуск
kolibri-stop                 # остановка
```

---

## ⚙️ ColibriAsmEngine (Ассемблер/Дизассемблер)

**Python CLI:** `~/argos-kolibri/colibri/colibri_cli.py`

### Архитектуры
| Архитектура | Keystone | Capstone | Применение |
|-------------|----------|----------|------------|
| x86         | ✅       | ✅       | ПК/legacy |
| x86_64      | ✅       | ✅       | ПК/серверы |
| arm         | ✅       | ✅       | ARMv7 |
| arm_thumb   | ✅       | ✅       | Cortex-M, nRF52, RP2040 |
| arm64       | ✅       | ✅       | ESP32-S3, RPi |
| avr         | ✅       | ⚠️       | Arduino ATmega |
| mips        | ✅       | ✅       | Embedded/роутеры |

### Команды

#### 1. Ассемблирование
```bash
colibri asm "mov eax, 1" --arch x86
colibri asm "[x86] nop"
colibri asm "[arm_thumb] mov r0, #1"
```

#### 2. Дизассемблирование
```bash
colibri disasm 90909090 --arch x86
colibri disasm "[arm_thumb:0x8000] 7047"
colibri disasm "[x86_64:0x1000] 554889e5"
```

#### 3. Работа с файлами
```bash
colibri file ~/project.asm --arch arm_thumb
colibri assemble-file /sdcard/Download/boot.asm x86
```

#### 4. Watch (авто-сборка)
```bash
colibri watch ~/project.asm --arch arm_thumb   # фоновое наблюдение
colibri watch-stop                              # остановка
```

#### 5. Статус
```bash
colibri status                                   # Keystone/Capstone availability
```

---

## 📱 Удалённое управление (с ПК)

```bash
# Статус
./mobile_manager.sh kolibri status

# Ассемблирование
./mobile_manager.sh kolibri asm "mov eax, 1" x86
./mobile_manager.sh kolibri asm "[arm_thumb] mov r0, #1"

# Дизассемблирование
./mobile_manager.sh kolibri disasm 90909090 x86
./mobile_manager.sh kolibri disasm "[arm_thumb:0x8000] 7047"

# Файлы
./mobile_manager.sh kolibri file /sdcard/Download/project.asm arm_thumb

# KolibriOS
./mobile_manager.sh kolibri start
./mobile_manager.sh kolibri stop
```

---

## 🔧 Файлы

```
firmwares/redmi-note-8t/
├── scripts/colibri_cli.py                    ← полный CLI (keystone + capstone)
├── scripts/kolibri_termux_setup.sh           ← установка KolibriOS + CLI
├── argos-system-module/system/xbin/
│   ├── argos-status
│   ├── argos-usb-setup
│   ├── argos-can-up
│   ├── argos-bridge
│   └── argos-colibri                        ← system wrapper
└── scripts/termux-multitool-bootstrap.sh     ← алиасы colibri / kolibri-os
```

## Установка на телефон

```bash
# В Termux:
cp /sdcard/Download/kolibri_termux_setup.sh ~
bash ~/kolibri_termux_setup.sh

# Или через PC:
./mobile_manager.sh shell "cp /sdcard/Download/kolibri_termux_setup.sh ~ && bash ~/kolibri_termux_setup.sh"
```

## Связи
- [[Redmi Note 8T Mobile Toolkit]]
- [[USB Arsenal MAX Setup]]
- [[ARGOS]]

[[Backbone Hub]]
