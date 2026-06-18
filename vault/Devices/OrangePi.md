---
type: device
name: Orange Pi One
ip: 192.168.2.168
---

# Orange Pi One

## Доступ
```bash
ssh root@192.168.2.168           # локально
ssh orangepi-tunnel              # Cloudflare
ssh-orangepi.argosssss.win       # через туннель laptop
```

## Z2M управление
```bash
systemctl status zigbee2mqtt
systemctl restart zigbee2mqtt
journalctl -u zigbee2mqtt -f
```

## Конфиг Z2M
`/opt/zigbee2mqtt/data/configuration.yaml`
- adapter: **ember** (НЕ zstack, НЕ ezsp)
- port: /dev/ttyUSB0
- MQTT: 192.168.1.53:1883

## Отчёты
`/home/ava/argos-reports/`

[[AGENTS]] | [[OrangePi STATUS→|../../../SharedMemory/orangepi/STATUS]]
