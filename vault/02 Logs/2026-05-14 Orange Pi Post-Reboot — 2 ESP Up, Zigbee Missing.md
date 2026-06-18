# 2026-05-14 — Orange Pi + Powered Hub — Статус после ручной перезагрузки

**Время:** 19:55  
**Действие:** Пользователь перезагрузил Orange Pi вручную после подключения powered USB hub  

---

## ✅ Что работает

### 2 ESP на CH340
| Порт | Устройство | Описание |
|------|-----------|----------|
| ttyUSB0 | **Bus 002 Device 007** | QinHeng CH340 serial converter (порт 4 хаба) |
| ttyUSB1 | **Bus 002 Device 008** | QinHeng CH340 serial converter (порт 2 хаба) |

- Драйвер `ch341` загружен
- Оба порта доступны для чтения/записи
- ESPHome конфиги созданы:
  - `/root/esphome/esp-usb-sensor.yaml` (ESP8266)
  - `/root/esphome/esp32-usb-actuator.yaml` (ESP32)
  - `/root/esphome/secrets.yaml`

---

## ❌ Что не работает

### Zigbee донгл
**Порт:** 3 (2-1.3)  
**Ошибки dmesg:**
```
usb 2-1.3: device descriptor read/64, error -32
usb 2-1-port3: unable to enumerate USB device
```

**Проблема:** USB устройство не опознаётся. Причины:
1. **Плохой USB кабель** к zigbee донглу
2. **Неисправный порт** на хабе
3. **Zigbee донгл подключен не к Orange Pi** (а к ноутбуку или ПК?)
4. **Insufficient power** даже с хабом (если хаб powered, но кабель к донглу тонкий)

**Проверено:**
- Порт 3 не создаёт `/sys/bus/usb/devices/2-1.3/` — устройство не опознаётся вообще
- Reset драйвера (`rmmod ch341 && modprobe ch341`) не помогает
- Полный power cycle порта невозможен (нет sysfs)

---

## 🔧 Действия пользователя

### Телепатический запрос #1: где физически подключен Zigbee донгл?
- **Если к Orange Pi:** попробуйте переподключить в **порт 1 или 3** хаба (порт 2 и 4 заняты ESP)
- **Если powered хаб есть свободные порты:** переподключите zigbee в другой порт
- **Если zigbee подключен к ноутбуку/ПК:** скажите — я настрою Z2M там

### Телепатический запрос #2: работали ли ESP после перезагрузки?
- ttyUSB0 и ttyUSB1 видны — значит ESP под питанием
- Но `cat /dev/ttyUSB0` не дал вывода — возможно ESP уже работают по WiFi (а не шлют логи в UART)
- Если ESP уже прошиты ESPHome и работают — повторная прошивка не нужна

### Действие для Zigbee
```bash
# На Orange Pi:
lsusb  # проверить появился ли zigbee
# Должно быть что-то вроде:
#   ID 1a86:5523 QinHeng   (CH341)
#   ID 0403:6001 FTDI      (FT232)
#   ID 10c4:ea60 Silicon Labs (CP210x)
#   ID 1cf1:0030 Dresden... (ConBee)
```

---

## 📦 ESPHome готов к деплою

```bash
# На Orange Pi:
cd /root/esphome

# Шаг 1: отредактировать secrets.yaml
nano secrets.yaml
# wifi_password: "ваш-пароль"

# Шаг 2: прошить ESP8266 (сначала вынуть один, прошить, потом второй)
esphome run esp-usb-sensor.yaml --device /dev/ttyUSB0

# Шаг 3: прошить ESP32
esphome run esp32-usb-actuator.yaml --device /dev/ttyUSB1
```

**ВАЖНО:** ESPHome `run` с `--device` прошьёт устройство по указанному порту. Убедитесь, что к порту подключен нужный ESP.

---

[[2026-05-14]]
[[Backbone Hub]]
