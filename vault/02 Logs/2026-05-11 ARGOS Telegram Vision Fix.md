# 2026-05-11 ARGOS Telegram Vision Fix

## Причина
- `+` уже отвечает Direct, Telegram bridge ожил.
- После отправки изображения ARGOS падал ответом: `❌ Ошибка анализа: 'NoneType' object is not subscriptable`.
- Короткое число `89385` уходило в Offline/AI path вместо быстрого Direct.

## Исправлено
- `src/connectivity/telegram_bot.py`: `handle_photo` больше не вызывает напрямую `self.core.vision._analyse(temp_path)`.
- Добавлен `_analyze_photo_file()` — совместимый адаптер для разных vision-реализаций:
  - `vision.analyze_file(path)`
  - `vision.analyze_image(path[, caption])`
  - `vision.bridge.describe_image(path)`
  - fallback `vision._analyse(base64)`
  - безопасный текст, если vision вернул `None`.
- `src/connectivity/telegram_bot.py`: короткие числовые сообщения до 12 цифр отвечают Direct (`Получил число/код`) без AI pipeline.
- `tests/test_telegram_bot_history_scope.py`: добавлены регрессии для numeric Direct и photo vision adapter.

## Проверка
- `pytest tests/test_telegram_bot_history_scope.py tests/test_web_learn_routing.py tests/test_telegram_can_start.py tests/test_core_provider_resilience.py -q` -> `26 passed`.
- `py_compile src/connectivity/telegram_bot.py` -> OK.
- Перезапуск через `Start Argos on Logon`: task `Running`, новый PID `23320`.
- MCP health -> `200`, `ok=true`.
- Telegram long-polling подтверждён: прямой `getUpdates` возвращает `409 Conflict`.
- Активные порты: `8000`, `8080`, `8082`, `8084`, `8090`, `11434`, `47291`.

## Следующий контроль
- В Telegram отправить `89385` -> ожидается быстрый Direct.
- Отправить фото -> ожидается описание или безопасное предупреждение vision, но не Python exception.