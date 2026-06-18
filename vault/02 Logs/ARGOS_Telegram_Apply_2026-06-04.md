# ARGOS — применение моментов из Telegram-сессии — 2026-06-04

## Источник
Telegram-экспорт `ChatExport_2026-06-04/messages.html` (248K символов, сессия с
Hermes-ботом ddgermesa_bot, 3-4 июня). Прочитан полностью.

## Важные моменты, выделенные из чата
| # | Момент | Где | Статус |
|---|--------|-----|--------|
| 1 | WhatsApp-бот молчит (whatsapp-web.js "заморозка", messages_processed:0) | J:\Projects\whatsapp-bot-v2 (Orion) | 🔧 фиксы подготовлены |
| 2 | OSINT-разведка: 17 поисковиков в ARGOS | ~/.hermes (ноутбук) | ⏳ не на Orion |
| 3 | Hermes compression: модель <64K блокирует | ~/.hermes/config.yaml (ноутбук) | ❌ не мой доступ |
| 4 | MCP ARGOS реальный = :8002 (mcp_api.py), не :8000 заглушка | Orion/ноутбук | ✅ работает |
| 5 | GPU-кластер OLLAMA_GPU_MODE=off | Orion | 🟡 задача |

## Что сделано (WhatsApp-бот, #1)
ПРОВЕРКА показала: фиксы из чата НЕ долетели до финального кода на Orion
(Hermes правил в /tmp на ноутбуке). В J:\Projects\whatsapp-bot-v2 был СТАРЫЙ код:
- `.env`: OWNER_NUMBER=15823226024 (НЕ обновлён на твой 79622863323) → бот игнорил твои сообщения
- `.env`: HEALTH_PORT=9001 (занят MinIO!) → health не поднимался
- `index.js`: headless:true + --single-process → Chromium засыпал ("заморозка")
- нет heartbeat, нет handleSIGINT:false

БЛОКЕР: J:\Projects принадлежит BUILTIN\Администраторы, у AvA нет прав записи,
icacls без админа не проходит (Access denied). Прямая запись невозможна.

РЕШЕНИЕ: исправленные файлы подготовлены в `F:\debug\argoss\_wa_fix\`:
- `index.js` — puppeteer headless:'new', убраны single-process/no-zygote/disable-gpu,
  добавлены anti-backgrounding флаги, handleSIGINT/TERM/HUP:false, SIGHUP-обработчик
- `.env` — OWNER_NUMBER=79622863323, HEALTH_PORT=9003, PING_INTERVAL_MS=30000
- `apply.ps1` — скрипт применения (бэкап → копия → очистка сессии → запуск → health)

## Применить (нужен Администратор — J: под админ-ACL)
```powershell
powershell -ExecutionPolicy Bypass -File F:\debug\argoss\_wa_fix\apply.ps1
```
Скрипт: остановит бота → бэкап index.js/.env → применит фиксы → очистит старую
сессию (была на старый номер) → запустит на :9003 → покажет health.
Дальше: QR из data\boot.log → сканировать с телефона → /ping боту с +7 962-286-33-23.

## Статус
- [x] Telegram-чат прочитан полностью, важные моменты выделены
- [x] WhatsApp-бот: причина молчания найдена (фиксы не применены + старый номер/порт)
- [x] Фиксы подготовлены в F:\_wa_fix\ + apply.ps1
- [ ] Применить apply.ps1 от админа (J: под админ-ACL — сам не могу)
- [ ] OSINT (#2), GPU (#5) — отдельные задачи
