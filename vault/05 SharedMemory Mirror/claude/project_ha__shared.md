---
argos_import: sharedmemory_mirror
source_path: claude/project_ha.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_ha.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_ha.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_ha.md`
- Category: [[Claude Hub]]

## Content

---
name: Home Assistant интеграция
description: HA на ноутбуке X230, интеграция с ARGOS через smart_environments skill
type: project
created: 2026-05-10
originSessionId: 07f7f1bc-6a4f-49cb-aca5-c0efa4942a8e
---
## Расположение
- **Хост:** X230 ноутбук (192.168.1.53:8123)
- **Docker:** `ghcr.io/home-assistant/home-assistant:stable`
- **Путь конфига:** `/home/ava/homeassistant`

## Доступ из ARGOS (ПК)
- HA_URL: `http://192.168.1.53:8123`
- HA_TOKEN: JWT в `.env` (iss: c1b0d8177d4644dc9c8bb88fb3ed8dce, exp: 2093)
- HA_MQTT_HOST: `192.168.1.53:1883`

## Сущности (72 на 2026-05-10)
| Домен | Кол-во | Примеры |
|-------|--------|---------|
| sensor | 25 | CPU/RAM ноутбука, Orange Pi, роутер, погода |
| switch | 12 | дом Switch 1-4, smart switch 4ch |
| scene | 9 | кухня, зал, Turn off all switches |
| binary_sensor | 7 | WAN роутера, Zigbee bridge, дверь, клапан |
| conversation | 3 | HA, ARGOS Ollama x2 |
| event | 3 | кнопки Zigbee |
| select | 3 | Zigbee log level |
| climate | 1 | пол (heat_cool) |
| light | 1 | дом Подсветка |
| weather | 1 | partlycloudy |

## Интеграция ARGOS ↔ HA
- `src/connectivity/home_assistant.py` — HomeAssistantBridge (REST API + MQTT + IoT-бридж)
- `src/skills/smart_environments.py` — handle() обрабатывает "home assistant статус"
- `src/core.py` → `_init_home_assistant()` — при старте подключает HA как IoT-бридж
- Триггеры: "home assistant", "ha статус", "ha сущности", "домашний ассистент"

## Zigbee устройства
- Хаб (Zigbee2MQTT bridge) — состояние: off (нужно запустить)
- Датчик двери
- Тёплый пол (climate, клапан)
- Кнопки (Powerful button)
- Умный свет (дом Подсветка)
- Smart switch 4ch

## Что сделано (2026-05-10)
- [x] HA_URL в .env → 192.168.1.53 (было localhost)
- [x] HA_MQTT_HOST → 192.168.1.53
- [x] HomeAssistantBridge: добавлены get_value(), send_command(), get_entity(), list_entities_summary()
- [x] smart_environments.py: добавлены HA триггеры и _handle_ha_command()
- [x] core.py: HA бридж подключается к SmartEnvironmentManager как IoT-бридж
- [x] Тест: 72 сущности читаются с ПК → ноутбук API OK

## TODO
- [ ] Запустить Zigbee2MQTT bridge (сейчас off)
- [ ] Маппинг HA entity_id → SmartEnvironment device_id для автоматического мониторинга
- [ ] Cloudflare туннель: `ha.argosssss.win → :8123`
- [ ] Автоматизации через ARGOS Telegram бот (включи свет, покажи температуру)

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_ha.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
