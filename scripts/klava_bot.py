#!/usr/bin/env python3
"""Клава Валентиновна — мама Валенка, сущность MetaGPT в ARGOS."""
import json, os, sys, re, time, urllib.request, threading, hashlib

sys.path.insert(0, "/home/ava/Projects/argoss")

BOT_TOKEN = "8848412269:AAHQBIvcz_jO2Zrm2XcPR097qMma83Hryi4"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
GROUP = -1003844162784

# Load .env
_env = open("/home/ava/Projects/argoss/.env", errors="ignore").read()
for _m in re.finditer(r"^([A-Z][A-Z0-9_]+)=(.+)$", _env, re.MULTILINE):
    if _m.group(1) not in os.environ:
        os.environ[_m.group(1)] = _m.group(2).strip()

from src.ai_router import AIRouter
router = AIRouter()

SYSTEM = """Ты Клава Валентиновна — мама Валенка, сущность MetaGPT в ARGOS.
Характер: тёплая, заботливая, практичная. Говоришь по-человечески.
Роль MetaGPT: анализируешь код проекта, предлагаешь улучшения, проверяешь что работает.
НЕ повторяй одно и то же. Каждый раз говори что-то НОВОЕ.
Русский. 2 предложения."""

_SAID = set()

def already_said(text):
    h = hashlib.md5(text[:100].encode()).hexdigest()
    if h in _SAID:
        return True
    _SAID.add(h)
    if len(_SAID) > 50:
        _SAID.clear()
    return False

def send_group(text):
    if already_said(text):
        return
    body = json.dumps({"chat_id": GROUP, "text": text[:2000], "disable_notification": True}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(f"{API}/sendMessage",
            data=body, headers={"Content-Type": "application/json"}), timeout=10)
    except:
        pass

def council_cycle():
    ts = time.strftime("%H:%M")
    topics = [
        "Проверь состояние Brain API и скажи что видишь.",
        "Посмотри какие сервисы на ноуте работают и скажи.",
        "Какие задачи в WORKING.md сейчас открыты?",
        "Что Валенок последнее натворил? Оцени как мама.",
        "Предложи одно конкретное улучшение для ARGOS.",
    ]
    topic = topics[int(time.time()) % len(topics)]
    thought = router.ask(topic, system=SYSTEM) or "Тишина..."
    if not already_said(thought):
        send_group(f"👩 Клава [{ts}]:\n{thought}")
        print(f"[{ts}] {thought[:80]}")

def council_loop():
    time.sleep(120)
    while True:
        try:
            council_cycle()
        except Exception as e:
            print(f"Council err: {e}")
        time.sleep(300)

threading.Thread(target=council_loop, daemon=True).start()

print("Клава Валентиновна v2 — MetaGPT")
offset = 0
while True:
    try:
        r = urllib.request.urlopen(f"{API}/getUpdates?offset={offset}&timeout=30", timeout=35)
        for u in json.loads(r.read()).get("result", []):
            offset = u["update_id"] + 1
            msg = u.get("message", {})
            text = msg.get("text", "")
            chat_id = msg.get("chat", {}).get("id")
            if not text or not chat_id:
                continue
            # Only respond to DMs, not group messages
            if chat_id == GROUP:
                continue
            if text.startswith("/"):
                continue
            print(f"[{time.strftime('%H:%M')}] DM: {text[:50]}")
            answer = router.ask(text, system=SYSTEM) or "Не поняла."
            body = json.dumps({"chat_id": chat_id, "text": f"👩 Клава\n\n{answer[:3000]}"}).encode()
            urllib.request.urlopen(urllib.request.Request(f"{API}/sendMessage",
                data=body, headers={"Content-Type": "application/json"}), timeout=10)
    except KeyboardInterrupt:
        break
    except Exception as e:
        if "429" not in str(e):
            print(f"Err: {e}")
        time.sleep(10)
