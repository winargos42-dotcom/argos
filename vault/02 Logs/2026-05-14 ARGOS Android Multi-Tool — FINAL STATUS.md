# 2026-05-14 ARGOS Android Multi-Tool — ФИНАЛЬНЫЙ СТАТУС

## ✅ Установлено на Redmi Note 8T (автоматически)

### APK Приложения (установлены через adb)
| Приложение | Пакет | Назначение | Статус |
|------------|-------|-----------|--------|
| **Andrax v5** | `com.thecrackerteam.andrax` | Pentest платформа (Metasploit, nmap, aircrack-ng) | ✅ |
| **Magisk** | `com.topjohnwu.magisk` | Root manager v30.6 | ✅ |
| **F-Droid** | `org.fdroid.fdroid` | Open-source app store | ✅ |
| **Termux** | `com.termux` | Terminal emulator | ✅ |
| **Termux:API** | `com.termux.api` | Termux addons | ✅ |
| **ARGOS Universal** | `org.iliyaqdrwalqu.argos.argos_universal` | ARGOS base APK | ✅ |

### Magisk System Module
| Бинарник | Назначение |
|----------|-----------|
| `argos-status` | Системный статус (root, USB, CAN, сеть) |
| `argos-usb-setup` | Права 666 на /dev/ttyUSB*, /dev/bus/usb |
| `argos-can-up` | Поднять CAN интерфейс (can0 @ 500000) |
| `argos-colibri` | KolibriOS + ColibriAsmEngine wrapper |
| `argos-bridge` | ARGOS network bridge launcher |

### Termux Пакеты (pkg install)
| Пакет | Назначение |
|-------|-----------|
| `tsu` | Root wrapper для Termux |
| `openssh` | SSH сервер :8022 |
| `nmap` | Сканер сети |
| `usbutils` | lsusb |
| `qemu-system-i386-headless` | QEMU для KolibriOS |
| `clang` | C/C++ compiler |
| `cmake` | Build system |
| `make` | Make utility |
| `python3` + `pip` | Python runtime |

### Python библиотеки
| Библиотека | Назначение | Статус |
|------------|-----------|--------|
| `pyserial` | USB-UART работа | ✅ |
| `pyusb` | USB direct access | ✅ |
| `requests` | HTTP клиент | ✅ |
| `paho-mqtt` | MQTT протокол | ✅ |
| `rich`, `colorama`, `prompt-toolkit` | CLI UI | ✅ |
| `capstone` | Дизассемблирование (disasm) | ✅ v5.0.7 |
| `keystone-engine` | Ассемблирование (asm) | ❌ не собирается на Termux |

### ARGOS Scripts (17 файлов)
- `usb_scan.py`, `obd_bridge.py`, `uart_bridge.py`, `can_sniff.py`, `ble_scan.py`
- `ch341a_dump.py`, `debug_bridge.py`, `xgecu_bridge.py`, `fnirsi_scope.py`
- `wifi_pentest.py`, `argos_bridge.py`, `argos_mobile_dashboard.py`
- `start_argos.sh`, `stop_argos.sh`
- 23 алиаса в `.bashrc_argos`

---

## 📲 Ручная установка (через F-Droid / Play Store)

Откройте **F-Droid** на телефоне, обновите репозиторий и установите:

### USB / Serial
| Приложение | Источник | Назначение |
|-----------|----------|-----------|
| **Serial USB Terminal** | Play Store / APKPure | CH340/FTDI/CP210x terminal |
| **DroidTerm** | F-Droid | USB serial terminal |
| **Physicaloid** | GitHub | Библиотека + demo |

### BLE
| Приложение | Источник | Назначение |
|-----------|----------|-----------|
| **nRF Connect** | Play Store / nordicsemi.com | BLE scanner, DFU, GATT |
| **nRF Toolbox** | Play Store | BLE profiles demo |

### OBD-II
| Приложение | Источник | Назначение |
|-----------|----------|-----------|
| **Car Scanner ELM OBD2** | Play Store | ELM327 диагностика |
| **Torque** | Play Store | OBD дашборд |

### WiFi
| Приложение | Источник | Назначение |
|-----------|----------|-----------|
| **WiFi Analyzer** | F-Droid / Play Store | WiFi сканирование |
| **aircrack-ng** | Termux | WiFi pentest (уже в Andrax) |

### Widgets / Automation
| Приложение | Источник | Назначение |
|-----------|----------|-----------|
| **Termux:Widget** | F-Droid | Виджеты для скриптов на рабочем столе |
| **Termux:Styling** | F-Droid | Темы для Termux |

---

## 🚀 Быстрый старт с ПК

```bash
# Статус системы
./mobile_manager.sh shell "su -c 'bash /data/adb/modules/argos-system/system/xbin/argos-status'"

# USB права
./mobile_manager.sh shell "su -c 'bash /data/adb/modules/argos-system/system/xbin/argos-usb-setup'"

# Colibri (дизассемблирование)
./mobile_manager.sh shell "python3 ~/argos-kolibri/colibri/colibri_cli.py disasm 90909090 --arch x86"

# Andrax запуск
./mobile_manager.sh shell "am start -n com.thecrackerteam.andrax/.MainActivity"
```

---

## ⚠️ Ограничения

- **keystone-engine** (assembly) — не компилируется на Android/Termux. Используйте ПК или онлайн ассемблеры.
- **Проприетарные APK** (Serial USB Terminal, nRF Connect, Car Scanner) — требуют Play Store или ручного download с APKPure/APKMirror.
- **KolibriOS образ** — требуется скачать kolibri.img и положить в `~/argos-kolibri/images/`

## Связи
- [[KolibriOS + ColibriAsmEngine Integration]]
- [[Phone Software Install Complete]]
- [[ARGOS]]

[[Backbone Hub]]
