#!/usr/bin/env python3
"""
ARGOS Autopilot v3 — использует АККАУНТ АРГОС (не бота) для отправки сообщений.
Читает входящие сообщения через Bot API, отвечает через MTProto (аккаунт АРГОС).
"""
import asyncio, time, json, subprocess, os, sys, re
sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')
from pathlib import Path
from datetime import datetime

# Telethon для АРГОС аккаунта
from telethon import TelegramClient, events
from telethon.sessions import SQLiteSession

import urllib.request

# ── Конфиг ──────────────────────────────────────────────────────────────────

env = open('/home/ava/Projects/argoss/.env').read()
def genv(k):
    m = re.search(f"{k}=([^\\n\\s]+)", env)
    return m.group(1).strip() if m else ""

TG_BOT_TOKEN = genv("TELEGRAM_BOT_TOKEN")  # @Argosssbot — для чтения updates
ANT_KEY      = genv("ANTHROPIC_API_KEY")
TOKENS       = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))
GROUP_ID     = -5129226282
AVA_ID       = 6923777384
CHECK_INTERVAL = 30

# АРГОС аккаунт (пишем ОТ НЕГО)
API_ID   = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
ARGOS_SESSION = '/home/ava/Projects/argoss/data/sessions/ava_main'

OFFSET_FILE = "/home/ava/Projects/argoss/data/autopilot_offset.json"

def bot_api(method, **kwargs):
    body = json.dumps(kwargs).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/{method}",
        data=body, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except: return {"ok": False}

def get_updates(offset=0):
    return bot_api("getUpdates", offset=offset, timeout=5, limit=20,
        allowed_updates=["message"])

def load_offset():
    try: return json.load(open(OFFSET_FILE))
    except: return {"update_id": 0}

def save_offset(data):
    json.dump(data, open(OFFSET_FILE, "w"), indent=2)

def get_system_data():
    data = {"brain": "?", "entity_bus": "?", "thoughts": {}}
    try:
        r = urllib.request.urlopen("http://192.168.1.53:5001/brain/nodes", timeout=5)
        d = json.loads(r.read())
        data["brain"] = f"{d['online']}/{d['total']}"
    except: pass
    data["entity_bus"] = subprocess.run(
        ["systemctl","is-active","argos-entity-bus"], capture_output=True, text=True
    ).stdout.strip()
    mem_dir = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/entities/memory")
    for f in mem_dir.glob("*.md"):
        lines = [l.strip() for l in f.read_text(errors="utf-8").split('\n') if l.strip() and not l.startswith('#')]
        if lines: data["thoughts"][f.stem] = lines[-1][:80]
    return data

def generate_image(prompt: str) -> bytes | None:
    """Генерируем через Pollinations или CF."""
    import urllib.parse
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=768&height=768&nologo=true"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ARGOS/2.0"})
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read()
            return data if len(data) > 10000 else None
    except: return None

async def main():
    print("🤖 ARGOS Autopilot v3 — пишет от аккаунта АРГОС")
    
    client = TelegramClient(ARGOS_SESSION, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ АРГОС сессия не авторизована!")
        return
    
    me = await client.get_me()
    print(f"Подключён как: {me.first_name} @{me.username} (id={me.id})")
    
    state = load_offset()
    cycle = 0
    
    while True:
        cycle += 1
        ts = datetime.now().strftime("%H:%M:%S")
        
        # Читаем новые updates через Bot API
        updates = get_updates(state["update_id"])
        
        if updates.get("ok") and updates.get("result"):
            for upd in updates["result"]:
                uid = upd.get("update_id", 0)
                state["update_id"] = max(state["update_id"], uid + 1)
                
                msg  = upd.get("message", {})
                text = msg.get("text", "")
                from_id  = msg.get("from", {}).get("id", 0)
                from_name = msg.get("from", {}).get("first_name", "User")
                chat_id  = msg.get("chat", {}).get("id", 0)
                
                if not text: continue
                
                print(f"[{ts}] '{text[:50]}' от {from_name}")
                
                data = get_system_data()
                
                # Определяем ответ
                tl = text.lower()
                
                if any(w in tl for w in ["нарисуй", "создай рисунок", "создай картин", "/draw ", "draw ", "сгенерируй", "аниме", "anime"]):
                    # Рисуем
                    for pref in ["/draw ", "нарисуй ", "создай рисунок ", "создай картинку ", "draw ", "сгенерируй ", "аниме ", "anime "]:
                        if tl.startswith(pref):
                            prompt = text[len(pref):].strip()
                            break
                    else:
                        prompt = text.strip()
                    
                    if "аниме" in tl or "anime" in tl:
                        prompt = f"anime style, {prompt}, high quality"
                    
                    await client.send_message(chat_id, f"🎨 Рисую: {prompt[:40]}...")
                    
                    img = generate_image(prompt)
                    if img:
                        import tempfile
                        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                            f.write(img)
                            fname = f.name
                        await client.send_file(chat_id, fname,
                            caption=f"🎨 Pollinations: {prompt[:60]}")
                        os.unlink(fname)
                    else:
                        await client.send_message(chat_id, "❌ Не смог нарисовать")
                
                elif tl in ("/status", "/s", "статус", "status"):
                    th = "\n".join(f"• {k}" for k in list(data["thoughts"].keys())[:5])
                    reply = f"📊 ARGOS [{ts}]\nBrain: {data['brain']} | Bus: {data['entity_bus']}\nСущностей: {len(data['thoughts'])}\n{th}"
                    await client.send_message(chat_id, reply)
                
                elif tl in ("/thoughts", "/t"):
                    th = "\n".join(f"• {k}: {v[:80]}" for k,v in list(data["thoughts"].items())[:5])
                    await client.send_message(chat_id, f"💭 Мысли:\n{th}")
                
                elif tl in ("/nodes", "/n"):
                    try:
                        r = urllib.request.urlopen("http://192.168.1.53:5001/brain/nodes", timeout=5)
                        d = json.loads(r.read())
                        nodes = "\n".join(f"{'✅' if n['status']=='online' else '❌'} {n['node_id']}" for n in d['nodes'][:12])
                        await client.send_message(chat_id, f"🌐 Brain [{d['online']}/{d['total']}]:\n{nodes}")
                    except:
                        await client.send_message(chat_id, "Brain недоступен")
                
                elif tl in ("/help", "/start", "/skills"):
                    await client.send_message(chat_id,
                        "ARGOS Universal OS 🤖\n\n"
                        "/status — состояние системы\n"
                        "/thoughts — мысли сущностей\n"
                        "/nodes — ноды Brain\n"
                        "нарисуй <текст> — генерация изображения\n"
                        "аниме <текст> — аниме стиль\n"
                        "/draw <текст> — рисунок")
                
                else:
                    # Общий ответ
                    await client.send_message(chat_id,
                        f"ARGOS [{ts}]\nBrain: {data['brain']} | {data['entity_bus']}\n"
                        f"Напиши /help для списка команд")
            
            save_offset(state)
        
        print(f"[{ts}] #{cycle} Brain:{data.get('brain','?')} offset={state['update_id']}")
        await asyncio.sleep(CHECK_INTERVAL)

asyncio.run(main())
