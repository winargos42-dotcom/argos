# Настройка Gmail App Password для ARGOS

## Статус
- OAuth2: ❌ Заблокирован Google (403 access_denied)
- App Password: 🔄 Требуется настройка

## Инструкция

### 1. Включи 2FA (обязательно)
- https://myaccount.google.com/signinoptions/two-step-verification
- Добавь телефон или authenticator

### 2. Создай App Password
- https://myaccount.google.com/apppasswords
- Выбери приложение: **Mail**
- Выбери устройство: **ARGOS** (или "Другое")
- Нажми **Generate**
- **Скопируй 16-символьный код** (без пробелов)

### 3. Обнови .env
\\\ash
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx  # 16 символов
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=winargos42@gmail.com
\\\

### 4. Проверь отправку
Запусти тестовое письмо через MCP:
\\\
!mcp tool send_email
\\\

## Безопасность
- App Password дает ТОЛЬКО доступ к Gmail
- Не дает доступа к другим сервисам Google
- Можно отозвать в любой момент
- Не требует верификации приложения

## Следующий шаг
После получения App Password обновим .env и протестируем отправку.

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
