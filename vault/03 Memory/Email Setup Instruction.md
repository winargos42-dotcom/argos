# Инструкция: Email для ARGOS

**Дата:** 2026-05-06  
**Email:** winargos42@gmail.com  
**Проблема:** Обычный пароль заблокирован Gmail (2FA)

---

## Быстрое решение (2 минуты)

### Шаг 1: Создать App Password
1. Открыть: https://myaccount.google.com/apppasswords
2. Войти как **winargos42@gmail.com**
3. В разделе "Выберите приложение" выбрать **Другое (пользовательское имя)**
4. Ввести название: **ARGOS**
5. Нажать **Создать**
6. **Скопировать 16-значный пароль** (без пробелов)

### Шаг 2: Обновить .env
```bash
# Открыть файл
notepad F:\debug\argoss\.env

# Найти и заменить:
SMTP_PASSWORD=sigtrip1464
ARGOS_EMAIL_PASSWORD=sigtrip1464

# На новый App Password (16 символов):
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
ARGOS_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

### Шаг 3: Перезапустить ARGOS
```powershell
# Убить процессы
Get-Process python | Where-Object {$_.Path -match "argoss"} | Stop-Process -Force

# Перезапустить
cd F:\debug\argoss
python main.py --no-gui
```

---

## Проверка отправки

После обновления пароля, ARGOS сможет отправлять письма:
- Через Telegram: `отправь письмо на email@example.com Привет!`
- Через MCP: `{"command": "отправь письмо", "args": {"to": "email@example.com", "subject": "Тема", "body": "Текст"}}`

---

## Примечание

**Почему не работает обычный пароль?**
- Gmail включил 2-Factor Authentication (2FA)
- С 2024 года обычные пароли заблокированы для SMTP
- Требуется специальный "App Password" для приложений

**Безопасность:**
- App Password работает только для SMTP/IMAP
- Не дает доступа к веб-интерфейсу Gmail
- Можно отозвать в любой момент

---

*Создано автоматически ARGOS*

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
