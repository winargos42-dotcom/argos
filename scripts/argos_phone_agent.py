"""ARGOS Phone Agent — программный интерфейс к телефону.

Работает на ноутбуке. Предоставляет REST API для управления телефоном,
Colibri P2P node, и публикации в Brain.

Endpoints:
  GET  /status          — статус агента и телефона
  POST /phone/cmd       — команда телефону (screenshot/tap/app/text/key)
  GET  /phone/screen    — скриншот + Gemini анализ
  POST /brain/register  — регистрация в Brain
  GET  /colibri/status  — статус Colibri ноды
  POST /evolution       — запуск evolution цикла
"""
import os, sys, json, time, subprocess, base64, urllib.request, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, '/home/ava/Projects/argoss')
from dotenv import load_dotenv
load_dotenv('/home/ava/Projects/argoss/.env')

PHONE = os.getenv("PHONE_ADB_IP", "192.168.1.149:5555")
BRAIN = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
GCP   = os.getenv("ARGOS_GCP_URL", "https://argos-core-m3gk27ccqa-uc.a.run.app")
PORT  = int(os.getenv("PHONE_AGENT_PORT", "7880"))
START = time.time()

# auto-detect USB device if WiFi ADB offline
import re as _re
def _resolve_device():
    try:
        out = subprocess.run("adb devices", shell=True, capture_output=True, text=True, timeout=5).stdout
        m = _re.search(r'^(\w+)\s+device$', out, _re.M)
        if m:
            return m.group(1)
    except: pass
    return PHONE

def adb(cmd: str) -> str:
    dev = _resolve_device()
    try:
        r = subprocess.run(f"adb -s {dev} {cmd}",
            shell=True, capture_output=True, text=True, timeout=15)
        return r.stdout.strip()
    except: return "error"

def adb_shell(cmd: str) -> str:
    return adb(f'shell "{cmd}"')

def phone_status() -> dict:
    bat = adb_shell("dumpsys battery | grep level | tr -dc '0-9'")
    temp_raw = adb_shell("dumpsys battery | grep temperature | tr -dc '0-9'")
    mem_a = adb_shell("cat /proc/meminfo | grep MemAvailable | awk '{print $2}'")
    mem_t = adb_shell("cat /proc/meminfo | grep MemTotal | awk '{print $2}'")
    cpu   = adb_shell("cat /proc/loadavg | awk '{print $1}'")
    ip    = adb_shell("ip addr show wlan0 | grep 'inet ' | awk '{print $2}'").split("/")[0]
    focus = adb_shell("dumpsys window | grep mCurrentFocus | head -1")
    
    def safe_int(s): 
        s = s.strip()
        return int(s) if s.lstrip('-').isdigit() else 0

    ram = round((safe_int(mem_t)-safe_int(mem_a))/max(safe_int(mem_t),1)*100, 1)
    return {
        "battery": safe_int(bat), "temp": round(safe_int(temp_raw)/10,1),
        "ram_pct": ram, "cpu_load": cpu, "wifi_ip": ip,
        "screen": focus.split()[-1] if focus else "?",
        "connected": "device" in adb("get-state")
    }

def screenshot_b64() -> tuple[str, str]:
    adb("shell screencap -p /sdcard/a.png")
    adb("pull /sdcard/a.png /tmp/phone_agent.png")
    try:
        img = open("/tmp/phone_agent.png","rb").read()
        b64 = base64.b64encode(img).decode()
        # Gemini vision
        body = json.dumps({"contents":[{"parts":[
            {"text":"Что видно на Android экране? Кратко на русском."},
            {"inline_data":{"mime_type":"image/png","data":b64}}
        ]}]}).encode()
        req = urllib.request.Request(
            f"{GCP}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
            data=body, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            desc = d["candidates"][0]["content"]["parts"][0]["text"][:300] if "candidates" in d else "?"
        return b64, desc
    except Exception as e:
        return "", f"vision error: {e}"

def brain_register():
    import requests
    try:
        requests.post(f"{BRAIN}/brain/register", json={
            "node_id": "argos-phone-agent",
            "address": f"192.168.1.53:{PORT}",
            "capabilities": ["phone","adb","vision","android","camera","gps"],
            "meta": {"device": "Redmi Note 8T", "os": "Android 14"}
        }, timeout=3)
    except: pass

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send_json(self, data: dict, code: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/status":
            ps = phone_status()
            self.send_json({
                "agent": "argos-phone-agent",
                "uptime": round(time.time()-START),
                "phone": ps,
                "brain": BRAIN,
                "port": PORT
            })
        elif p == "/phone/screen":
            b64, desc = screenshot_b64()
            self.send_json({"description": desc, "image_b64": b64[:100]+"..."})
        elif p == "/colibri/status":
            log = "/var/log/argos_colibri.log"
            last = open(log).readlines()[-3:] if os.path.exists(log) else []
            self.send_json({"status":"active","log":last})
        else:
            self.send_json({"endpoints":["/status","/phone/screen","/phone/cmd","/colibri/status","/evolution"]})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        p = self.path.split("?")[0]

        if p == "/phone/cmd":
            cmd = body.get("cmd","")
            result = self._execute_phone_cmd(cmd, body)
            self.send_json({"result": result, "cmd": cmd})

        elif p == "/evolution":
            # Запускаем evolution цикл в фоне
            threading.Thread(target=self._run_evolution, daemon=True).start()
            self.send_json({"status":"evolution started"})

        elif p == "/brain/register":
            brain_register()
            self.send_json({"status":"registered"})
        else:
            self.send_json({"error":"unknown"}, 404)

    def _execute_phone_cmd(self, cmd: str, body: dict) -> str:
        APPS = {"telegram":"org.telegram.messenger/.DefaultIcon",
                "chrome":"com.android.chrome/com.google.android.apps.chrome.Main",
                "youtube":"com.google.android.youtube/com.google.android.youtube.HomeActivity",
                "maps":"com.google.android.apps.maps/com.google.android.maps.MapsActivity",
                "camera":"android.hardware.Camera",
                "connectbot":"org.connectbot/.HostListActivity",
                "ssh":"org.connectbot/.HostListActivity"}
        cmd = cmd.lower().strip()
        if cmd == "screenshot":
            _, desc = screenshot_b64()
            return f"📸 {desc}"
        elif cmd == "status":
            s = phone_status()
            return f"📱 bat={s['battery']}% temp={s['temp']}°C ram={s['ram_pct']}% cpu={s['cpu_load']}"
        elif cmd == "tap":
            adb_shell(f"input tap {body.get('x',0)} {body.get('y',0)}")
            return f"Нажал ({body.get('x')},{body.get('y')})"
        elif cmd == "text":
            t = body.get("text","").replace("'","\\'").replace(" ","%s")
            adb_shell(f"input text '{t}'")
            return "Напечатано"
        elif cmd == "key":
            keys={"home":"3","back":"4","enter":"66","volume_up":"24","volume_down":"25","power":"26"}
            adb_shell(f"input keyevent {keys.get(body.get('key','home'),'3')}")
            return f"Кнопка: {body.get('key')}"
        elif cmd == "app":
            app = body.get("app","").lower()
            pkg = APPS.get(app)
            if pkg: adb_shell(f"am start -n {pkg}")
            return f"Открыто: {app}" if pkg else f"Неизвестно: {app}"
        elif cmd == "swipe":
            adb_shell(f"input swipe {body.get('x1',0)} {body.get('y1',0)} {body.get('x2',0)} {body.get('y2',0)} {body.get('duration',500)}")
            return "Свайп выполнен"
        elif cmd == "call":
            adb_shell(f"am start -a android.intent.action.CALL -d tel:{body.get('number','')}")
            return f"Звоним: {body.get('number')}"
        return f"Неизвестная команда: {cmd}"

    def _run_evolution(self):
        import requests
        try:
            r = requests.post(f"http://localhost:8000/ask",
                json={"prompt":"Эволюция: как телефон-агент может развить ARGOS?"},
                timeout=30)
            if r.ok:
                resp = r.json().get("response","")[:200]
                requests.post("http://localhost:1883", 
                    headers={"Content-Type":"application/json"},
                    json={"topic":"argos/evolution/phone","payload":resp})
        except: pass

if __name__ == "__main__":
    import socket as _socket
    HTTPServer.allow_reuse_address = True
    brain_register()
    print(f"🐦 ARGOS Phone Agent v1.0 on 0.0.0.0:{PORT}")
    ps = phone_status()
    print(f"📱 Phone: bat={ps['battery']}% connected={ps['connected']}")
    srv = HTTPServer(("0.0.0.0", PORT), Handler)
    srv.serve_forever()
