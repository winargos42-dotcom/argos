# Email: Почему не отправляется автоматически

**Дата:** 2026-05-06  
**Email:** winargos42@gmail.com  
**Пароль:** [REDACTED — credential removed from repository]

---

## Проблема

ARGOS не может отправить email автоматически, потому что:

1. **Gmail включил 2-Factor Authentication (2FA)**
2. **Обычный пароль блокируется для SMTP**
3. **Требуется App Password (16 символов)** или OAuth2 токен

### Что пробовалось:
- ❌ SMTP_SSL порт 465 — `535 Authentication failed`
- ❌ OAuth2 flow — нет CLIENT_ID/CLIENT_SECRET в .env
- ❌ API Key — Gmail API не поддерживает API Keys для отправки

---

## Решение

Использовать OAuth2 или отдельный App Password, который хранится только в секретах окружения/secret manager и никогда не записывается в Git, логи или MemPalace.

Пример переменных окружения без реального секрета:
```text
SMTP_PASSWORD=<secret-from-runtime>
ARGOS_EMAIL_PASSWORD=<secret-from-runtime>
```

## Политика внешней коммуникации

ARGOS не должен автоматически отправлять письма внешним support/press/company адресатам. По умолчанию допускаются только чтение входящих и подготовка черновика. Фактическая отправка внешнего сообщения требует явного подтверждения владельца. Для каналов, попросивших прекратить прямые обращения, отправка запрещена до явного разрешения получателя.

---

*Автоматическая запись ARGOS; credential redacted 2026-08-10*

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
