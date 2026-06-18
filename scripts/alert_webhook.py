#!/usr/bin/env python3
"""
AlertManager webhook → Obsidian alerts
Порт 19091
"""
import json, pathlib, datetime, http.server, threading, urllib.request, os, sys

VAULT      = pathlib.Path.home() / "Documents/MyObsidianVault"
ALERTS_DIR = VAULT / "SharedMemory/entities/alerts"
ENV_PATH   = pathlib.Path.home() / "Projects/argoss/.env"
TOKEN      = CHAT    = None

def load_env():
    global TOKEN, CHAT
    for line in ENV_PATH.read_text(errors="replace").splitlines():
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            TOKEN = line.split("=",1)[1].strip()
        elif line.startswith("ENTITY_COUNCIL_GROUP_ID="):
            CHAT = line.split("=",1)[1].strip()

def send_tg(text: str):
    if not TOKEN or not CHAT:
        return
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data=json.dumps({"chat_id": CHAT, "text": text[:4000], "parse_mode": "HTML"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        print(f"TG webhook failed: {e}")

def write_obsidian(alerts: list):
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now()
    fname = f"{now.strftime('%Y-%m-%d-%H%M')}_alert.md"
    lines = [f"# 🚨 ARGOS Alert {now.strftime('%Y-%m-%d %H:%M')}\n"]
    for a in alerts:
        status = a.get("status","firing")
        labels = a.get("labels",{})
        annot  = a.get("annotations",{})
        sev    = labels.get("severity","unknown")
        name   = labels.get("alertname","unknown")
        summary= annot.get("summary","")
        icon   = "🔴" if status=="firing" else "🟢"
        lines.append(f"## {icon} {name} ({sev})")
        lines.append(f"- **status**: {status}")
        lines.append(f"- **summary**: {summary}")
        lines.append(f"- **started**: {a.get('startsAt','')}")
        lines.append("")
    path = ALERTS_DIR / fname
    path.write_text("\n".join(lines), encoding="utf-8")
    return fname

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length',0))
        body = self.rfile.read(length)
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')
        try:
            data = json.loads(body)
            alerts = data.get("alerts",[])
            if not alerts:
                return
            fname = write_obsidian(alerts)
            text = f"🚨 ARGOS Alert ({len(alerts)} alerts) → {fname}"
            send_tg(text)
            print(f"[ALERT] {text}")
        except Exception as e:
            print(f"Webhook parse error: {e}")

    def log_message(self, fmt, *args):
        pass

def run():
    load_env()
    srv = http.server.HTTPServer(("0.0.0.0", 19091), Handler)
    print("[AlertWebhook]listening on :19091")
    srv.serve_forever()

if __name__ == "__main__":
    run()
