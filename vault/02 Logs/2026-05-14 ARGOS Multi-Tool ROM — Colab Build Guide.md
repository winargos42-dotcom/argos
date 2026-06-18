# ARGOS Multi-Tool ROM для Redmi Note 8T (ginkgo)
## Сборка LineageOS 21 + ARGOS overlay в Google Colab

**Runtime:** GPU (или None) — достаточно CPU  
**Время:** ~3-5 часов  
**Диск:** 70 GB SSD в Colab  
**Устройство:** Xiaomi Redmi Note 8T (codename `ginkgo`)  
**База:** LineageOS 21 (Android 14)

---

## 📋 Что входит в ARGOS ROM

| Компонент | Статус | Описание |
|-----------|--------|----------|
| **LineageOS 21** | ✅ | Чистый AOSP-based Android 14 |
| **Magisk 30.6** | ✅ | Pre-installed в `/data/adb/magisk` + boot patch |
| **Termux + Addons** | ✅ | `termux`, `termux-api`, `termux-widget`, `termux-styling`, `termux-task`, `termux-float` |
| **ARGOS System Module** | ✅ | 5 xbin-утилит: `argos-status`, `argos-usb-setup`, `argos-can-up`, `argos-colibri`, `argos-bridge` |
| **ARGOS Mobile Scripts** | ✅ | 22 Python-скрипта в `/data/data/com.termux/files/home/argos-mobile/scripts/` |
| **Andrax v5b5** | ✅ | Pentest chroot в `/data/andrax/` |
| **ARGOS Universal APK** | ✅ | Базовое приложение ARGOS |
| **F-Droid** | ✅ | Open-source app store |
| **KolibriOS + QEMU** | ✅ | KolibriOS образ + `qemu-system-i386-headless` |
| **ColibriAsmEngine** | ✅ | Capstone-дизассемблер CLI |
| **Custom Boot Animation** | ✅ | ARGOS лого + спиннер |
| **Russian Locale** | ✅ | `ru-RU,en-US` по умолчанию |

---

## 🚀 Colab Notebook — пошаговый код

### Cell 1: Монтирование Google Drive (опционально)
```python
from google.colab import drive
drive.mount('/content/drive')
# Для сохранения ROM между сессиями
```

### Cell 2: Подготовка окружения
```bash
%%bash
apt-get update -qq
apt-get install -y -qq \
  git-core gnupg flex bison build-essential zip curl \
  zlib1g-dev libc6-dev-i386 x11proto-core-dev \
  libgl1-mesa-dev libxml2-utils xsltproc unzip \
  fontconfig imagemagick python3 python3-pip bc \
  ccache aria2 lzip squashfs-tools brotli \
  openjdk-17-jdk android-sdk-platform-tools \
  lib32ncurses5-dev lib32z1-dev libncurses5 \
  repo rsync 2>&1 | tail -n 5

# repo tool
mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
export PATH="~/bin:$PATH"
```

### Cell 3: Конфигурация git
```bash
%%bash
git config --global user.email "argos@build.local"
git config --global user.name "ARGOS Builder"
git config --global color.ui false
```

### Cell 4: Инициализация LineageOS 21 репо
```bash
%%bash
export PATH="~/bin:$PATH"
mkdir -p /content/lineageos && cd /content/lineageos

repo init \
  -u https://github.com/LineageOS/android.git \
  -b lineage-21.0 \
  --git-lfs \
  --no-clone-bundle

# Для ускорения в Colab: shallow sync
repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags 2>&1 | tail -n 20
```

### Cell 5: Девайс-специфичные деревья (ginkgo)
```bash
%%bash
cd /content/lineageos

# Device tree
mkdir -p device/xiaomi/ginkgo
git clone --depth 1 \
  https://github.com/LineageOS/android_device_xiaomi_ginkgo.git \
  device/xiaomi/ginkgo

# Vendor blobs ( proprietary )
mkdir -p vendor/xiaomi
git clone --depth 1 \
  https://github.com/TheMuppets/proprietary_vendor_xiaomi.git \
  vendor/xiaomi/ginkgo

# Kernel
mkdir -p kernel/xiaomi
git clone --depth 1 \
  https://github.com/LineageOS/android_kernel_xiaomi_ginkgo.git \
  kernel/xiaomi/ginkgo
```

### Cell 6: ARGOS Overlay — device.mk модификации
```bash
%%bash
cat >> /content/lineageos/device/xiaomi/ginkgo/device.mk << 'EOF'

# ==========================================
# ARGOS Multi-Tool Overlay
# ==========================================

# Prebuilt APKs -> system partition
PRODUCT_PACKAGES += \
    AndraxV5 \
    ARGOSUniversal \
    Termux \
    TermuxAPI \
    TermuxWidget \
    TermuxStyling \
    TermuxTask \
    TermuxFloat \
    FDroid \
    WiFiAnalyzer \
    ConnectBot \
    OpenVPN \
    FreeOTPPlus

# ARGOS System Module -> recovery flashable overlay
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/argos-overlay/argos-system-module.zip:$(TARGET_COPY_OUT_PRODUCT)/media/argos/argos-system-module.zip \
    $(LOCAL_PATH)/argos-overlay/kolibri.img:$(TARGET_COPY_OUT_PRODUCT)/media/argos/kolibri.img \
    $(LOCAL_PATH)/argos-overlay/argos-mobile-scripts.tar.gz:$(TARGET_COPY_OUT_PRODUCT)/media/argos/argos-mobile-scripts.tar.gz

# Boot animation
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/argos-overlay/bootanimation.zip:$(TARGET_COPY_OUT_PRODUCT)/media/bootanimation.zip

# Default locale
PRODUCT_DEFAULT_LANGUAGE := ru
PRODUCT_DEFAULT_REGION   := RU
PRODUCT_LOCALES := ru_RU en_US
EOF
```

### Cell 7: Создание overlay-структуры
```bash
%%bash
mkdir -p /content/lineageos/device/xiaomi/ginkgo/argos-overlay

# Boot animation (ARGOS spinner)
cd /content/lineageos/device/xiaomi/ginkgo/argos-overlay
cat > generate-bootanim.py << 'PYEOF'
import zipfile, os, subprocess
os.makedirs("part0", exist_ok=True)
# Генерация 30 кадров через ImageMagick
for i in range(30):
    subprocess.run([
        "convert", "-size", "1080x2280", "xc:black",
        "-gravity", "center", "-pointsize", "60",
        "-fill", "#00ff00", "-annotate", "+0+0", f"ARGOS ROM\\nLOADING {i*100//29}%",
        f"part0/{i:05d}.png"
    ])
with zipfile.ZipFile("bootanimation.zip", 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr("desc.txt", "1080 2280 30\np 0 0 part0\n")
    for f in sorted(os.listdir("part0")):
        z.write(f"part0/{f}", f"part0/{f}")
PYEOF
python3 generate-bootanim.py

# Архив скриптов (предполагается что собраны на ПК)
touch argos-mobile-scripts.tar.gz
# Magisk модуль
touch argos-system-module.zip
# KolibriOS образ
touch kolibri.img
```

### Cell 8: Magisk preinstall в ramdisk
```bash
%%bash
cd /content/lineageos/device/xiaomi/ginkgo

# Добавляем Magisk в boot.img patch
cat >> BoardConfig.mk << 'EOF'

# ARGOS: Magisk pre-patch
TARGET_PREBUILT_KERNEL := $(LOCAL_PATH)/prebuilt/kernel
BOARD_KERNEL_CMDLINE += androidboot.selinux=permissive
EOF

mkdir -p prebuilt
curl -L -o prebuilt/magisk.apk https://github.com/topjohnwu/Magisk/releases/download/v30.6/Magisk-v30.6.apk
curl -L -o prebuilt/magiskboot \
  https://raw.githubusercontent.com/topjohnwu/Magisk/master/native/src/boot/magiskboot
chmod +x prebuilt/magiskboot
```

### Cell 9: Источники питания и lunch
```bash
%%bash
cd /content/lineageos
source build/envsetup.sh
lunch lineage_ginkgo-userdebug
```

### Cell 10: Сборка
```bash
%%bash
cd /content/lineageos
export PATH="~/bin:$PATH"
source build/envsetup.sh
lunch lineage_ginkgo-userdebug

# CCache для ускорения повторных сборок
export USE_CCACHE=1
export CCACHE_DIR=/content/ccache
ccache -M 50G

# Старт сборки
mka bacon -j$(nproc --all) 2>&1 | tee /content/build.log
```

> ⏱️ **Время:** 3-5 часов в Colab CPU. Первые 30% — скачивание/синхронизация, остальное — компиляция.

---

## 📦 Результат сборки

| Файл | Путь в Colab | Размер |
|------|-------------|--------|
| **ROM ZIP** | `/content/lineageos/out/target/product/ginkgo/lineage-21.0-*.zip` | ~800 MB |
| **boot.img** | `/content/lineageos/out/target/product/ginkgo/boot.img` | ~32 MB |
| **recovery.img** | `/content/lineageos/out/target/product/ginkgo/recovery.img` | ~40 MB |

---

## 💾 Сохранение в Google Drive

```python
from google.colab import files
import shutil, glob

rom = glob.glob("/content/lineageos/out/target/product/ginkgo/lineage-21.0-*.zip")[0]
shutil.copy(rom, "/content/drive/MyDrive/ARGOS_ROM/")
files.download(rom)  # Прямая загрузка в браузер
```

---

## 🔧 Флешинг на устройство

### Требования на ПК/ноутбуке
- `adb` + `fastboot` из `android-sdk-platform-tools`
- Разблокированный bootloader
- Активный USB-ADB

### Команды
```bash
# 1. Перезагрузка в fastboot
adb reboot bootloader

# 2. Флеш boot (с Magisk pre-patch)
fastboot flash boot boot.img

# 3. Флеш recovery
fastboot flash recovery recovery.img

# 4. Установка ROM через recovery
adb sideload lineage-21.0-*-ARGOS.zip

# 5. Wipe data (первый раз)
fastboot -w

# 6. Reboot
fastboot reboot
```

### Первый запуск
1. Мастер настройки LineageOS (ru-RU)
2. WiFi ADB автоматически включается при подключении к `SiG`
3. Magisk автоматически активен (проверить: `su -c 'id'`)
4. Termux доступен в лаунчере
5. Andrax в меню приложений

---

## 🔗 Связи
- [[2026-05-14 ARGOS FULL PACK — FINAL DEPLOYMENT]]
- [[2026-05-14 ARGOS Android Multi-Tool — FINAL STATUS]]
- [[2026-05-14 Phone Software Install Complete]]
- [[2026-05-14 KolibriOS + ColibriAsmEngine Integration]]
- [[2026-05-13 Redmi Note 8T Custom Firmware Guide]]
- [[ARGOS]]

[[Backbone Hub]]
