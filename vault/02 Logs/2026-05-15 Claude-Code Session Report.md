# 2026-05-15 — Отчёт Claude Code сессии

## Zigbee2MQTT
### OPi (192.168.2.168)
- **Адаптер**: ZB-GW04 v1.2 (EFR32MG21) → `/dev/ttyUSB0` (прямое подключение)
- **Тип**: `ember` (EmberZNet 7.4.5)
- **Топик MQTT**: `zigbee2mqtt/bridge/state`
- **Frontend**: :8099 → `z2m.argosssss.win`
- **Статус**: ✅ running

### ПК (192.168.1.66)
- **Адаптер**: CC2531 → COM14 (ZStack)
- **Топик MQTT**: `zigbee2mqtt_pc/bridge/state`
- **Frontend**: :8100
- **Статус**: started via SSH

## Brain fix
`check_url` body limit: 500 → 5MB. HA active_entities баг устранён.
Brain: ARGOS_AI_PRIORITY=kimi,deepseek (только облако)

## Cloudflare
- `ssh-pc.argosssss.win` ← новый маршрут
- `brain-pc.argosssss.win` ← новый маршрут
- `z2m.argosssss.win` ← новый маршрут

[[Backbone Hub]]
