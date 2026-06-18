---
argos_import: project_file
source_path: BACKUP_CONFIGS.md
source_abs: F:\debug\argoss\BACKUP_CONFIGS.md
source_ext: .md
source_sha256: 6f8d8c8486eb8e376c06d981ab5f8bdb30e5f5827b707a3652e70a49179fd71b
text_sha256: 6f8d8c8486eb8e376c06d981ab5f8bdb30e5f5827b707a3652e70a49179fd71b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# BACKUP_CONFIGS.md

- Source: `BACKUP_CONFIGS.md`
- Extract: `text`
- SHA256: `6f8d8c8486eb8e376c06d981ab5f8bdb30e5f5827b707a3652e70a49179fd71b`

## Content

# ARGOS System Backup - 2026-04-23
# Все конфигурации сохранены локально

## Работающие компоненты

### GPU Кластер (3/3)
- GPU0 (RX 580): http://localhost:8082 - qwen2.5:3b
- GPU1 (Vega 11): http://localhost:8083 - tinyllama  
- GPU2 (RX 560): http://localhost:8084 - phi4-mini

### AI Mode
- ARGOS_AI_MODE=ollama
- ARGOS_AI_PRIORITY="local-gpu,local-ollama,vm-cluster,azure"
- OLLAMA_HOST=http://localhost:11434

### Сервисы
- Brain API: http://localhost:5010
- MCP: http://localhost:8000
- Redis: localhost:6379
- Ollama: http://localhost:11434
- Dashboard: http://localhost:8080

## Сохраненные файлы

### 1. Watchdog (мониторинг)
- argos_watchdog.ps1 - Основной скрипт
- watchdog_auto.bat - Автозапуск каждые 5 мин
- watchdog_menu.bat - Интерактивное меню

### 2. Image Generation
- src/skills/image_gen.py - 10 провайдеров
- test_image_gen.py - Тестирование
- scripts/download_image_models.py - Загрузчик

### 3. ComfyUI
- setup_comfyui.ps1 - Установщик
- comfyui/ - Директория установлена

### 4. Dashboard
- src/interface/web_dashboard.py - Обновлен
- argos_free_apis.html - Каталог API
- dashboard.html - Task Dashboard
- start_argos.bat - Обновлен

### 5. WireGuard
- wg/setup_se_wg_final.sh - Настройка SE VM
- wg/README_SE_FIX.md - Инструкция

## Команды запуска

```powershell
# Полный запуск
.\start_argos.bat

# Только дашборд
python src/interface/web_dashboard.py

# Watchdog
.\watchdog_auto.bat

# Проверка GPU
python -c "import requests; [print(f'Port {p}: OK') if requests.get(f'http://localhost:{p}/health', timeout=3).ok else print(f'Port {p}: FAIL') for p in [8082,8083,8084\]\]"
```

## Проблемы и решения

### Ollama на CPU (не GPU)
Windows Ollama НЕ поддерживает AMD GPU.
Решение: Использовать llama-server (уже запущен на портах 8082-8084)

### Telegram бот конфликт
[TG-BRIDGE]: Конфликт polling
Решение: Запущен только один экземпляр

### Gemini отключен
API key expired
Решение: Обновить ключ или использовать Ollama

## Прямые ссылки

- Dashboard: http://localhost:8080
- Task Dashboard: http://localhost:8080/dashboard  
- Free APIs: http://localhost:8080/apis
- Brain API: http://localhost:5010
- MCP: http://localhost:8000
- GPU 0: http://localhost:8082
- GPU 1: http://localhost:8083
- GPU 2: http://localhost:8084

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
