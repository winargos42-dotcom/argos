# 2026-05-14 ARGOS FULL PACK — Финальное развёртывание

## ✅ Что установлено (автоматически через adb)

### 📱 APK Приложения
| Приложение | Пакет | Назначение | Статус |
|-----------|-------|-----------|--------|
| **Andrax** | `com.thecrackertechnology.andrax` | Pentest: Metasploit, nmap, aircrack-ng, sqlmap | ✅ |
| **Magisk** | `com.topjohnwu.magisk` | Root manager v30.6 | ✅ |
| **F-Droid** | `org.fdroid.fdroid` | Open-source app store | ✅ |
| **Termux** | `com.termux` | Terminal emulator | ✅ |
| **Termux:API** | `com.termux.api` | Termux addons | ✅ |
| **Termux:Widget** | `com.termux.widget` | Termux widgets на рабочий стол | ✅ |
| **Termux:Styling** | `com.termux.styling` | Темы Termux | ✅ |
| **Termux:Task** | `com.termux.tasker` | Интеграция с Tasker | ✅ |
| **Termux:Float** | `com.termux.window` | Плавающее окно Termux | ✅ |
| **ARGOS Universal** | `org.iliyaqdrwalqu.argos.argos_universal` | ARGOS base APK | ✅ |
| **WiFi Analyzer** | `com.vrem.wifianalyzer` | WiFi сканер + графики | ✅ |
| **ConnectBot** | `org.connectbot` | SSH клиент | ✅ |
| **OpenVPN** | `de.blinkt.openvpn` | OpenVPN клиент | ✅ |
| **FreeOTP+** | `org.liberty.android.freeotpplus` | 2FA генератор | ✅ |

### 🔧 Magisk System Module
| | |
|---|---|
| `argos-status` | ✅ |
| `argos-usb-setup` | ✅ |
| `argos-can-up` | ✅ |
| `argos-colibri` | ✅ |
| `argos-bridge` | ✅ |

### 🐧 Termux Scripts (22 файла в `~/argos-mobile/`)
- USB scanner (CH340/FTDI/ELM327/Scanmatik)
- OBD-II bridge
- UART terminal
- CAN sniffer
- BLE scanner
- CH341A dumper
- XGecu bridge
- Debug bridge (J-Link/ST-Link)
- WiFi pentest
- ColibriAsmEngine CLI (disasm ✅, asm ⏳)
- ARGOS bridge (agent :7779)
- 23 алиаса в `.bashrc_argos`

## ⚠️ Что требует ручного запуска (1 команда в Termux)

**Причина**: Termux `pkg install` и `pip install` блокируются при запуске от root. Нужно запускать в GUI Termux от пользователя u0_a567. adb `input text` injection ненадёжен для больших скриптов.

Введите в Termux **одну команду** — она сделает всё:

```bash
# === ЕДИНСТВЕННАЯ КОМАНДА НА ТЕЛЕФОНЕ ===
# Откройте приложение Termux и вставьте:
bash ~/termux_full_install.sh
```

Скрипт `termux_full_install.sh` уже лежит в `~/` и установит:
- `tsu openssh nmap usbutils`
- `clang cmake make ninja`
- `qemu-system-i386-headless`
- `aircrack-ng tcpdump`
- `python3 python-pip`
- `avrdude openocd stlink`

Затем:
```bash
bash ~/python_full_install.sh
```

Это установит:
- `torch transformers opencv`
- `scapy impacket`
- `capstone unicorn`
- `fastapi uvicorn`

## 📲 Ручная установка (Play Store / 4PDA)

**Закрытые APK не скачиваются автоматически** (нет Google Play API ключа):

| Устройство | Приложение | Где взять |
|-----------|-----------|-----------|
| ELM327 OBD-II | **Car Scanner ELM OBD2** | Play Store |
| ELM327 OBD-II alt. | **Torque Pro** | Play Store |
| BLE nRF52 | **nRF Connect** | Play Store / nordicsemi.com |
| USB-UART CH340 | **Serial USB Terminal** | Play Store (Kai Morich) |
| USB-UART alt. | **USB Serial Pro** | Play Store |
| J-Link | **J-Link OB** | nordicsemi.com |
| WiFi pentest | **WiGLE WiFi Wardriving** | Play Store |
| CAN bus | нет нативного Android GUI | Только через Termux + CAN-utils |

## 🚀 Быстрый старт с ПК

```bash
# Статус
./mobile_manager.sh shell "su -c 'argos-status'"

# USB права
./mobile_manager.sh shell "su -c 'argos-usb-setup'"

# Colibri (дизассемблирование)
./mobile_manager.sh shell "python3 ~/argos-kolibri/colibri/colibri_cli.py disasm 90909090 --arch x86"

# Andrax запуск
./mobile_manager.sh shell "am start -n com.thecrackertechnology.andrax/.MainActivity"

# WiFi Analyzer
./mobile_manager.sh shell "am start -n com.vrem.wifianalyzer/.MainActivity"
```

## 📁 Файлы арсенала

```
firmwares/redmi-note-8t/
├── apps/
│   ├── termux.apk                 ✅
│   ├── termux-api.apk            ✅
│   ├── fdroid.apk                ✅
│   └── from_phone/
│       └── andraxv5b5.apk        ✅
├── scripts/
│   ├── redmi8t-tool.sh v2.0      ← прошивка, backup, root info
│   ├── mobile_manager.sh v2.0    ← ADB WiFi управление
│   ├── termux-multitool-bootstrap.sh v3.0 ← алиасы
│   ├── argos_android_full_setup.sh ← полная установка
│   ├── argos_mobile_dashboard.py ← Web UI
│   ├── install_argos_system.sh   ← Magisk модуль
│   ├── kolibri_termux_setup.sh   ← KolibriOS + Colibri
│   ├── colibri_cli.py            ← Asm/Disasm CLI
│   └── argos_fullpack_installer.sh ← этот инсталлятор
├── argos-system-module/           ← Magisk модуль
└── vault/
    └── 2026-05-14 ARGOS FULL PACK — FINAL DEPLOYMENT.md
```

## Связи
- [[KolibriOS + ColibriAsmEngine Integration]]
- [[Phone Software Install Complete]]
- [[ARGOS]]

[[Backbone Hub]]
