# AI Session Log — 2026-05-14
## Vault Audit + ARGOS ROM Guide

**Агент:** pi-coding-agent (Claude 4)  
**Пользователь:** AvA  
**Длительность:** ~2 часа  
**Vault:** `/home/ava/Projects/argoss/vault`

---

## 🔍 Выполненные операции

### 1. Изучение структуры vault'а
- Найдены 2 хранилища: `/home/ava/Obsidian Vault/` и `/home/ava/Projects/argoss/vault/`
- Основной рабочий — `argoss/vault` (PARA-структура: 01 Projects, 02 Logs, 03 Memory, 05 SharedMemory Mirror)
- Обнаружено дублирование: файлы из `02 Logs/` продублированы внутри `.obsidian/02 Logs/` — вероятно, баг скрипта `vault-sync.sh`

### 2. Анализ файлов, созданных 2026-05-14
Изучены 9 заметок (всего ~60 KB):
- `2026-05-14.md` — Daily Note: ESP8266→ESPHome, Cloudflare AI fix, P2P heartbeat, Orange Pi WiFi
- `SERVER.md` — конфиг ПК (IP .66, RX 580+560, Ollama 9 моделей)
- `02 Logs/` — 7 логов: ANDRAX v5, ARGOS FULL PACK, Final Status Audit, Post-Reboot, Phone Install, KolibriOS+Colibri, Android Multi-Tool

### 3. Создание новой заметки
**`2026-05-14 ARGOS Multi-Tool ROM — Colab Build Guide.md`**
- Полный гайд по сборке LineageOS 21 + ARGOS overlay в Google Colab
- 10 code cells (init, sync, device trees, overlay, Magisk, build)
- Таблица prebuilt APK (Andrax, Termux suite, ARGOS Universal, F-Droid)
- Инструкция по флешингу через fastboot + adb sideload

### 4. Проблемы выявленные
| Проблема | Приоритет | Решение |
|----------|-----------|---------|
| Дубли в `.obsidian/02 Logs/` | ⚠️ Средний | Удалить `.obsidian/02 Logs/`, проверить `vault-sync.sh` |
| Keystone-engine на ARM | ⚠️ Низкий | Assembly = PC-only; disassembly = capstone ✅ |
| Zigbee2MQTT без донгла | ⚠️ Средний | Купить Zigbee USB coordinator |
| Orange Pi без WiFi | ⚠️ Средний | USB WiFi dongle |

---

## 🔗 Новые связи в графе
- `[[ARGOS Multi-Tool ROM — Colab Build Guide]]` → связывает все логи ginkgo в единый трек
- `[[Backbone Hub]]` — центральный узел для навигации

---

## 📝 Методология
- Все правки через `write`/`edit` — безопасно для Markdown
- Поиск через `bash find` + `read` — анализ перед изменением
- Структура следует существующему naming convention (`YYYY-MM-DD Тема.md`)

[[Backbone Hub]]

---

## 🔄 Продолжение сессии — Cleanup + Sync Fix + Integrations

**Длительность:** +~2 часа (итого ~4 часа)  
**Запрос пользователя:** «вспомни все», очистить дубли, починить синхронизацию, запустить всё на Windows ПК

---

### 5. Полная очистка дублей — ✅
- **Найдено**: `.obsidian/` содержал полную копию vault'а (2640 .md файлов + все директории)
  - `00 Memory Web`, `01 Projects`, `02 Logs`, `03 Memory`, `04 Project Mirror`, `05 SharedMemory Mirror`, `06 Link Stubs`, `07 Duplicates Archive`, `Daily`, `Excalidraw`
- **Удалено**: ВСЕ дубли, сохранены только настоящие системные файлы: `plugins/` + `snippets/`
- **Root cause**: `sync-obsidian-memory.py` не исключал `.obsidian/` из списка файлов для синхронизации

### 6. Синхронизация починена — ✅

**`sync-obsidian-memory.py` v2:**
- `exclude = {".obsidian", ".git"}`
- Проверка `parts` на любой глубине вложенности

**`vault-sync.sh` v2:**
- `guard_path()` — fatal error если путь содержит `.obsidian/` или `.git/`
- `flock -n` — предотвращает concurrent runs через lockfile `/tmp/vault-sync.lock`

### 7. Spaced Repetition — запущено на Windows ПК — ✅

**Target:** `F:\debug\аргос\.obsidian\plugins\obsidian-spaced-repetition\`

- **main.js**: 2,422,329 bytes
- **manifest.json**: 449 bytes  
- **styles.css**: 25,641 bytes
- **Plugin**: `obsidian-spaced-repetition` v1.13.9 by st3v3nmw
- **Скрипт**: `scripts/argos_install_spaced_repetition.sh` (bash) + PowerShell wrapper для Windows
- **Status**: Установлен, требует restart Obsidian + enable в Community plugins

### 8. Mini-Tron-50 + русская классика — в процессе деплоя на Windows ПК — 🔄

**Model**: `Imperius/mini-tron-50` (50M params, NanoGPT/GPT-2 архитектура)
**Downloaded on laptop**: 129 MB `pytorch_model.bin` + tokenizer/configs
**Transfer to Windows**: SCP в фоне (PID 759073, 119 MB tarball)
**Windows script**: `argos_setup_mini_tron_windows.ps1`
  - Скачивает модель с HF (fallback если tarball ещё не доехал)
  - Создаёт Modelfile для Ollama
  - Регистрирует как `argos-classic`

**System prompt** (русская классика):
> «Ты — русскоязычный ассистент ARGOS, обученный на классической литературе. Говоришь ёмко, образно, с долей иронии.»

**ML Stack** (установлен 13.05.2026 на laptop):
- pip: torch, transformers, opencv, ultralytics, spacy, nltk, xgboost, catboost, lightgbm, langchain, llamaindex...
- pacman: python-pytorch, python-tensorflow, qemu-full, lxc, dnsmasq...
- yay: python-langchain, waydroid...

### 9. Новые заметки vault'а
- `02 Logs/2026-05-14 ARGOS Spaced Repetition + Mini-Tron-50 Integration.md`
- Обновлён `2026-05-14.md` — добавлены секции 6–9

### 10. Новые скрипты
| Скрипт | Назначение |
|--------|-----------|
| `scripts/argos_install_spaced_repetition.sh` | Установка SR плагина |
| `scripts/argos_setup_mini_tron.sh` | Сетап mini-tron-50 (Linux) |
| `scripts/argos_setup_mini_tron_windows.ps1` | Сетап mini-tron-50 (Windows) |

---

## 📊 Итоговый статус деплоя на Windows ПК (argos-pc)

| Компонент | Статус | Примечание |
|-----------|--------|------------|
| SR Plugin файлы | ✅ | В `.obsidian/plugins/obsidian-spaced-repetition/` |
| SR Plugin активен | ⏳ | Нужен restart Obsidian + enable |
| Mini-Tron-50 модель | 🔄 | Скачана на laptop, SCP в пути на Windows |
| Mini-Tron-50 GGUF | ❌ | Конвертация требует llama.cpp (WSL или PC) |
| Mini-Tron-50 Ollama | ❌ | Ждёт GGUF + `ollama create argos-classic` |

## 📝 Методология (обновлено)
- Windows деплой: PowerShell через SSH + SCP для бинарников
- Bash-скрипты: через WSL или PowerShell `-File`
- Фоновые передачи: `nohup scp ... > log 2>&1 &`
- Проблема: медленный интернет к HF/GitHub с Linux-окружения (~300 KB/s)

[[Backbone Hub]]
