---
argos_import: project_file
source_path: requirements.iot.txt
source_abs: F:\debug\argoss\requirements.iot.txt
source_ext: .txt
source_sha256: 6f7dbab6d23e5fd3a5ede51dbcac4fd579cfe03715e2cc7a9dea6cfda6b7ee51
text_sha256: 6f7dbab6d23e5fd3a5ede51dbcac4fd579cfe03715e2cc7a9dea6cfda6b7ee51
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# requirements.iot.txt

- Source: `requirements.iot.txt`
- Extract: `text`
- SHA256: `6f7dbab6d23e5fd3a5ede51dbcac4fd579cfe03715e2cc7a9dea6cfda6b7ee51`

## Content

# ARGOS IoT Hub — зависимости
# pip install -r requirements.iot.txt

# ── Все протоколы ─────────────────────────────────────
pyserial>=3.5            # UART: LoRa, SIM800C, RS-485, Modbus RTU
paho-mqtt>=2.0.0         # MQTT: Zigbee, Tasmota, общий брокер

# ── Беспроводные ─────────────────────────────────────
bleak>=0.21.0            # BLE

# ── Промышленные ─────────────────────────────────────
pymodbus>=3.5.0          # Modbus RTU/TCP/ASCII

# ── Датчики ───────────────────────────────────────────
smbus2>=0.4.3            # I2C (BME280, SHT30, ADS1115...)
w1thermsensor>=2.3.0     # 1-Wire DS18B20

# ── NFC ───────────────────────────────────────────────
nfcpy>=1.0.4             # ACR122U, PN532
mfrc522>=0.0.7           # RC522 (RPi SPI)

# ── Умный дом ────────────────────────────────────────
requests>=2.31.0         # Home Assistant REST

# ── IPC ───────────────────────────────────────────────
redis>=5.0.0             # Redis Pub/Sub IPC (опционально)
websockets>=14.0         # WebSocket IPC

# ── RPi ──────────────────────────────────────────────
# RPi.GPIO>=0.7.1        # GPIO: только на Raspberry Pi
# gpiozero>=2.0.1        # GPIO: альтернатива RPi.GPIO

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
