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


async def configure_command_menu(bot, chat_ids, menu_button) -> list[str]:
    """Restore the command menu globally and for known private chats.

    Telegram lets an old per-chat WebApp button override the default button.
    Updating the default alone won't replace a previously configured Yandex URL.
    Return errors instead of preventing the bot from starting.
    """
    errors = []
    try:
        await bot.set_my_commands(COMMAND_MENU)
    except Exception as exc:
        errors.append(f"set_my_commands: {type(exc).__name__}: {exc}")

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
    return errors
