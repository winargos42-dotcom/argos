# ARGOS Stability Audit — 2026-05-11

## Что исправлено
- MCP fast-path: команда статус системы теперь обрабатывается без LLM и без таймаутов.
- Core warmup: добавлен флаг GPU_SERVER_1_ENABLED, GPU1 (Vega11) можно отключать без спама ошибок.
- Knowledge routing: для изучи ... с фокусом на Obsidian больше нет ухода в web/LLM при пустом результате.
- Launcher: start_argos_telegram_stable.ps1 запускает GPU-скрипт через PowerShell 7.
- GPU launcher: 	hree_gpu_start.ps1 адаптирован под 2-GPU стенд (RX580 + RX560), порт 8083 пропускается если нет 3-го Vulkan устройства.

## Проверка
- MCP: http://127.0.0.1:8000/health = 200
- GPU: 8082 = OK, 8084 = OK
- Команда статус системы отвечает ~0.5s
- Команда мульти провайдер чат отвечает стабильно
- Obsidian: vault = F:\debug\аргос, заметок = 100

## Текущий контур
- AI mode: auto / consensus ON
- MCP: порт 8000
- Dashboard: порт 8090
- Локальные GPU: RX580 (8082), RX560 (8084)