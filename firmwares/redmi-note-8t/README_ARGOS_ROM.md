# ARGOS Multi-Tool ROM для Redmi Note 8T (ginkgo)
## Версия 1.0 | 2026-05-14

---

## 📦 Варианты установки

### Вариант A: Flashable Zip (быстро, 71KB)
Добавляет ARGOS tools к существующей LineageOS. **Установить через TWRP** поверх текущей прошивки.

```
ARGOS-ROM-v1.0-ginkgo.zip
├── system/xbin/argos-*          # 5 системных tools
├── system/etc/init.d/99argos    # Автозагрузка
├── data/adb/modules/argos-system/ # Magisk module
└── data/local/argos/scripts/    # 24 Python scripts
```

**Размер:** 71 KB (только скрипты, бинарники ставятся отдельно через Termux)

### Вариант B: Полноценная LOS + ARGOS прошивка
Сборка **LineageOS 21 из исходников** с pre-installed ARGOS компонентами.

---

## 🔧 Структура прошивки

```
argos-rom/
├── boot/                          # Kernel patches
│   └── argos-kernel.patch       # USB OTG + serial driver patches
├── device/
│   └── xiaomi/
│       └── ginkgo/
│           ├── Android.mk         # Prebuilt APKs
│           └── device.mk          # ARGOS overlay
├── META-INF/
│   └── com/google/android/
│       ├── update-binary          # TWRP installer
│       └── updater-script         # Edify script
├── data/
│   └── adb/modules/argos-system/  # Magisk module
├── system/
│   ├── xbin/argos-*               # ARGOS tools
│   ├── etc/init.d/99argos        # Boot init
│   └── permissions/
│       └── com.argos.hardware.xml
├── prebuilts/argos/              # Prebuilt APKs
│   ├── Termux.apk
│   ├── F-Droid.apk
│   └── WiFiAnalyzer.apk
└── out/ARGOS-ROM-v1.0-ginkgo.zip # Flashable zip
```

---

## 📋 Build инструкция (LOS + ARGOS из исходников)

### 1. Подготовка системы (200GB+ SSD)
```bash
sudo pacman -S repo git python3 python-pip jdk17 gradle
mkdir -p ~/ lineageos && cd ~/lineageos
```

### 2. Инициализация repo
```bash
repo init -u https://github.com/LineageOS/android.git -b lineage-21.0 --git-lfs
```

### 3. Device tree ginkgo
```bash
mkdir -p .repo/local_manifests
cat > .repo/local_manifests/argos_ginkgo.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <project name="LineageOS/android_device_xiaomi_ginkgo" path="device/xiaomi/ginkgo" remote="github" />
  <project name="LineageOS/android_device_xiaomi_sm6150-common" path="device/xiaomi/sm6150-common" remote="github" />
  <project name="LineageOS/android_kernel_xiaomi_ginkgo" path="kernel/xiaomi/ginkgo" remote="github" />
  <project name="LineageOS/android_vendor_xiaomi_ginkgo" path="vendor/xiaomi/ginkgo" remote="github" />
  <!-- ARGOS overlay -->
  <project name="argos-team/argos-rom" path="device/xiaomi/ginkgo/argos" remote="github" />
</manifest>
EOF
repo sync -c -j$(nproc --all)
```

### 4. Применение ARGOS overlay
```bash
cp -r device/xiaomi/ginkgo/argos/* device/xiaomi/ginkgo/
# Редактировать device/xiaomi/ginkgo/device.mk:
# $(call inherit-product, device/xiaomi/ginkgo/argos/device.mk)
```

### 5. Kernel patches (USB OTG + Serial)
```bash
cd kernel/xiaomi/ginkgo
patch -p1 < ../../device/xiaomi/ginkgo/boot/argos-kernel.patch
# или ручное редактирование:
# CONFIG_USB_SERIAL=y
# CONFIG_USB_SERIAL_CH341=y
# CONFIG_USB_SERIAL_FTDI_SIO=y
# CONFIG_USB_SERIAL_CP210X=y
# CONFIG_USB_SERIAL_PL2303=y
# CONFIG_CAN=y
# CONFIG_CAN_MCP251X=y
```

### 6. Сборка
```bash
cd ~/lineageos
source build/envsetup.sh
lunch lineage_ginkgo-userdebug
mka bacon -j$(nproc --all)
# Результат: out/target/product/ginkgo/lineage-21.0-*.zip (~1.5GB)
```

### 7. Интеграция ARGOS в выходной zip
```bash
# Распаковать LOS zip
unzip out/target/product/ginkgo/lineage-21.0-*.zip -d /tmp/argos_los/
# Добавить ARGOS overlay
# Перепаковать
```

---

## 🚀 Установка (end-user)

### Требования
- **Redmi Note 8T** (ginkgo/willow)
- **Unlocked bootloader**
- **TWRP** (обязательно)
- **Бэкап** (сделан ✅)

### Шаги
```bash
# 1. Boot in TWRP (Volume Up + Power)
# 2. Wipe -> Format Data (если чистая установка)
# 3. Install -> выбрать lineage-21.0-...zip (LOS базовая)
# 4. Install -> выбрать ARGOS-ROM-v1.0-ginkgo.zip (ARGOS overlay)
# 5. Reboot System
```

---

## 🛡️ Pre-installed в ARGOS ROM

### Magisk Module (авто)
- argos-status, argos-usb-setup, argos-can-up, argos-colibri, argos-bridge

### Termux (pre-installed)
- Python 3.13, pip, pyserial, pyusb, python-can, bleak, capstone, rich
- Rust, Go, Clang, Nmap, Tshark, Avrdude

### APKs (pre-installed)
- Termux + Termux:Widget + Termux:Styling + Termux:Task + Termux:Float
- Andrax v5
- Magisk 30.6
- WiFi Analyzer
- ConnectBot, FreeOTP+, OpenVPN

### Scripts (/data/local/argos/)
- usb_scan.py, obd_bridge.py, uart_bridge.py
- can_sniff.py, ble_scan.py
- ch341a_dump.py, debug_bridge.py, xgecu_bridge.py
- fnirsi_scope.py, wifi_pentest.py
- argos_mobile_dashboard.py, colibri_cli.py

### System
- Russian locale (ru-RU)
- USB Serial permissions (CH340/FTDI/CP210x/PL2303)
- CAN interface auto-up
- ARGOS init.d script

---

## 📊 Параметры

| Компонент | Размер | RAM |
|-----------|--------|-----|
| LOS 21 base | ~1.5 GB | ~400 MB |
| ARGOS overlay | ~71 KB | ~0 |
| Termux + tools | ~600 MB (optional) | ~100 MB |
| Andrax chroot | ~15 GB (optional) | ~500 MB |
| **Total system** | **~2-3 GB** | **~600 MB** |

---

## 🔗 Ссылки

- **Flashable zip**: `/home/ava/Projects/argoss/firmwares/redmi-note-8t/ARGOS-ROM-v1.0-ginkgo.zip`
- **Device tree**: [LineageOS/android_device_xiaomi_ginkgo](https://github.com/LineageOS/android_device_xiaomi_ginkgo)
- **Kernel**: [LineageOS/android_kernel_xiaomi_ginkgo](https://github.com/LineageOS/android_kernel_xiaomi_ginkgo)
- **XDA ginkgo**: [Redmi Note 8T development](https://forum.xda-developers.com/c/redmi-note-8t.9827/)

---

*ARGOS Multi-Tool ROM — мобильная лаборатория пентеста и hardware-hacking в кармане.*
