"""
Создаёт боты сущностей через BotFather с паузой 320 сек между каждым.
Сохраняет прогресс — можно прерывать и продолжать.
"""
import asyncio, re, json, os, time

API_ID   = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION  = "/home/ava/Projects/argoss/data/sessions/argos_tl"
TOKENS   = "/home/ava/Projects/argoss/data/entity_bot_tokens.json"
PAUSE    = 320  # 5 мин 20 сек между ботами

BOTS = [
    ("ARGOS DeepSeek Bot",    "argos_deepseek_v3_bot"),
    ("ARGOS Gemini Bot",      "argos_gemini_v3_bot"),
    ("ARGOS Cloudflare Bot",  "argos_cf_v3_bot"),
    ("ARGOS OpenAI Bot",      "argos_openai_v3_bot"),
    ("ARGOS Brain Hub",       "argos_hub_brain_bot"),
    ("ARGOS Evolution Bot",   "argos_evol_v3_bot"),
]

def load_tokens():
    existing = {}
    if os.path.exists(TOKENS):
        existing = json.load(open(TOKENS))
    # Добавляем уже созданные
    existing.setdefault("argos_claude_ai_bot", "8753655441:AAFzgbF1Smxc7Cz-IibRDVR3sgobFn-9K8s")
    existing.setdefault("argos_kimi_ai_bot",   "8685383341:AAF6cJOYw5n1T0Uj_WupwKF28h8He73_nvc")
    return existing

async def main():
    from telethon import TelegramClient, functions
    from telethon.tl.functions.messages import GetDialogsRequest
    from telethon.tl.types import InputPeerEmpty, InputPeerUser

    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    
    me = await client.get_me()
    print(f"✅ Аккаунт: {me.first_name} id={me.id}")
    
    dialogs = await client(GetDialogsRequest(
        offset_date=None, offset_id=0,
        offset_peer=InputPeerEmpty(), limit=100, hash=0
    ))
    bf = next((u for u in dialogs.users if u.id == 93372553), None)
    bf_peer = InputPeerUser(bf.id, bf.access_hash)
    
    tokens = load_tokens()
    print(f"Уже создано: {len(tokens)} ботов")
    
    for i, (name, username) in enumerate(BOTS):
        if username in tokens:
            print(f"⏭️  @{username} уже создан")
            continue
        
        print(f"\n[{i+1}/{len(BOTS)}] → {name} (@{username})")
        
        if i > 0:
            print(f"  ⏳ Пауза {PAUSE}с (BotFather limit)...")
            # Публикуем статус каждые 30 сек
            for s in range(0, PAUSE, 30):
                await asyncio.sleep(30)
                remaining = PAUSE - s - 30
                print(f"  ⏳ Осталось {max(0,remaining)}с")
        
        try:
            await client(functions.messages.SendMessageRequest(
                peer=bf_peer, message="/newbot",
                random_id=int.from_bytes(os.urandom(8),'big',signed=True),
                no_webpage=True
            ))
            await asyncio.sleep(3)
            
            await client(functions.messages.SendMessageRequest(
                peer=bf_peer, message=name,
                random_id=int.from_bytes(os.urandom(8),'big',signed=True),
                no_webpage=True
            ))
            await asyncio.sleep(3)
            
            await client(functions.messages.SendMessageRequest(
                peer=bf_peer, message=username,
                random_id=int.from_bytes(os.urandom(8),'big',signed=True),
                no_webpage=True
            ))
            await asyncio.sleep(6)
            
            msgs = await client.get_messages(bf_peer, limit=3)
            for m in msgs:
                text = m.text or ""
                tok = re.search(r'(\d{8,10}:[A-Za-z0-9_-]{35})', text)
                if tok:
                    tokens[username] = tok.group(0)
                    print(f"  ✅ Token: {tok.group(0)}")
                    json.dump(tokens, open(TOKENS,"w"), indent=2)
                    break
                elif any(k in text.lower() for k in ["taken","sorry","unavailable","already"]):
                    print(f"  ⚠️ {text[:100]}")
                    break
        except Exception as e:
            print(f"  Error: {type(e).__name__}: {e}")
    
    json.dump(tokens, open(TOKENS,"w"), indent=2)
    print(f"\n✅ ГОТОВО! {len(tokens)} ботов:")
    for k,v in tokens.items():
        print(f"  @{k}: {v}")
    
    await client.disconnect()

asyncio.run(main())
