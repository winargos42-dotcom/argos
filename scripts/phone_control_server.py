"""HTTP API сервер для управления телефоном через ADB (запускается на ноутбуке)."""
import subprocess, json, time, os, base64
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 7879
PHONE_IP = os.getenv("PHONE_ADB_IP", "192.168.1.149:5555")

def adb(cmd):
    try:
        r = subprocess.run(f"adb -s {PHONE_IP} {cmd}", shell=True,
            capture_output=True, text=True, timeout=15)
        return r.stdout.strip()
    except:
        return "error"

def adb_shell(cmd):
    return adb(f'shell "{cmd}"')

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        cmd = body.get("cmd", "")
        result = self._handle(cmd, body)
        resp = json.dumps({"result": result, "ok": True}, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(resp)

    def _handle(self, cmd, body):
        cmd = cmd.lower().strip()

        if cmd in ("status", "статус"):
            bat = adb_shell("dumpsys battery | grep level | tr -dc '0-9'")
            temp_raw = adb_shell("dumpsys battery | grep temperature | tr -dc '0-9'")
            temp = round(int(temp_raw)/10, 1) if temp_raw.isdigit() else 0
            mem_a = adb_shell("cat /proc/meminfo | grep MemAvailable | awk '{print $2}'")
            mem_t = adb_shell("cat /proc/meminfo | grep MemTotal | awk '{print $2}'")
            cpu = adb_shell("cat /proc/loadavg | awk '{print $1}'")
            ram = round((1 - int(mem_a)/int(mem_t))*100, 1) if mem_a.isdigit() and mem_t.isdigit() else 0
            return (f"📱 Redmi Note 8T\n"
                    f"🔋 {bat}% 🌡 {temp}°C\n"
                    f"💾 RAM: {ram}% ⚙️ CPU: {cpu}")

        elif cmd in ("screenshot", "скрин", "скриншот"):
            adb("shell screencap -p /sdcard/s.png")
            adb("pull /sdcard/s.png /tmp/phone_s.png")
            # Vision via Gemini
            try:
                img = open("/tmp/phone_s.png","rb").read()
                b64 = base64.b64encode(img).decode()
                import urllib.request
                req_body = json.dumps({"contents":[{"parts":[
                    {"text":"Что видно на экране Android? Кратко на русском."},
                    {"inline_data":{"mime_type":"image/png","data":b64}}
                ]}]}).encode()
                gcp = os.getenv("ARGOS_GCP_URL","https://argos-core-m3gk27ccqa-uc.a.run.app")
                req = urllib.request.Request(
                    f"{gcp}/proxy/gemini/v1/models/gemini-2.5-flash:generateContent",
                    data=req_body, headers={"Content-Type":"application/json"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    d = json.loads(r.read())
                    desc = d["candidates"][0]["content"]["parts"][0]["text"][:200] if "candidates" in d else "?"
                return f"📸 Скриншот:\n🔍 {desc}"
            except Exception as e:
                return f"📸 Скриншот сделан (vision error: {e})"

        elif cmd == "tap":
            x, y = body.get("x",0), body.get("y",0)
            adb_shell(f"input tap {x} {y}")
            return f"Нажал ({x},{y})"

        elif cmd == "text":
            text = body.get("text","").replace("'","\\'")
            adb_shell(f"input text '{text}'")
            return f"Напечатано"

        elif cmd == "key":
            key = body.get("key","home")
            keys = {"home":"3","back":"4","enter":"66","volume_up":"24","volume_down":"25"}
            adb_shell(f"input keyevent {keys.get(key,key)}")
            return f"Кнопка: {key}"

        elif cmd == "app":
            apps = {"telegram":"org.telegram.messenger/.DefaultIcon",
                    "chrome":"com.android.chrome/com.google.android.apps.chrome.Main",
                    "youtube":"com.google.android.youtube/com.google.android.youtube.HomeActivity",
                    "maps":"com.google.android.apps.maps/com.google.android.maps.MapsActivity"}
            app = body.get("app","").lower()
            pkg = apps.get(app)
            if pkg:
                adb_shell(f"am start -n {pkg}")
                return f"Открыто: {app}"
            return f"Неизвестное приложение: {app}"

        elif cmd == "call":
            num = body.get("number","")
            adb_shell(f"am start -a android.intent.action.CALL -d tel:{num}")
            return f"Звоним: {num}"

        return f"Неизвестная команда: {cmd}"

    def do_GET(self):
        connected = adb("get-state")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({"status":"ok","phone":connected}).encode())

if __name__ == "__main__":
    print(f"Phone Control Server on 0.0.0.0:{PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
