# Email: Почему не отправляется автоматически

**Дата:** 2026-05-06  
**Email:** winargos42@gmail.com  
**Пароль:** sigtrip1464 (пароль от Google аккаунта)

---

## Проблема

ARGOS не может отправить email автоматически, потому что:

1. **Gmail включил 2-Factor Authentication (2FA)**
2. **Обычный пароль (sigtrip1464) блокируется для SMTP**
3. **Требуется App Password (16 символов)** или OAuth2 токен

### Что пробовалось:
- ❌ SMTP_SSL порт 465 — `535 Authentication failed`
- ❌ OAuth2 flow — нет CLIENT_ID/CLIENT_SECRET в .env
- ❌ API Key — Gmail API не поддерживает API Keys для отправки

---

## Решение (только ручное)

### Вариант A: Создать App Password (2 минуты)
1. Открыть: https://myaccount.google.com/apppasswords
2. Войти как **winargos42@gmail.com** с паролем **sigtrip1464**
3. Выбрать **Другое** → ввести "ARGOS"
4. Скопировать **16-значный код** (например: `abcd efgh ijkl mnop`)
5. Обновить `.env`:
   ```
   SMTP_PASSWORD=abcd efgh ijkl mnop
   ARGOS_EMAIL_PASSWORD=abcd efgh ijkl mnop
   ```
6. Перезапустить ARGOS

### Вариант B: Отключить 2FA (не рекомендуется)
1. https://myaccount.google.com/signinoptions/two-step-verification
2. Выключить 2FA
3. Тогда обычный пароль заработает

---

## Альтернатива без Gmail

Если нужна полная автоматизация, лучше использовать:
- **SendGrid** — API ключ, без OAuth
- **Mailgun** — API ключ
- **AWS SES** — Access Key

---

*Автоматическая запись ARGOS*

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
