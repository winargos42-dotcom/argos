---
argos_import: sharedmemory_mirror
source_path: Ngrok_Setup_Report.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\Ngrok_Setup_Report.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: Ngrok_Setup_Report.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\Ngrok_Setup_Report.md`
- Category: [[SharedMemory Hub]]

## Content

# Отчет о настройке ngrok туннеля для Ollama в рамках проекта ARGOS

**Дата:** 2026-05-08  
**Время:** после проверки доступности через ngrok

## Что сделано

1. **Проверен существующий ngrok туннель**
   - Туннель уже был запущен и активен через systemd пользовательский сервис `ngrok.service`.
   - Статус сервиса: active (running).
   - Публичный URL: `https://myollama123.ngrok.io`.
   - Проверка доступа: `curl -s https://myollama123.ngrok.io/api/tags` возвращает JSON со списком моделей (llama3.1:8b).

2. **Обновлена конфигурация проекта ARGOS**
   - Файл: `/home/ava/Projects/argoss/.env`
   - Изменено:
     - `OLLAMA_HOST` с `http://localhost:11434` на `https://myollama123.ngrok.io`
     - `OLLAMA_ENABLED` с `false` на `true`
   - Это заставляет ARGOS использовать удаленный Ollama через ngrok туннель вместо локального экземпляра.

3. **Проверено, что туннель обходит ограничения сети**
   - Ранее Cloudflare туннель не работал из-за блокировки UDP/QUIC между Windows хостом и WSL2.
   - ngrok использует TCP/HTTPS (порт 443), что обычно не блокируется, обеспечивая связь между ноутбуком (где находится пользователь) и ПК (где запущен Ollama в WSL2).

## Текущее состояние

- **ngrok туннель:** активен, публичный URL `https://myollama123.ngrok.io`.
- **Ollama доступен:** через указанный URL возвращает список моделей.
- **ARGOS конфигурация:** обновлена для использования удаленного Ollama (`OLLAMA_ENABLED=true`).
- **Связь ноутбук ↔ ПК через интернет:** подтверждена работоспособностью ngrok туннеля.

## Следующие шаги

- При необходимости перезапустить ARGOS (main.py или связанные сервисы), чтобы он подхватил новые переменные окружения.
- Мониторинг логов ngrok при необходимости: `journalctl --user -u ngrok.service -f`.
- Если понадобится изменить поддомен или параметры туннеля, отредактировать `/home/ava/.ngrok2/ngrok.yml` и перезапустить сервис.
- Рассмотреть добавление базовой аутентификации или ограничения IP в дашборде ngrok для повышения безопасности.

## Примечание

Все действия выполнены в среде WSL2 (Linux) на ПК с Arch Linux. ngrok клиент запущен в той же среде, туннель направлен на `localhost:11434` внутри WSL2, где запущен Ollama.

*Отчет сохранен в Obsidian vault SharedMemory и будет синхронизирован с ПК в течение 2 минут.*

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[SharedMemory Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `Ngrok_Setup_Report.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[SharedMemory Hub]]
