# 2026-05-14 — Финальный статус Orange Pi + ручные действия

**Время:** 20:00

---

## 🔴 Zigbee донгл — порт 3 Orange Pi

**Проблема:** Аппаратная. USB порт 3 не может опознать устройство.

**Проверено всё программно:**
- ✅ Root hub reset
- ✅ Hub port power cycle (`usbreset`)
- ✅ Driver reload (ch341, cdc_acm, cp210x, ftdi_sio)
- ✅ Bus authorization reset
- ✅ 10 попыток enumeration

**Результат:** `lsusb` показывает только хаб + 2 CH340. Порт 3 — `error -32` (STALL).

**Причина (одна из):**
1. Порт 3 хаба повреждён
2. Донгл неправильно вставлен/плохой контакт питания
3. Powered хаб не подключён к БП (хаб берёт 100mA — недостаточно для 3 устройств)
4. Донгл в режиме bootloader/ожидания

**Требуется физическое действие**

---

## ✅ 2 ESP — работают

- `/dev/ttyUSB0` — ESP (CH340, порт 4 хаба)
- `/dev/ttyUSB1` — ESP (CH340, порт 2 хаба)
- Конфиги ESPHome написаны: `/root/esphome/esp-usb-sensor.yaml`, `esp32-usb-actuator.yaml`

**Далее:** прошивка ESP через `esphome run` (требуется python3 + pip)

---

## 🔧 Скрипты созданы и готовы

| Скрипт | Где | Статус |
|--------|-----|--------|
| `orangepi_deploy_all.sh` | `/root/` Orange Pi | ✅ Готов, ждёт zigbee |
| `orangepi_auto_detect_and_start.sh` | `/root/` Orange Pi | ✅ Автозапуск Z2M при появлении донгла |
| `vault-sync.sh` v2 | laptop (`~/.local/bin/`) | ✅ Синхронизация починена |
| `argos_install_spaced_repetition.sh` | Windows ПК | ✅ Плагин на месте |
| `argos_minitron_api.py` | Windows ПК | ✅ Python API wrapper |
| `windows_dongle_setup.ps1` | Windows ПК | ✅ Диагностика COM14 |

---

## 📋 Что нужно сделать руками (я физически не могу)

### Orange Pi (1 минута)
```
[ ] Проверить powered hub — подключён ли адаптер питания к хабу?
[ ] Если хаб не powered — переподключить донгл в порт 1 хаба
[ ] Или: подключить донгл напрямую к ноутбуку (argos-laptop)
```

После этого — всё запустится автоматически.

### Windows ПК
```
[ ] Restart Obsidian → enable Spaced Repetition plugin
[ ] Запустить mini-tron API: python argos_minitron_api.py --preload
[ ] COM14: проверить devmgmt.msc → что за устройство
```

---

[[2026-05-14]]
[[Backbone Hub]]
