#!/usr/bin/env python3
"""
VirtualSIM Watcher — читает SMS коды из @virtualsimio_bot в Telegram.
Пишет коды в Brain API для телефонного агента.
Запускается на ноутбуке (есть ava_main.session).
"""
import asyncio, json, re, time, urllib.request
from pathlib import Path
import sys
sys.path.insert(0, '/home/ava/Projects/argoss')
sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')

API_ID   = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION  = "/home/ava/Projects/argoss/data/sessions/ava_tl"  # запасная сессия
BRAIN    = "http://192.168.1.53:5001"
COUNCIL  = "-5129226282"
PC_TOKEN = "8651650695:AAFKp_UyRq0cRorzV-Boouwwkf7kHB3xYw8"

VSIM_BOTS = [
    "virtualsimio_bot",
    "sms_activate_bot",
    "5simbot",
    "getsmscode_bot",
    "smshub_bot",
]

last_seen = {}

def post(url, data):
    try:
        body = json.dumps(data, ensure_ascii=False).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except: return None

def tg_send(text):
    try:
        body = json.dumps({"chat_id": COUNCIL, "text": text[:1000]}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{PC_TOKEN}/sendMessage",
            data=body, headers={"Content-Type":"application/json"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.loads(r.read()).get("ok")
    except: return False

async def watch_vsim(client):
    """Читаем сообщения от VirtualSIM ботов."""
    print(f"Watching VirtualSIM bots: {VSIM_BOTS}")

    while True:
        for bot_name in VSIM_BOTS:
            try:
                entity = await client.get_entity(bot_name)
                msgs = await client.get_messages(entity, limit=5)

                for m in msgs:
                    if not m.text:
                        continue
                    msg_id = f"{bot_name}:{m.id}"
                    if msg_id in last_seen:
                        continue

                    last_seen[msg_id] = True
                    text = m.text

                    # Ищем коды верификации
                    codes = re.findall(r'\b(\d{4,8})\b', text)
                    phones = re.findall(r'\+\d{10,15}', text)

                    if codes:
                        print(f"[{bot_name}] Код: {codes} | Номер: {phones}")

                        # Сохраняем в Brain
                        post(f"{BRAIN}/brain/event", {
                            "node_id": "vsim-watcher",
                            "event": "sms_code",
                            "data": {
                                "codes": codes,
                                "phones": phones,
                                "message": text[:200],
                                "bot": bot_name,
                                "ts": time.time()
                            }
                        })

                        # Уведомляем в Entity Council
                        tg_send(
                            f"📱 *VirtualSIM код*\n"
                            f"Бот: @{bot_name}\n"
                            f"Номер: {', '.join(phones) if phones else '?'}\n"
                            f"Код: `{'` `'.join(codes)}`\n"
                            f"Сообщение: {text[:100]}"
                        )

            except Exception as e:
                if "not found" not in str(e).lower():
                    print(f"[{bot_name}] {e}")

        await asyncio.sleep(15)  # проверяем каждые 15 сек

async def buy_number(client, service="Telegram"):
    """Покупаем виртуальный номер."""
    try:
        vsim = await client.get_entity("virtualsimio_bot")
        await client.send_message(vsim, f"/buy {service}")
        await asyncio.sleep(5)
        msgs = await client.get_messages(vsim, limit=3)
        for m in msgs:
            if not m.out and m.text:
                phones = re.findall(r'\+\d{10,15}', m.text)
                if phones:
                    print(f"Куплен номер: {phones[0]}")
                    return phones[0]
    except Exception as e:
        print(f"Buy number error: {e}")
    return None

async def main():
    from telethon import TelegramClient

    # Пробуем запасную сессию
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print(f"❌ Сессия {SESSION} не авторизована")
        # Пробуем ava_main
        from telethon.sessions import SQLiteSession
        SESSION2 = "/home/ava/Projects/argoss/data/sessions/ava_main"
        client2 = TelegramClient(SESSION2, API_ID, API_HASH)
        try:
            await client2.connect()
            if await client2.is_user_authorized():
                me = await client2.get_me()
                print(f"✅ Используем ava_main: @{me.username}")
                await watch_vsim(client2)
        except Exception as e:
            print(f"ava_main error: {e}")
        return

    me = await client.get_me()
    print(f"✅ Подключён: @{me.username}")

    # Регистрируем в Brain
    post(f"{BRAIN}/brain/register", {
        "node_id": "vsim-watcher",
        "address": "192.168.1.53",
        "capabilities": ["sms_monitoring","vsim","number_buying"],
        "meta": {"role":"vsim_watcher","bots": VSIM_BOTS}
    })

    await watch_vsim(client)

if __name__ == "__main__":
    asyncio.run(main())
