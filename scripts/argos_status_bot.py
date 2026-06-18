#!/usr/bin/env python3
"""
ARGOS Status Bot — монетизация через Telegram.
Приоритет А: отчёты/статусы (рекомендация @claude_gidbot)
Команды: /status /unavail /hard_heal
"""
import urllib.request, json, time, re, subprocess
from datetime import datetime

# Токен нужно задать через BotFather
import os
TOKEN = os.getenv("ARGOS_STATUS_BOT_TOKEN", "")
if not TOKEN:
    print("⚠️  Нужен ARGOS_STATUS_BOT_TOKEN в .env")
    print("Создай бота через @BotFather и добавь ARGOS_STATUS_BOT_TOKEN=...")
    exit(1)

BRAIN_URL = "http://192.168.1.53:5001"
HA_TOKEN = re.search(r'HA_TOKEN=([^\n\s]+)', open('/home/ava/Projects/argoss/.env').read())
HA_TOKEN = HA_TOKEN.group(1) if HA_TOKEN else ""

def brain_status():
    try:
        r = urllib.request.urlopen(f"{BRAIN_URL}/brain/nodes", timeout=5)
        d = json.loads(r.read())
        online = [n['node_id'] for n in d['nodes'] if n['status'] == 'online']
        offline = [n['node_id'] for n in d['nodes'] if n['status'] != 'online']
        return f"{d['online']}/{d['total']} нод онлайн", online, offline
    except: return "?/?", [], []

def ha_status():
    try:
        req = urllib.request.Request("http://localhost:8123/api/states",
            headers={"Authorization": f"Bearer {HA_TOKEN}"})
        with urllib.request.urlopen(req, timeout=5) as r:
            states = json.load(r)
        unavail = [s for s in states if s['state'] == 'unavailable']
        domains = {}
        for s in unavail:
            d = s['entity_id'].split('.')[0]
            domains[d] = domains.get(d, 0) + 1
        return len(states), unavail, domains
    except: return "?", [], {}

def get_watchdog_log():
    try:
        log = open("/var/log/argos_ha_watchdog.log", errors="replace").readlines()
        heals = [l for l in log if 'healing_event' in l][-5:]
        return "\n".join(l.strip()[:100] for l in heals) or "нет событий"
    except: return "лог недоступен"

def send(chat_id, text):
    body = json.dumps({"chat_id": chat_id, "text": str(text)[:4000], "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try: urllib.request.urlopen(req, timeout=8)
    except: pass

def get_updates(offset=0):
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=0&limit=10")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.load(r).get("result", [])
    except: return []

print("🤖 ARGOS Status Bot запущен")
offset = 0

while True:
    for upd in get_updates(offset):
        offset = max(offset, upd["update_id"] + 1)
        msg = upd.get("message", {})
        text = msg.get("text", "")
        chat_id = msg.get("chat", {}).get("id", 0)
        if not text: continue
        
        t = text.lower()
        ts = datetime.now().strftime("%H:%M")
        
        if t in ("/start", "/help"):
            send(chat_id,
                f"*ARGOS Status Bot* 🤖\n\n"
                f"Мониторинг системы ARGOS в реальном времени\n\n"
                f"Команды:\n"
                f"/status — общий статус\n"
                f"/unavail — недоступные entities\n"
                f"/hard\\_heal — последние события healing\n"
                f"/nodes — список нод Brain")
        
        elif t == "/status":
            brain, online, offline = brain_status()
            total, unavail, domains = ha_status()
            svcs = subprocess.run(["systemctl","list-units","argos-*","--no-pager","--no-legend","--state=active"],
                capture_output=True, text=True, timeout=5).stdout
            active_count = len([l for l in svcs.split('\n') if 'active' in l])

            # Читаем метрики watchdog из файла
            wm = {}
            try:
                wm = json.load(open("/tmp/argos_watchdog_metrics.json"))
            except:
                wm = {}

            msg_text = (
                f"*ARGOS Status* `{ts}`\n\n"
                f"🧠 *Brain*: {brain}\n"
                f"🏠 *Home Assistant*: {total} entities, {len(unavail)} unavailable\n"
                f"🔧 *Services*: {active_count} active\n"
                f"⚕️ *Watchdog*: healing={wm.get('heals', '?')}, errors={wm.get('errors', '?')}\n"
            )
            if domains:
                msg_text += f"\n⚠️ Unavailable domains: {', '.join(f'{k}({v})' for k,v in list(domains.items())[:5])}"
            send(chat_id, msg_text)

        elif t == "/unavail":
            total, unavail, domains = ha_status()
            if not unavail:
                send(chat_id, "✅ Все entities доступны!")
            else:
                lines = [f"❌ {u['entity_id']}: {u['state']}" for u in unavail[:15]]
                send(chat_id, f"*Недоступные entities ({len(unavail)})*\n\n" + "\n".join(lines))

        elif t == "/hard_heal":
            log_text = get_watchdog_log()
            send(chat_id, f"*Последние события healing*\n\n```\n{log_text}\n```")

        elif t == "/nodes":
            brain, online, offline = brain_status()
            msg_text = f"*Brain Nodes*\n\n✅ Online ({len(online)}):\n" + "\n".join(f"  • {n}" for n in online[:10])
            if offline:
                msg_text += f"\n\n❌ Offline ({len(offline)}):\n" + "\n".join(f"  • {n}" for n in offline[:10])
            send(chat_id, msg_text)

    time.sleep(1)