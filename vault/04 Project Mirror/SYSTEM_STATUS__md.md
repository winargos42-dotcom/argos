---
argos_import: project_file
source_path: SYSTEM_STATUS.md
source_abs: F:\debug\argoss\SYSTEM_STATUS.md
source_ext: .md
source_sha256: 02aa3ec0224b444370615bbd0f6a88d1fcb6c128f18bd7273345581482f31102
text_sha256: 02aa3ec0224b444370615bbd0f6a88d1fcb6c128f18bd7273345581482f31102
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# SYSTEM_STATUS.md

- Source: `SYSTEM_STATUS.md`
- Extract: `text`
- SHA256: `02aa3ec0224b444370615bbd0f6a88d1fcb6c128f18bd7273345581482f31102`

## Content

# ARGOS System Configuration Save
# Generated: 2026-04-23
# Version: 2.1.3

## Статус системы

### GPU Кластер (3/3 активны)
- GPU0 (RX 580):  http://localhost:8082 - qwen2.5:3b - ✅
- GPU1 (Vega 11): http://localhost:8083 - tinyllama - ✅
- GPU2 (RX 560):  http://localhost:8084 - phi4-mini - ✅

### AI Режим
- ARGOS_AI_MODE=ollama
- ARGOS_AI_PRIORITY="local-gpu,local-ollama,vm-cluster,azure"

### Сервисы
- Brain API:   http://localhost:5010 - ✅
- MCP:         http://localhost:8000 - ✅
- Compute:     http://localhost:8002 - ✅
- Redis:       localhost:6379 - ✅
- Ollama:      http://localhost:11434 - ✅
- Dashboard:   http://localhost:8080 - ✅

### Image Generation Провайдеры
1. z_turbo - Z-Image-Turbo (HF Space API)
2. animagine - Animagine XL 4.0 (HF Space API)
3. paperbanana - PaperBanana (HF Space API)
4. flux_dev - FLUX.1-dev (локальная GGUF)
5. flux_dedistilled - FLUX.1-Dev DedistilledMixTuned V3
6. longcat_image - LongCat-Image (API)
7. black_magic_flux - BLACK-MAGIC-FLUX (локальная)
8. tongyi_z_image - Tongyi Z-Image (локальная)

### WireGuard Mesh
- AU:  10.200.0.1 - ✅
- JP1: 10.200.0.2 - ✅
- JP2: 10.200.0.3 - ✅
- SE:  10.200.0.4 - ⚠️ Требует настройки
- EXT: 10.200.0.5 - ✅
- PC:  10.200.0.6 - ✅ (Local)

### Добавленные модели
- FLUX.1-dev Q8
- FLUX.1-Dev DedistilledMixTuned V3
- BLACK-MAGIC-FLUX
- LongCat-Image
- Tongyi Z-Image
- Z-Image-Turbo
- Animagine XL 4.0
- PaperBanana

## Созданные файлы

1. argos_watchdog.ps1 - Мониторинг системы
2. watchdog_auto.bat - Автозапуск watchdog
3. watchdog_menu.bat - Интерактивное меню
4. setup_comfyui.ps1 - Установка ComfyUI
5. scripts/download_image_models.py - Загрузка моделей
6. test_image_gen.py - Тестирование генерации
7. wg/setup_se_wg_final.sh - Настройка SE VM
8. wg/setup_se_wg.sh - Альтернативная настройка SE
9. wg/README_SE_FIX.md - Инструкция по SE
10. fix_bugs.sh - Исправление багов

## Интеграция Dashboard
- ✅ Добавлена кнопка "TASK DASHBOARD" (/dashboard)
- ✅ Добавлена кнопка "FREE APIs" (/apis)
- ✅ Добавлен роутинг в web_dashboard.py

## Скрипты запуска
- start_argos.bat - Обновлён для запуска web_dashboard.py

## Требует действий
1. Запустить: python scripts/download_image_models.py
2. Установить ComfyUI: .\setup_comfyui.ps1
3. Настроить SE VM через Azure Portal
4. Перезапустить браузер с Ctrl+F5 для обновления dashboard

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
