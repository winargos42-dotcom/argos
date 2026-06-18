---
argos_import: project_file
source_path: reports/Новый текстовый документ.txt
source_abs: F:\debug\argoss\reports\Новый текстовый документ.txt
source_ext: .txt
source_sha256: 64ec3f0a0a4ac9bc241a94141eb06ce75e00cd3755060c13af62423081c32903
text_sha256: 807dd374e7df4869867fcbbea16fb8d2ec616dfd4bbd3c8def4c6129baf19afe
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:26
---

# Новый текстовый документ.txt

- Source: `reports/Новый текстовый документ.txt`
- Extract: `text`
- SHA256: `64ec3f0a0a4ac9bc241a94141eb06ce75e00cd3755060c13af62423081c32903`

## Content

#!/bin/bash
# tts_commands.sh - Команды для работы с TTS модулем ARGOS

# === Инициализация ===
# Запуск TTS сервера
./arg os tts start

# Проверка статуса
./arg os tts status

# Остановка
./arg os tts stop

# === Управление голосом ===
# Установить голос (示例: ru-RU, en-US)
./arg os tts voice set ru-RU

# Регулировка скорости (0.5 - 2.0)
./arg os tts speed 1.0

# Регулировка высоты тона
./arg os tts pitch 0.0

# === Синтез речи ===
# Озвучить текст
./arg os tts speak "Привет, я ARGOS"

# Сохранить в файл
./arg os tts save "Текст для записи" output.wav

# Озвучить файл
./arg os tts play input.wav

# === Мониторинг ===
# Логи TTS
./arg os tts logs

# Статистика использования
./arg os tts stats

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
