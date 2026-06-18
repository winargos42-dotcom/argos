# 2026-05-14 Phone Software Installation — Final Status

## ✅ Установлено на телефоне (автоматически + Termux GUI)

### System Level (Magisk Module)
| Компонент | Путь | Статус |
|-----------|------|--------|
| argos-status | /data/adb/modules/argos-system/system/xbin/ | ✅ |
| argos-usb-setup | /data/adb/modules/argos-system/system/xbin/ | ✅ |
| argos-can-up | /data/adb/modules/argos-system/system/xbin/ | ✅ |
| argos-colibri | /data/adb/modules/argos-system/system/xbin/ | ✅ |
| argos-bridge | /data/adb/modules/argos-system/system/xbin/ | ✅ |

### Termux Packages (pkg install через GUI + adb input)
| Пакет | Статус |
|-------|--------|
| tsu | ✅ |
| openssh | ✅ |
| nmap | ✅ |
| usbutils | ✅ |
| qemu-system-i386-headless | ✅ |
| clang | ✅ |
| cmake | ✅ |
| make | ✅ |
| python3 | ✅ |
| pip | ✅ |

### Python библиотеки
| Библиотека | Статус |
|------------|--------|
| pyserial | ✅ |
| pyusb | ✅ |
| requests | ✅ |
| paho-mqtt | ✅ |
| rich | ✅ |
| colorama | ✅ |
| prompt-toolkit | ✅ |
| capstone | ✅ v5.0.7 (дизассемблирование) |
| keystone-engine | ❌ не удалось скомпилировать на Termux |

### ARGOS Scripts
- 16 скриптов в `~/argos-mobile/scripts/`
- 23 алиаса в `.bashrc_argos`
- Colibri CLI: `~/argos-kolibri/colibri/colibri_cli.py`

## 🔧 ColibriAsmEngine — текущий статус

**Дизассемблирование (capstone) — РАБОТАЕТ:**
```bash
colibri disasm 90909090 --arch x86
colibri disasm "[arm_thumb:0x8000] 7047"
```

**Ассемблирование (keystone) — НЕДОСТУПНО:**
- keystone-engine не компилируется на Android/Termux
- Требует сложной сборки C++ библиотеки с LLVM backend
- Альтернатива: онлайн ассемблеры, или собрать на ПК

## ⚠️ Ограничения
- `keystone-engine` (assembly) — требует ручной сборки на ПК или другой toolchain
- DNS не работает в `su <uid>` контексте — pip/pkg только через Termux GUI
- QEMU для KolibriOS установлен, но KolibriOS образ ещё не скачан

## 🚀 Использование с ПК
```bash
# Проверка статуса
./mobile_manager.sh shell "su -c 'bash /data/adb/modules/argos-system/system/xbin/argos-status'"

# Colibri (дизассемблирование)
./mobile_manager.sh shell "python3 ~/argos-kolibri/colibri/colibri_cli.py disasm 90909090 --arch x86"

# USB права
./mobile_manager.sh shell "su -c 'bash /data/adb/modules/argos-system/system/xbin/argos-usb-setup'"
```

## Связи
- [[KolibriOS + ColibriAsmEngine Integration]]
- [[Redmi Note 8T Mobile Toolkit]]
- [[ARGOS]]

[[Backbone Hub]]
