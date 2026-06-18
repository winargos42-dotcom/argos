#!/usr/bin/env python3
"""
ARGOS Telegram Streaming + Guest Mode (TG 7 May 2026 features).

Telegram AI Bot Revolution добавил:
1. Гостевой режим: @bot упомянуть в любом чате — он отвечает
2. Bot-to-Bot: боты могут отвечать другим ботам (ARGOS Council уже так работает!)
3. Постепенный вывод: editMessageText каждые ~0.5 сек

Использование:
    from telegram_streaming import stream_message
    stream_message(chat_id, "Текст...", bot_token=...)
"""
import os
import time
import requests
from typing import Optional, Callable


def _send(token: str, method: str, **kwargs) -> dict:
    """POST к Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/{method}"
    r = requests.post(url, json=kwargs, timeout=30)
    return r.json()


def stream_message(
    chat_id: int,
    text_source: Callable[[], str],
    bot_token: str,
    update_interval: float = 0.8,
    min_delta_chars: int = 30,
    max_wait: float = 120.0,
) -> Optional[int]:
    """
    Постепенный вывод длинного текста в TG (TG AI Bot Revolution 7 May 2026).

    Вместо одного большого sendMessage:
    1. Отправляем placeholder "⏳ генерирую..."
    2. editMessageText каждые ~0.5 сек пока LLM генерирует
    3. Финальный текст — без префикса "⏳"

    :param chat_id: ID чата
    :param text_source: функция, возвращающая текущий полный текст
    :param bot_token: токен бота
    :param update_interval: как часто проверять новый текст
    :param min_delta_chars: мин. разница в символах для обновления
    :param max_wait: макс. ожидание (сек)
    :return: message_id или None
    """
    start = time.time()
    msg_id = None
    last_sent = ""
    sent = False
    placeholder = "⏳ _генерирую ответ..._"

    while time.time() - start < max_wait:
        current = text_source()
        if not current:
            time.sleep(update_interval)
            continue

        if not sent:
            r = _send(bot_token, "sendMessage",
                      chat_id=chat_id,
                      text=placeholder,
                      parse_mode="Markdown")
            if r.get("ok"):
                msg_id = r["result"]["message_id"]
                sent = True
            else:
                return None

        if abs(len(current) - len(last_sent)) >= min_delta_chars:
            suffix = "\n\n_⏳ ..._" if len(current) > 4096 else ""
            try:
                r = _send(bot_token, "editMessageText",
                          chat_id=chat_id,
                          message_id=msg_id,
                          text=current[:4096] + suffix,
                          parse_mode="Markdown")
                if r.get("ok"):
                    last_sent = current
            except Exception:
                _send(bot_token, "editMessageText",
                      chat_id=chat_id,
                      message_id=msg_id,
                      text=current[:4096])
                last_sent = current

        # Если текст стабилизировался — выходим
        if current == last_sent and len(current) > 50:
            time.sleep(update_interval * 2)
            current2 = text_source()
            if current2 == current:
                _send(bot_token, "editMessageText",
                      chat_id=chat_id,
                      message_id=msg_id,
                      text=current[:4096])
                return msg_id

        time.sleep(update_interval)

    return msg_id


def is_guest_mode_enabled(bot_token: str) -> bool:
    """
    Проверяет, поддерживает ли бот гостевой режим (TG AI Bot Revolution 7 May 2026).
    Если supports_guest_queries=True — бота можно упоминать @bot в любом чате.
    """
    me = _send(bot_token, "getMe")
    if not me.get("ok"):
        return False
    return me.get("result", {}).get("supports_guest_queries", False)


def bot_info(bot_token: str) -> dict:
    """Информация о боте (включая guest mode)."""
    me = _send(bot_token, "getMe")
    if not me.get("ok"):
        return {"error": me.get("description", "unknown")}
    r = me["result"]
    return {
        "username": r.get("username"),
        "guest_mode": r.get("supports_guest_queries"),
        "inline": r.get("supports_inline_queries"),
        "groups": r.get("can_join_groups"),
        "topics": r.get("has_topics_enabled"),
    }


if __name__ == "__main__":
    import sys
    token = os.environ.get("ARGOS_BOT_TOKEN") or os.environ.get("BOT_ARGOS_CLAUDE_AI_BOT")
    if not token:
        print("NO TOKEN in env", file=sys.stderr)
        sys.exit(1)
    info = bot_info(token)
    print(f"Bot: @{info.get('username')}")
    print(f"  Guest mode (7 May 2026): {'✅' if info.get('guest_mode') else '❌'}")
    print(f"  Inline queries: {'✅' if info.get('inline') else '❌'}")
    print(f"  Can join groups: {'✅' if info.get('groups') else '❌'}")
    print(f"  Topics enabled: {'✅' if info.get('topics') else '❌'}")
