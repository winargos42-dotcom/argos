# 2026-05-11 ARGOS Telegram Clean Restart

## Причина
После патча `+` пользователь сообщил, что Telegram всё ещё не отвечает.

## Найдено
- Прямой Bot API `sendMessage` успешно отправляет сообщения admin chat `6923777384`.
- Значит токен, chat_id и сеть Telegram рабочие.
- Старый живой процесс держал MCP/lock, но task-log не обновлялся.
- До перезапуска прямой `getUpdates` не конфликтовал, что указывало на отсутствие активного long-polling у живого процесса.

## Действие
- Остановлены stale PID `19032` (`main.py --no-gui`) и `12312` (`web_server.py`).
- Запущена Windows task `Start Argos on Logon`.

## Проверка после перезапуска
- Task `Start Argos on Logon`: `Running`.
- Новый основной PID: `17964` (`python.exe F:\debug\argoss\main.py --no-gui`).
- Лог: `[TG] bot ready: @Argosssbot id=8651650695`.
- Лог: `[TG] polling started`.
- Прямой `getUpdates` теперь возвращает `409 Conflict`, что подтверждает активный Telegram long-polling внутри ARGOS.
- MCP health `http://127.0.0.1:8000/health` -> `200`, `ok=true`.
- Порты: `8000`, `8080`, `8082`, `8084`, `8090`, `11434`, `47291`.
- Служебное сообщение отправлено в Telegram: `message_id=7143`.

## Следующий контроль
- Пользователь отправляет `+`.
- Ожидаемый ответ: быстрый `ARGOS [Direct]`.
- Если ответа нет, смотреть `logs/argos_task_20260511_224757.out.log` на `[TG] incoming`.