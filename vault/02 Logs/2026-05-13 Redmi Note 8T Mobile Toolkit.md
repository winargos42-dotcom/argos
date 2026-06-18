# 2026-05-13 Redmi Note 8T — Полевой Мультитул (Mobile Toolkit)

## ✅ ТЕЛЕФОН КАК ИНСТРУМЕНТ

### Сеть
| Параметр | Значение |
|----------|----------|
| **IP** | `192.168.1.149` |
| **WiFi** | SiG (5GHz, WPA2, RSSI -51) |
| **ADB** | USB + WiFi (`:5555`) |
| **SSH** | `8022` (ожидает bootstrap) |

### Статус компонентов
| Компонент | Статус |
|-----------|--------|
| LineageOS 21 | ✅ |
| Bootloader unlocked | ✅ |
| Termux | ✅ v1022 |
| Termux:API | ✅ |
| ADB over WiFi | ✅ |
| Root (su/Magisk) | ❌ (нужен для OTG полный доступ) |
| SSH daemon | ❌ (запустится после bootstrap) |

## 📁 ФАЙЛЫ МУЛЬТИТУЛА

```
firmwares/redmi-note-8t/
├── scripts/
│   ├── redmi8t-tool.sh              ← Управление прошивкой (fastboot)
│   ├── mobile_manager.sh            ← Управление телефоном с ПК (ADB WiFi)
│   └── termux-multitool-bootstrap.sh ← Bootstrap для Termux (Android)
├── apps/
│   ├── termux.apk                   (уже установлен v1022)
│   ├── termux-api.apk              ✅ установлен
│   └── fdroid.apk                   (уже установлен)
└── logs/ / captures/
```

## 🛠️ УПРАВЛЕНИЕ С ПК

```bash
cd /home/ava/Projects/argoss/firmwares/redmi-note-8t

# Статус телефона
./scripts/mobile_manager.sh status

# Скриншот
./scripts/mobile_manager.sh screenshot

# Logcat
./scripts/mobile_manager.sh logcat

# ADB shell команда
./scripts/mobile_manager.sh shell "lsusb"
./scripts/mobile_manager.sh shell "dumpsys battery"

# Перезагрузка
./scripts/mobile_manager.sh reboot

# Push файла на телефон
./scripts/mobile_manager.sh push firmware.bin

# Установить APK из apps/
./scripts/mobile_manager.sh install_apps
```

## 📱 НАСТРОЙКА TERMUX (на телефоне)

**Шаг 1:** Открыть приложение **Termux**

**Шаг 2:** Скопировать bootstrap:
```bash
cp /sdcard/Download/argos-termux-bootstrap.sh ~
```

**Шаг 3:** Запустить установку:
```bash
bash ~/argos-termux-bootstrap.sh
```

**Шаг 4:** Перезапустить Termux

**После этого доступны:**
- `obd` — OBD-II bridge (USB OTG + ELM327)
- `uart` — USB-UART терминал (CH340/FTDI)
- `scan` — USB device scanner
- `can-sniff` — CAN bus (требует root)
- `flash` — Firmware утилита
- SSH сервер на `:8022`

## 🔌 USB OTG АРСЕНАЛ

| Устройство | Android-совместимость | Требуется |
|------------|----------------------|-----------|
| **Scanmatik SM-2** | ⚠️ pyusb через termux-usb | Root или Termux API |
| **FTDI OBD (0403:b470)** | ✅ pyserial/ELM327 | OTG адаптер |
| **CH340 USB-UART** | ✅ pyserial | OTG адаптер |
| **J-Link V9** | ⚠️ pylink-square? | Root |
| **ST-Link V2** | ⚠️ stlink? | Root |
| **XGecu T48** | ❌ Нет Android софта | Только ПК |
| **FNIRSI 2C23T** | ❌ Нет Android драйвера | Только ПК |

## 🚀 БЫСТРЫЙ СТАРТ

```bash
# ПК: проверить статус
./scripts/mobile_manager.sh status

# Телефон: в Termux
bash ~/argos-termux-bootstrap.sh

# ПК: подключиться по SSH
ssh -p 8022 u0_a149@192.168.1.149

# Или через ADB shell в Termux (но изолирован):
adb shell "am start -n com.termux/.app.TermuxActivity"
```

## 📦 РЕКОМЕНДУЕМЫЕ ANDROID-ПРИЛОЖЕНИЯ

| Приложение | Назначение | Источник |
|------------|-----------|----------|
| **Car Scanner ELM OBD2** | OBD диагностика | Play Store |
| **Serial USB Terminal** | USB-UART монитор | Play Store |
| **nRF Connect** | BLE сканер | Play Store |
| **WiFi Analyzer** | WiFi анализ | Play Store / F-Droid |
| **MQTT Dash** | IoT dashboard | Play Store |
| **Termux:Widget** | Виджеты | F-Droid |
| **Termux:Styling** | Темы | F-Droid |

## 🔐 ROOT (опционально, для полного OTG)

Для прямого доступа к `/dev/ttyUSB*`, `/dev/bus/usb` и CAN bus:

**Вариант A — LineageOS Rooted Debugging:**
```
Settings → System → Developer options → Rooted debugging → ON
```

**Вариант B — Magisk:**
```bash
# TWRP → Install → Magisk.zip → Reboot
# Или patched boot image через fastboot
```

## Связи
- [[USB Arsenal MAX Setup]]
- [[Redmi Note 8T Analysis + Multi-Tool]]
- [[Redmi Note 8T Custom Firmware Guide]]
- [[ARGOS]]

[[Backbone Hub]]
