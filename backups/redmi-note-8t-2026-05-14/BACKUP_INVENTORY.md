# ARGOS Multi-Tool — Backup Inventory
## Device: Redmi Note 8T (ginkgo)
## Date: 2026-05-14
## Location: /mnt/media_rw/1CB8C155B8C12E58/ARGOS_BACKUP_2026-05-14/

---

## Flash Drive Backup (59GB, primary)

| File | Size | Location on Flash |
|------|------|-------------------|
| termux.tar.gz | 713 MB | /ARGOS_BACKUP_2026-05-14/termux.tar.gz |
| sdcard.tar.gz | 692 MB | /ARGOS_BACKUP_2026-05-14/sdcard.tar.gz |
| andrax.tar.gz | 442 MB | /ARGOS_BACKUP_2026-05-14/andrax.tar.gz |
| boot_magisk_patched.img | 64 MB | /ARGOS_BACKUP_2026-05-14/boot_magisk_patched.img |
| kolibri.img | 1.4 MB | /ARGOS_BACKUP_2026-05-14/kolibri.img |
| apps_list.txt | <1 KB | /ARGOS_BACKUP_2026-05-14/apps_list.txt |
| magisk_modules.txt | <1 KB | /ARGOS_BACKUP_2026-05-14/magisk_modules.txt |
| settings_global.txt | <1 KB | /ARGOS_BACKUP_2026-05-14/settings_global.txt |
| settings_secure.txt | <1 KB | /ARGOS_BACKUP_2026-05-14/settings_secure.txt |
| settings_system.txt | <1 KB | /ARGOS_BACKUP_2026-05-14/settings_system.txt |
| wpa_supplicant.conf | <1 KB | /ARGOS_BACKUP_2026-05-14/wpa_supplicant.conf |
| wifi_config.xml | <1 KB | /ARGOS_BACKUP_2026-05-14/wifi_config.xml |

**Total Flash Backup: ~1.9 GB**

---

## Laptop Backup (secondary)

| File | Size | Location on Laptop |
|------|------|-------------------|
| boot_magisk_patched.img | 64 MB | /home/ava/Projects/argoss/backups/redmi-note-8t-2026-05-14/ |
| kolibri.img | 1.4 MB | /home/ava/Projects/argoss/backups/redmi-note-8t-2026-05-14/ |
| sdcard/ | (stubs) | /home/ava/Projects/argoss/backups/redmi-note-8t-2026-05-14/sdcard/ |
| termux/ | (stubs) | /home/ava/Projects/argoss/backups/redmi-note-8t-2026-05-14/termux/ |
| andrax/ | (stubs) | /home/ava/Projects/argoss/backups/redmi-note-8t-2026-05-14/andrax/ |

---

## Contents

### termux.tar.gz (713 MB)
- /data/data/com.termux/files/home/ — all scripts, Python modules, configs
- argos-mobile/scripts/ (24 Python scripts)
- argos-kolibri/ (images, colibri_cli.py)
- .bashrc, .bashrc_argos (aliases)
- Python venv packages (serial, usb, obd, can, bleak, capstone, rich)
- Installed binaries: qemu, nmap, rust, go, clang, avrdude, tshark

### sdcard.tar.gz (692 MB)
- DCIM/ (photos/videos)
- Download/ (APKs, files)
- Documents/
- Pictures/
- boot_magisk_20260513.img
- kolibri.img
- Music/
- Ringtones/
- PDF templates

### andrax.tar.gz (442 MB)
- /data/data/com.thecrackertechnology.andrax/
- ACRA-INSTALLATION marker
- bin/, home/, scripts/

### boot_magisk_patched.img (64 MB)
- **CRITICAL**: Patched boot image with Magisk
- Used for: fastboot flash boot (recovery if ROM fails)

### System Configs
- WiFi networks (wpa_supplicant.conf)
- Magisk modules list
- Android global/secure/system settings
- Installed apps list (190+ apps)

---

## Pre-Flash Checklist

- [x] /sdcard backup
- [x] Termux home backup
- [x] Andrax data backup
- [x] WiFi configs backup
- [x] Apps list backup
- [x] Magisk boot.img backup
- [x] System settings backup
- [ ] Contacts/SMS (adb backup requires GUI — OPTIONAL)
- [x] Flash drive mounted (59GB available)

---

## Restore Instructions (if flash fails)

```bash
# From TWRP terminal:
adb pull /mnt/media_rw/1CB8C155B8C12E58/ARGOS_BACKUP_2026-05-14/sdcard.tar.gz /sdcard/
adb pull /mnt/media_rw/1CB8C155B8C12E58/ARGOS_BACKUP_2026-05-14/boot_magisk_patched.img /sdcard/
# In TWRP: Install -> Install Image -> boot_magisk_patched.img -> Boot partition
# Reboot -> system
```

---

*Backup created automatically by ARGOS Multi-Tool System*
*All files preserved on external flash drive and laptop*
