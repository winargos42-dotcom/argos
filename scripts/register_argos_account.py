"""
Быстрая регистрация нового Telegram аккаунта для ARGOS сущностей.
Использование: python3 register_argos_account.py +7XXXXXXXXXX КОД
"""
import asyncio, re, json, sys, os

API_ID   = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"

ENTITY_BOTS = [
    ("ARGOS Claude Bot",     "argos_claude_v3_bot"),
    ("ARGOS DeepSeek Bot",   "argos_deepseek_v3_bot"),
    ("ARGOS Kimi Bot",       "argos_kimi_v3_bot"),
    ("ARGOS Gemini Bot",     "argos_gemini_v3_bot"),
    ("ARGOS Cloudflare Bot", "argos_cf_v3_bot"),
    ("ARGOS Entity Hub",     "argos_hub_v3_bot"),
    ("ARGOS Brain Bot",      "argos_brain_v3_bot"),
    ("ARGOS Evolution Bot",  "argos_evol_v3_bot"),
]

async def main():
    phone = sys.argv[1] if len(sys.argv) > 1 else input("Номер телефона: ")
    code  = sys.argv[2] if len(sys.argv) > 2 else None
    
    from telethon import TelegramClient
    
    session_name = f"/home/ava/Projects/argoss/data/sessions/argos_{phone.replace('+','')}"
    os.makedirs(os.path.dirname(session_name), exist_ok=True)
    
    client = TelegramClient(session_name, API_ID, API_HASH)
    
    if code:
        await client.connect()
        await client.send_code_request(phone)
        await client.sign_in(phone, code)
    else:
        await client.start(phone=phone)
    
    me = await client.get_me()
    print(f"✅ Аккаунт: {me.first_name} id={me.id} phone={me.phone}")
    
    # Создаём ботов через BotFather
    from telethon.tl.functions.messages import GetDialogsRequest
    from telethon.tl.types import InputPeerEmpty
    
    # Ищем BotFather
    dialogs = await client(GetDialogsRequest(
        offset_date=None, offset_id=0,
        offset_peer=InputPeerEmpty(), limit=100, hash=0
    ))
    bf = next((u for u in dialogs.users if u.id == 93372553), None)
    if not bf:
        bf = await client.get_entity("@BotFather")
    
    tokens = {}
    for name, username in ENTITY_BOTS:
        print(f"\n→ {name} (@{username})")
        try:
            await client.send_message(bf, "/newbot")
            await asyncio.sleep(2)
            await client.send_message(bf, name)
            await asyncio.sleep(2)
            await client.send_message(bf, username)
            await asyncio.sleep(5)
            
            msgs = await client.get_messages(bf, limit=2)
            for m in msgs:
                tok = re.search(r'\d{8,10}:[A-Za-z0-9_-]{35}', m.text or "")
                if tok:
                    tokens[username] = tok.group(0)
                    print(f"  ✅ {tok.group(0)}")
                    break
                elif any(k in (m.text or "").lower() for k in ["taken","sorry","unavailable"]):
                    print(f"  ⚠️ {(m.text or '')[:80]}")
                    break
            await asyncio.sleep(3)
        except Exception as e:
            print(f"  Error: {e}")
    
    # Сохраняем
    all_tokens = {}
    tok_file = "/tmp/entity_bot_tokens.json"
    if os.path.exists(tok_file):
        all_tokens = json.load(open(tok_file))
    all_tokens.update(tokens)
    json.dump(all_tokens, open(tok_file,"w"), indent=2)
    
    print(f"\n✅ Итого токенов: {len(all_tokens)}")
    for u,t in all_tokens.items():
        print(f"  @{u}: {t}")
    
    await client.disconnect()

asyncio.run(main())
