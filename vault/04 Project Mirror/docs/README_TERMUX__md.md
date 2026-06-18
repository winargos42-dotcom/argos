---
argos_import: project_file
source_path: docs/README_TERMUX.md
source_abs: F:\debug\argoss\docs\README_TERMUX.md
source_ext: .md
source_sha256: 0f1dc683ad07a8a489f1cf92a105eca86ff2e14e1895594359ee34b72554e1aa
text_sha256: 0f1dc683ad07a8a489f1cf92a105eca86ff2e14e1895594359ee34b72554e1aa
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:59
---

# README_TERMUX.md

- Source: `docs/README_TERMUX.md`
- Extract: `text`
- SHA256: `0f1dc683ad07a8a489f1cf92a105eca86ff2e14e1895594359ee34b72554e1aa`

## Content

# 📱 ARGOS — Установка на Android через Termux

## Быстрый старт (3 шага)

### 1. Установи Termux
Скачай с [F-Droid](https://f-droid.org/packages/com.termux/) (не из Google Play).

### 2. Дай доступ к хранилищу (один раз)
```bash
termux-setup-storage
```

### 3. Запусти установщик
```bash
bash ~/storage/downloads/install_termux.sh
```
Установщик сам найдёт `files (18).zip` в папке Загрузки.

---

## После установки
```bash
source ~/.bashrc          # активировать алиасы
nano ~/argos/.env         # вписать ключи (необязательно)
argos-bot                 # запустить ARGOS
argos-health              # проверка системы
```

## Минимальный .env
```
GEMINI_API_KEY=           # бесплатно: aistudio.google.com
TELEGRAM_BOT_TOKEN=       # @BotFather в Telegram
USER_ID=                  # @userinfobot в Telegram
```

## Частые проблемы
| Проблема | Решение |
|---------|---------|
| Архив не найден | `ls ~/storage/downloads/ grep zip` |
| Python < 3.10 | `pkg install python` |
| Нет хранилища | `termux-setup-storage` |
| Ошибка unzip | `unzip -t ~/storage/downloads/"files (18).zip"` |

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
