---
argos_import: project_file
source_path: docs/quickstart.md
source_abs: F:\debug\argoss\docs\quickstart.md
source_ext: .md
source_sha256: 8690ec23583657c8732c36248d2dd80cf24b1751b2d9a7db2e2fd77f32b6b348
text_sha256: 8690ec23583657c8732c36248d2dd80cf24b1751b2d9a7db2e2fd77f32b6b348
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:59
---

# quickstart.md

- Source: `docs/quickstart.md`
- Extract: `text`
- SHA256: `8690ec23583657c8732c36248d2dd80cf24b1751b2d9a7db2e2fd77f32b6b348`

## Content

# User Guide: Запуск и установка

## 1) Установка зависимостей

```bash
pip install -r requirements.txt

# Установка Ollama (для локального ИИ-режима)
# (рекомендуется сначала просмотреть скрипт install.sh)
curl -fsSL https://ollama.com/install.sh | sh
```

Для голосовых функций также могут понадобиться системные пакеты (например, PortAudio).

## 2) Настройка окружения

Создай `.env` в корне проекта и укажи минимально необходимые ключи:

```env
GEMINI_API_KEY=...
ARGOS_NETWORK_SECRET=...
```

Если используешь Telegram и Home Assistant — добавь соответствующие переменные из README.

## 3) Инициализация и запуск

```bash
python genesis.py
python main.py
bash launch.sh       # по умолчанию запускает полную конфигурацию (--full)
```

Режимы запуска:

- Desktop: `python main.py`
- Headless: `python main.py --no-gui`
- Dashboard: `python main.py --dashboard`
- Full configuration: `python main.py --full`

## 4) Первые команды

- `статус системы`
- `что ты знаешь`
- `найди в памяти кот`
- `граф знаний`
- `запусти p2p`

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
