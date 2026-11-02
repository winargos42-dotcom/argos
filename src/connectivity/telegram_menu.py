"""Repair ARGOS's Telegram command list and per-chat menu button."""

from __future__ import annotations


COMMAND_MENU = [
    ("start", "Запустить Аргос"),
    ("help", "Справка по командам"),
    ("commands", "Все команды Аргоса"),
    ("status", "Состояние системы"),
    ("tghealth", "Проверка Telegram"),
    ("ask", "Задать вопрос ИИ"),
    ("providers", "Доступные модели ИИ"),
    ("skills", "Навыки Аргоса"),
    ("agents", "Состояние агентов"),
    ("memory", "Память Аргоса"),
    ("history", "История беседы"),
    ("voice_on", "Включить голос"),
    ("voice_off", "Выключить голос"),
    ("limits", "Лимиты провайдеров"),
    ("network", "Сеть и подключения"),
    ("alerts", "Уведомления"),
    ("reasoning", "Режим рассуждений"),
    ("ai_edit", "Редактор ИИ"),
]

PILOT_MENU = [
    ("menudemo", "Демонстрация меню Яндекс.Еды"),
    ("menu", "Меню ресторана по ссылке"),
    ("menuai", "Анализ меню через ИИ"),
    ("menudemoai", "ИИ на учебном меню"),
    ("menutokens", "Токены пилота меню"),
    ("menuhtml", "Загрузить HTML меню"),
]


def _merge_commands(registered, existing):
    descriptions = dict(COMMAND_MENU + PILOT_MENU)
    for item in existing:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            key, description = item
        else:
            key = getattr(item, "command", None)
            description = getattr(item, "description", None)
        if isinstance(key, str) and isinstance(description, str):
            descriptions.setdefault(key, description)

    ordered = [command for command, _ in COMMAND_MENU]
    extras = set(registered or ()) | {
        getattr(item, "command", item[0] if isinstance(item, (list, tuple)) and item else "")
        for item in existing
    }
    for command in sorted(extras):
        if isinstance(command, str) and command.isascii() and command.replace("_", "").isalnum() and command not in ordered:
            ordered.append(command)
    return [(command, descriptions.get(command, "Команда ARGOS")) for command in ordered[:100]]


async def configure_command_menu(
    bot, chat_ids, menu_button, *, registered_commands=(), scope_for_chat=None
) -> list[str]:
    """Restore the command menu globally and for known private chats.

    Telegram lets an old per-chat WebApp button override the default button.
    Updating the default alone won't replace a previously configured Yandex URL.
    Return errors instead of preventing the bot from starting.
    """
    errors = []
    existing = []
    try:
        existing = await bot.get_my_commands()
    except Exception as exc:
        errors.append(f"get_my_commands: {type(exc).__name__}: {exc}")
    commands = _merge_commands(registered_commands, existing)
    try:
        await bot.set_my_commands(commands)
    except Exception as exc:
        errors.append(f"set_my_commands: {type(exc).__name__}: {exc}")

    # Telegram may have a Russian-language-specific command list that hides
    # the default list, so update that scope as well.
    try:
        russian = await bot.get_my_commands(language_code="ru")
        await bot.set_my_commands(_merge_commands(registered_commands, existing + russian), language_code="ru")
    except Exception as exc:
        errors.append(f"set_ru_commands: {type(exc).__name__}: {exc}")

    try:
        await bot.set_chat_menu_button(menu_button=menu_button)
    except Exception as exc:
        errors.append(f"set_default_menu: {type(exc).__name__}: {exc}")

    for chat_id in sorted(set(str(x).strip() for x in chat_ids)):
        if not chat_id.isascii() or not chat_id.isdecimal():
            continue
        try:
            await bot.set_chat_menu_button(chat_id=int(chat_id), menu_button=menu_button)
        except Exception as exc:
            errors.append(f"set_chat_menu({chat_id}): {type(exc).__name__}: {exc}")
        if scope_for_chat is not None:
            # A chat-specific command scope takes precedence over bot defaults.
            # Restore both its generic and Russian lists without losing pilot commands.
            scope = scope_for_chat(int(chat_id))
            for language in (None, "ru"):
                options = {"scope": scope}
                if language:
                    options["language_code"] = language
                try:
                    scoped = await bot.get_my_commands(**options)
                    await bot.set_my_commands(
                        _merge_commands(registered_commands, existing + scoped), **options
                    )
                except Exception as exc:
                    errors.append(f"set_chat_commands({chat_id},{language}): {type(exc).__name__}: {exc}")
    return errors
