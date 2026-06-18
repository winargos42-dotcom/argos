# Email: Ошибка OAuth — Приложение не проверено

**Дата:** 2026-05-06  
**Email:** winargos42@gmail.com  
**Ошибка:** `403: access_denied` — Приложение "argos" не прошло проверку Google

---

## Причина

OAuth приложение (Client ID: `508337926357-lokspuo11ijiis17kuksljin5if9abrl`) находится в **тестовом режиме** (Testing).

Google блокирует доступ для пользователей, которые не добавлены в список тестировщиков.

---

## Решение 1: Опубликовать приложение (рекомендуется)

### Шаги:
1. Открыть: https://console.cloud.google.com/apis/credentials/consent
2. Выбрать проект **argos-489214**
3. В разделе **Publishing status** нажать **PUBLISH APP**
4. Подтвердить публикацию

После этого OAuth будет работать для всех пользователей.

---

## Решение 2: Добавить тестировщика

### Шаги:
1. Открыть: https://console.cloud.google.com/apis/credentials/consent
2. Выбрать проект **argos-489214**
3. В разделе **Test users** нажать **ADD USERS**
4. Добавить: `winargos42@gmail.com`
5. Сохранить

---

## Решение 3: App Password (самый быстрый)

Если OAuth настроить сложно, использовать **App Password**:

1. https://myaccount.google.com/apppasswords
2. Создать пароль для приложения "ARGOS"
3. Обновить `.env`:
   ```
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   ARGOS_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

---

## Текущий статус

- ❌ OAuth: Блокирован (тестовый режим)
- ❌ SMTP: Блокирован (обычный пароль)
- ⏳ Решение: Требуется действие пользователя

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
