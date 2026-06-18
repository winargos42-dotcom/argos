# Попытка отправки Email

**Дата:** 2026-05-06  
**От:** winargos42@gmail.com  
**Кому:** doppol85@gmail.com  
**Статус:** ⚠️ Требуется App Password

## Проблема
Обычный пароль не принимается Gmail:
\\\
535 5.7.8 Username and Password not accepted
\\\

## Решение
Необходимо создать **App Password**:
1. Открыть: https://myaccount.google.com/apppasswords
2. Войти как winargos42@gmail.com
3. Выбрать "Другое (пользовательское имя)" → "ARGOS"
4. Скопировать 16-значный пароль
5. Обновить SMTP_PASSWORD в .env

## Альтернатива
Использовать OAuth2 вместо SMTP (требует настройки в Google Cloud Console)

---
*Автоматическая запись*

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
