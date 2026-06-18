# Email: Финальная инструкция по OAuth

**Дата:** 2026-05-06
**Проблема:** Приложение не прошло проверку Google (Testing mode)

## Быстрое решение

### Шаг 1: Открыть консоль (10 секунд)
https://console.cloud.google.com/apis/credentials/consent?project=argos-489214

### Шаг 2: Нажать кнопку
**PUBLISH APP** (вверху справа)

### Шаг 3: Подтвердить
Нажать "CONFIRM"

### Шаг 4: Отправить email
\\\powershell
cd F:\debug\argoss
. .venv\Scripts\Activate.ps1
python send_email_oauth.py
\\\

Браузер откроется для авторизации → подтверди → письмо отправится!

## Альтернатива (если публикация не сработает)

Добавить тестового пользователя:
1. В том же окне найти "Test users"
2. Нажать "ADD USERS"
3. Ввести: winargos42@gmail.com
4. Сохранить
5. Повторить отправку email

---
*Создано автоматически*

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
