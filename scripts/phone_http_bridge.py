"""HTTP receiver для статистики телефона → публикует в MQTT"""
import os, json, time, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

MQTT_HOST = "localhost"
PORT = 7878

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            for key, val in data.items():
                topic = f"argos/phone/{key}"
                subprocess.run(["mosquitto_pub","-h",MQTT_HOST,"-t",topic,"-m",str(val)],
                    capture_output=True)
            ts = time.strftime("%H:%M:%S")
            print(f"[{ts}] Phone → MQTT: {list(data.keys())}")
        except Exception as e:
            print(f"Error: {e}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({"status":"argos_phone_bridge","mqtt":MQTT_HOST}).encode())

if __name__ == "__main__":
    print(f"Phone HTTP bridge started on 0.0.0.0:{PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


# Дополнительный эндпоинт — прокси к телефону
PHONE_AGENT_URL = "http://192.168.1.149:7788"

class PhoneProxy(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        import urllib.request as _ur
        path = self.path  # /status, /screenshot, /cmd etc
        try:
            r = _ur.urlopen(f"{PHONE_AGENT_URL}{path}", timeout=8)
            data = r.read()
            self.send_response(200)
            self.send_header("Content-Type", r.headers.get("Content-Type","application/json"))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f'{{"error":"{e}"}}'.encode())

    def do_POST(self):
        import urllib.request as _ur
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            req = _ur.Request(f"{PHONE_AGENT_URL}/cmd", data=body,
                              headers={"Content-Type": "application/json"})
            r = _ur.urlopen(req, timeout=30)
            data = r.read()
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f'{{"error":"{e}"}}'.encode())
