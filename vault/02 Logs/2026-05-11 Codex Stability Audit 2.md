# ARGOS Stability Audit 2 — 2026-05-11

## Дополнительно исправлено
- 	hree_gpu_start.ps1: безопасный 2-GPU режим и запуск через PowerShell 7.
- start_argos_telegram_stable.ps1: вызов GPU-скрипта через pwsh7.
- src/mcp_api.py: fast-path для статус системы через ArgosAdmin.get_stats().
- src/core.py: safe getattr в _auto_providers (устранён тестовый AttributeError).

## Проверка
- pytest: 	ests/test_core_provider_resilience.py + 	ests/test_mcp_fast_ai_status.py → 4 passed.
- MCP статус системы: стабильно < 1 сек.
- MCP обсидиан статус: vault F:\debug\аргос, 100 заметок.
- GPU health: 8082 и 8084 отвечают 200.