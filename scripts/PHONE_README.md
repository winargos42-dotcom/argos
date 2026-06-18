# 📱 ARGOS Phone Manager

## Быстрый старт

```bash
# Показать статус всех телефонных агентов
python3 scripts/phone_manager.py status

# Список агентов
python3 scripts/phone_manager.py list

# Скриншот экрана телефона
python3 scripts/phone_manager.py screenshot

# Статус батареи
python3 scripts/phone_manager.py battery

# Отправить команду на телефон (ADB)
python3 scripts/phone_manager.py cmd "input keyevent KEYCODE_HOME"
python3 scripts/phone_manager.py cmd "input tap 500 1000"
python3 scripts/phone_manager.py cmd "am start -a android.intent.action.VIEW -d https://t.me/argos_entity_council"
```

## Агенты на телефоне

| Агент | Файл | Описание |
|-------|------|----------|
| phone-redmi | colibri_phone.py | P2P / Brain API heartbeat |
| phone-v2 | argos_phone_v2.py | HTTP сервер :7788 (screenshot, cmd) |
| phone-subject | argos_phone_subject.py | Наблюдатель / мысли для сущностей |
| root-agent | argos_root_agent.py | Root управление системой |
| avangard | argos_autogpt.py | AutoGPT циклы (Observe→Think→Act) |
| consciousness | argos_stub_agent.py | Сознание (heartbeat stub) |
| business | argos_stub_agent.py | Бизнес (heartbeat stub) |

## HTTP API телефона (:7788)

```bash
# Статус
curl http://192.168.1.149:7788/status

# Скриншот
curl http://192.168.1.149:7788/screenshot -o screen.png

# Команда
curl -X POST http://192.168.1.149:7788/cmd \
  -H "Content-Type: application/json" \
  -d '{"cmd": "input tap 500 1000"}'
```

## Brain API регистрация

Агенты отправляют heartbeat на `http://192.168.1.66:5010/brain/heartbeat`.

Через phone_manager.py можно управлять запуском/остановкой.
