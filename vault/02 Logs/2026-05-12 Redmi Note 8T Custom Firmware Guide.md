# 2026-05-12 Redmi Note 8T — Custom Firmware Guide

## Устройство
- **Model**: Xiaomi Redmi Note 8T
- **Codename**: `willow` (unified with `ginkgo` — Redmi Note 8)
- **SoC**: Qualcomm Snapdragon 665 (SM6125)
- **RAM**: 3/4/6 GB
- **Storage**: 32/64/128 GB eMMC
- **Battery**: 4000 mAh
- **GPU**: Adreno 610

## ⚠️ ПРЕДУПРЕЖДЕНИЕ
- Unlock bootloader **СТИРАЕТ ВСЕ ДАННЫЕ**
- Xiaomi требует **168 часов (7 дней)** ожидания после привязки Mi Account
- Гарантия аннулируется

## 📋 ЭТАПЫ ПРОШИВКИ

### 1. Разблокировка Bootloader (7 дней)

**На телефоне:**
1. `Settings` → `About phone` → тапнуть `MIUI version` 7 раз → Developer mode ON
2. `Settings` → `Additional settings` → `Developer options`:
   - ✅ `OEM unlocking`
   - ✅ `USB debugging`
   - ✅ `USB debugging (Security settings)`
3. `Mi Unlock Status` → `Add account and device`
4. Использовать телефон **7 дней** с этим Mi Account

**На ПК (через 7 дней):**
```bash
# Перезагрузка в fastboot
adb reboot bootloader

# Проверка
fastboot devices

# Unlock (инструмент Mi Unlock Tool)
# Скачать: https://en.miui.com/unlock/
```

### 2. Установка TWRP Recovery

**Скачать:**
- TWRP 3.4.0-10 для ginkgo/willow:
  - https://twrp.me/xiaomi/xiaomiredminote8.html
  - или https://github.com/TeamWin/android_device_xiaomi_ginkgo

```bash
# Перезагрузка в fastboot
adb reboot bootloader

# Прошивка TWRP
fastboot flash recovery twrp-3.4.0-10-ginkgo.img

# Сразу загрузиться в TWRP (ВАЖНО — иначе stock recovery вернётся)
fastboot boot twrp-3.4.0-10-ginkgo.img
```

**В TWRP:**
- Swipe to allow modifications
- `Wipe` → `Format Data` → type `yes`
- `Reboot` → `Recovery` (остаться в TWRP)

### 3. Прошивка LineageOS 22.2 (Android 15)

**Скачать:**
- LineageOS 22.2 для ginkgo/willow:
  - https://download.lineageos.org/devices/ginkgo/builds
  - или https://xdaforums.com/t/official-rom-15-lineageos-22-2-for-redmi-note-8-8t.4743145/

**Требования:**
- Firmware: **Android 11 (MIUI 12.5)** последняя версия
- Если сток Android 9/10 → сначала обновить через MIUI Updater

```bash
# Копирование файлов на телефон (в TWRP, через MTP)
adb push lineage-22.2-*.zip /sdcard/
adb push twrp-3.4.0-10-ginkgo.img /sdcard/

# Или через adb sideload в TWRP:
# TWRP → Advanced → ADB Sideload
adb sideload lineage-22.2-*.zip
```

**В TWRP:**
1. `Wipe` → `Advanced Wipe` → выбрать `System`, `Data`, `Cache`, `Dalvik`
2. `Install` → выбрать `lineage-22.2-*.zip` → Swipe to confirm
3. `Reboot` → `Recovery`

### 4. GApps (опционально)

**Варианты:**
- **NikGapps** (рекомендуется): https://nikgapps.com/
  - Выбрать `core` или `full` для Android 15
- **MindTheGapps**: https://github.com/MindTheGapps/

```bash
adb push NikGapps-core-arm64-15-*.zip /sdcard/
# В TWRP: Install → Swipe
```

### 5. Magisk (Root — опционально)

**Скачать:**
- Magisk APK: https://github.com/topjohnwu/Magisk/releases
- Переименовать `.apk` → `.zip` для прошивки в TWRP

```bash
adb push Magisk-v28.0.zip /sdcard/
# В TWRP: Install → Swipe
```

**После первой загрузки:**
- Установить Magisk APK как обычное приложение
- Magisk Manager → настройка root

### 6. Первый запуск LineageOS

- Первая загрузка: **5-10 минут**
- Настройка без Google (vanilla) или с Google (GMS)
- Проверка SafetyNet (Magisk → Hide)

## 📁 ФАЙЛЫ (workspace)

```
firmwares/redmi-note-8t/
├── twrp/
│   └── twrp-3.4.0-10-ginkgo.img
├── lineageos/
│   └── lineage-22.2-20250607-nightly-ginkgo.zip
├── gapps/
│   └── NikGapps-core-arm64-15-20250607.zip
├── magisk/
│   └── Magisk-v28.0.zip
└── tools/
    └── miunlock/          # Mi Unlock Tool
```

## 🔧 УСТАНОВЛЕННЫЙ СОФТ (ПК)

| Пакет | Назначение |
|-------|-----------|
| `android-tools` | adb, fastboot |
| `android-udev` | udev rules |
| `scrcpy` | Screen mirror |
| `android-file-transfer` | MTP GUI |
| `frida` / `objection` | Runtime pentest |

## ⚡ БЫСТРЫЕ КОМАНДЫ

```bash
# Проверка устройства
adb devices
adb shell getprop ro.product.device    # should be: willow

# Bootloader status
adb reboot bootloader
fastboot getvar unlocked               # yes / no

# Flash всё одним скриптом:
fastboot flash recovery twrp.img
fastboot boot twrp.img
# В TWRP → Wipe → Install LineageOS → Install GApps → Install Magisk → Reboot
```

## 🌐 ССЫЛКИ

| Ресурс | URL |
|--------|-----|
| LineageOS 22.2 XDA | https://xdaforums.com/t/4743145/ |
| LineageOS Downloads | https://download.lineageos.org/devices/ginkgo/builds |
| TWRP Official | https://twrp.me/xiaomi/xiaomiredminote8.html |
| Mi Unlock | https://en.miui.com/unlock/ |
| NikGapps | https://nikgapps.com/ |
| Magisk | https://github.com/topjohnwu/Magisk |
| Firmware Archive | https://roms.miuier.com/en-us/devices/willow/ |

## 📊 ПРОБЛЕМЫ LineageOS 22.2 на willow

| Компонент | Статус |
|-----------|--------|
| Базовая система | ✅ Работает |
| Батарея / производительность | ✅ Хорошо |
| Камера (4x) | ✅ Работает (gcam лучше OpenCamera) |
| IR Blaster | ⚠️ Не работает (известный баг) |
| NFC | ✅ Работает (willow only) |
| Raise to wake | ❌ Нет |
| Dolby Atmos | ❌ Проприетарный, нет |

## Связи
- [[USB Arsenal MAX Setup]]
- [[Xiaomi Redmi Note 8T Setup]]
- [[ARGOS]]

[[Backbone Hub]]
