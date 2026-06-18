# Orange Pi USB Power Issue — Диагностика

**Время:** 19:40  
**Устройство:** Orange Pi One H3 (192.168.2.168)  
**Симптом:** ESP + Zigbee донгл не опознаются (`lsusb` показывает только хаб)

---

## 🔍 Диагностика

### 1. USB устройства (после удаления CAN адаптера)
```
Bus 002 Device 002: ID 1a40:0101 Terminus Technology Inc. Hub
```
Только хаб. Подключенные устройства (ESP, Zigbee) **не видны**.

### 2. dmesg ошибки
```
usb 2-1.4: device descriptor read/64, error -110
usb 2-1-port4: unable to enumerate USB device
usb usb2-port1: cannot reset (err = -32)
usb usb2-port1: Cannot enable. Maybe the USB cable is bad?
```

### 3. Хаб питание
```
Hub power: 100mA
```
**⚠️ Критически мало!** Bus-powered хаб без внешнего питания.

### 4. Orange Pi One H3 specs
- 1x USB 2.0 Host порт
- Максимальный ток: ~500mA (USB spec)
- Хаб Terminus (100mA) + 2 ESP (~150mA каждый) + Zigbee (~50mA) = **~450mA+**
- При старте ESP может потреблять до 300mA (WiFi startup)
- **Итог:** хаб отключает порты из-за over-current

---

## 🎯 Вердикт

**Проблема:** Нехватка питания через USB. Bus-powered хаб не справляется с 2 ESP + Zigbee.

**Решения:**

### A) Powered USB Hub ✅ Рекомендуется
Подключить хаб с **внешним блоком питания 5V 2A+**. Тогда:
- Хаб питается от БП
- Orange Pi только передаёт данные
- Все устройства получают достаточно тока

### B) Подключить к ноутбуку (fallback)
Если powered hub нет — подключить ESP и Zigbee к **ноутбуку** (argos-laptop):
- USB порты ноутбука мощнее
- Zigbee2MQTT можно запустить на ноутбуке
- ESPHome flasher работает на Linux

### C) По одному устройству
Подключить только **одно** устройство к Orange Pi напрямую (без хаба):
- Либо Zigbee донгл
- Либо 1 ESP
- Но не все сразу

---

## 🔧 Что настроено автоматически

При появлении питания/подключении, скрипты готовы:
- `orangepi_deploy_all.sh` — сканирует порты, пишет Z2M + ESPHome конфиги
- Драйверы `ch341`, `cdc_acm`, `usbserial` уже загружены

---

## 📋 Чеклист

- [ ] Подключить **powered USB hub** к Orange Pi
- [ ] Подключить ESP + Zigbee к powered hub
- [ ] Перезагрузить Orange Pi: `reboot`
- [ ] Проверить: `lsusb` должно показать все устройства
- [ ] Запустить `orangepi_deploy_all.sh`

[[2026-05-14]]
[[Backbone Hub]]
