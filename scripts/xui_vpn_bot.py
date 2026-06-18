#!/usr/bin/env python3
"""
ARGOS VPN Bot (@argoossso_vpn_bot) — статус панелей 3x-ui и трафик клиентов.
Команды: /start /help /id /status /usage /panels
"""
import os, re, json, time, urllib.request
from datetime import datetime

ENV = open('/home/ava/Projects/argoss/.env').read()
def env(name, default=""):
    m = re.search(rf'^{name}=([^\n]*)$', ENV, re.M)
    return m.group(1).strip() if m else default

TOKEN = env("XUI_BOT_TOKEN")
if not TOKEN:
    print("⚠️  XUI_BOT_TOKEN не найден в .env"); exit(1)

PANEL_URL = env("XUI_PANEL_URL", "https://3x-ui-production-ca87.up.railway.app")
API_KEY = env("XUI_API_KEY")

# Все известные узлы 3x-ui
PANELS = {
    "Railway": PANEL_URL,
    "GCP-Asia": "http://35.201.181.205:2053",
    "GCP-EU": "http://34.77.207.14:2053",
}

def panel_status(url):
    try:
        req = urllib.request.Request(url + "/", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return f"🟢 онлайн (HTTP {r.status})"
    except Exception as e:
        return f"🔴 недоступна ({e})"

def api_get(path):
    """GET к API панели через Bearer API key (только Railway)."""
    try:
        req = urllib.request.Request(PANEL_URL + path, headers={"Authorization": f"Bearer {API_KEY}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.load(r)
    except Exception as e:
        return {"success": False, "msg": str(e)}

def fmt_bytes(n):
    n = float(n)
    for unit in ("Б", "КБ", "МБ", "ГБ", "ТБ"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} ПБ"

def usage_report():
    data = api_get("/panel/api/inbounds/list")
    if not data.get("success"):
        return f"❌ Не удалось получить данные: {data.get('msg')}"
    lines = ["*Трафик VPN-клиентов (Railway)*\n"]
    for inbound in data.get("obj", []):
        remark = inbound.get("remark", "?")
        lines.append(f"📡 *{remark}* (порт {inbound.get('port')})")
        for c in inbound.get("clientStats", []):
            up = fmt_bytes(c.get("up", 0))
            down = fmt_bytes(c.get("down", 0))
            total = c.get("total", 0)
            limit = fmt_bytes(total) if total else "∞"
            status = "✅" if c.get("enable") else "⛔"
            lines.append(f"  {status} `{c.get('email')}` — ↑{up} / ↓{down} (лимит: {limit})")
        lines.append("")
    return "\n".join(lines)

def panels_report():
    lines = ["*Статус VPN-панелей*\n"]
    for name, url in PANELS.items():
        lines.append(f"🌐 {name}: {url}\n   {panel_status(url)}")
    lines.append("\n⚠️ GCP-узлы: порты 2053/443/2096 пока закрыты файрволом (ждём включения billing в GCP)")
    return "\n".join(lines)

def send(chat_id, text):
    body = json.dumps({"chat_id": chat_id, "text": str(text)[:4000], "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try: urllib.request.urlopen(req, timeout=8)
    except Exception as e: print("send error:", e)

def get_updates(offset=0):
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=20&limit=10")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("result", [])
    except Exception as e:
        print("getUpdates error:", e)
        return []

print("🤖 ARGOS VPN Bot (@argoossso_vpn_bot) запущен")
offset = 0

while True:
    for upd in get_updates(offset):
        offset = max(offset, upd["update_id"] + 1)
        msg = upd.get("message", {})
        text = msg.get("text", "")
        chat = msg.get("chat", {})
        chat_id = chat.get("id", 0)
        user = msg.get("from", {})
        if not text:
            continue
        t = text.lower().strip()
        ts = datetime.now().strftime("%H:%M")

        if t in ("/start", "/help"):
            send(chat_id,
                "*ARGOS VPN Bot* 🛡️\n\n"
                "Бот панелей 3x-ui (Xray VPN)\n\n"
                "Команды:\n"
                "/status — статус основной панели (Railway)\n"
                "/panels — статус всех узлов (Railway + GCP Asia/EU)\n"
                "/usage — трафик VPN-клиентов\n"
                "/id — твой Telegram ID\n"
                "/help — это сообщение")

        elif t == "/id":
            send(chat_id, f"Твой chat_id: `{chat_id}`\nuser_id: `{user.get('id')}`\nusername: @{user.get('username','—')}")

        elif t == "/status":
            send(chat_id,
                f"*VPN Panel Status* `{ts}`\n\n"
                f"🌐 {PANEL_URL}\n"
                f"Статус: {panel_status(PANEL_URL)}")

        elif t == "/panels":
            send(chat_id, panels_report())

        elif t == "/usage":
            send(chat_id, usage_report())

        else:
            send(chat_id, "Не знаю такую команду. /help — список команд")

    time.sleep(1)
