# 2026-05-12 Xiaomi Redmi Note 8T Setup

## Устройство
- **Xiaomi Redmi Note 8T** — смартфон Android
- VID: `18d1` (Google), PID: `4ee7` (charging + debug)
- Manufacturer: `Xiaomi`
- Product: `Redmi Note 8T`
- Серийник: `97beca7`
- Bus 002 Device 6, High Speed (480 Mbps)
- Режим: ADB debug + charging

## ADB
- `adb devices` → `97beca7 unauthorized` ✅
- **Требуется**: подтвердить авторизацию на экране телефона
- После подтверждения: `adb shell`, `adb logcat`, `adb pull/push`

## Установленный софт
| Пакет | Назначение |
|-------|-----------|
| `android-tools` | `adb`, `fastboot` |
| `android-udev` | UDEV правила для всех Android устройств |
| `scrcpy` | Зеркалирование экрана телефона на ПК |
| `libimobiledevice` / `ifuse` | iOS устройства (дополнительно) |
| `android-studio` | Android IDE |
| `android-sdk-platform-tools` | SDK tools |
| `android-sdk-build-tools` | Build tools |
| `frida` / `frida-tools` | Runtime instrumentation |
| `objection` | Mobile app pentest |

## Использование
```bash
# Зеркалирование экрана
scrcpy --serial 97beca7

# ADB shell
adb -s 97beca7 shell

# Logcat
adb -s 97beca7 logcat

# Frida
frida -U -n com.android.settings

# Fastboot (в режиме bootloader)
adb reboot bootloader
fastboot devices
fastboot flash recovery recovery.img
```

## Права
- Пользователь `ava` добавлен в группы: `adbusers`, `plugdev`

## Связи
- [[USB Arsenal Full Setup]]
- [[ARGOS]]

[[Backbone Hub]]
