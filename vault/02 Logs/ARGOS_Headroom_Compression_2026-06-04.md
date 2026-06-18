# ARGOS — Headroom Compression интегрирован в MCP — 2026-06-04

## Источник
Hermes-бот создал skill на ноутбуке: `~/.hermes/skills/headroom-compression/`
(argos_compressor.py, argos_mcp_compression.py, headroom_mcp_handler.py, SKILL.md).
Доступ через `ssh argos-laptop` (настроен сегодня).

## Проверка реальности (не на слово)
- Файлы реальны, argos_compressor.py 391 строк, классы ArgosCompressor/ArgosMCPMiddleware.
- Функциональный тест на ноутбуке: 5363→738 символов (87%).
- Скопировано на Orion: `F:\debug\argoss\scripts\headroom\` (3 .py + spec).
- Тест на Orion: 21764→1357 символов = **93.76% экономии** (стратегия json_array).
- Малые входы (<лимит) → passthrough (не сжимает) — корректное поведение.
- API: `ArgosCompressor().compress(text)` → CompressResult(.text, .strategy,
  .original_chars, .compressed_chars, .savings_pct, .ratio, .stats).

## Интеграция в ARGOS MCP (src/mcp_api.py)
Добавлено в 3 местах:
1. tools list — определение `headroom_compress` (после status, ~916) с inputSchema {text}.
2. обработчик — `elif name == "headroom_compress"` → self._headroom_compress (~1457).
3. метод `_headroom_compress(text)` — импортит scripts/headroom/argos_compressor,
   возвращает заголовок [headroom: strategy, N→M символов, экономия X%] + сжатый текст.

## Проверка
- `py_compile src/mcp_api.py` → ✓
- Метод: 14280→1107 символов = 92% на тестовом JSON-массиве.

## Статус
- [x] Файлы компрессора проверены и скопированы на Orion (scripts/headroom/)
- [x] headroom_compress интегрирован в ARGOS MCP (mcp_api.py)
- [x] Компилируется, метод работает (92-94% сжатия на больших outputs)
- [x] ARGOS перезапущен (loader_test=LOADER_SURVIVED, поднялся за ~75с) — tool В ЖИВОМ MCP
- [x] Живой вызов tools/call headroom_compress: 5823→968 символов, 83% ✓

## Рестарт ARGOS 2026-06-05
- loader_test → LOADER_SURVIVED (без segfault) → рестарт безопасен.
- main.py --no-gui перезапущен, :8000 поднялся за ~75с (skills загружены).
- tools/list: 33 tools (было 31) — добавились headroom_compress + osint.
- Живые вызовы: headroom_compress работает (83% сжатие), osint работает.
- hc.py обёртка (scripts/headroom/hc.py) — для сжатия больших выводов в работе.

## Что даёт
ARGOS MCP теперь умеет сжимать большие tool outputs (providers, terminal, логи, JSON)
на 90%+ через headroom_compress — экономия контекста для агентов.
Файлы: scripts/headroom/*, src/mcp_api.py (tool headroom_compress).
