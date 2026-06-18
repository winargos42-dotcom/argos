---
type: agent
name: Autonomous Brain
location: laptop
status: running
---

# Autonomous Brain

## Файл
`~/Projects/argoss/scripts/autonomous_brain.py`

## Цикл (10 минут)
1. CPU/RAM/temp метрики
2. Статус нод P2P + ESP устройства
3. HA entities через API (токен в .env)
4. Принятие решений + cooldown ha_check 1ч
5. Выполнение команд через MQTT
6. Heartbeat → argos/heartbeat
7. Отчёт → Daily/YYYY-MM-DD-brain.md

## Исправления (2026-05-15)
- check_url body limit: 500 → 5MB (HA API = 42KB)
- except → {"ok": False} (ранее было {"ok": True} без active)
- cooldown 3600s для ha_check

## MQTT топики
- Публикует: argos/heartbeat, argos/log, argos/command
- Подписан: argos/command, argos/agents/brain/inbox

[[AGENTS]]
