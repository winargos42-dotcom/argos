#!/usr/bin/env python3
"""
Remote Shell Gate — API для команд на удалённых узлах.
POST /exec/{node} с секретом → выполняет команду через SSH.
Доступ ТОЛЬКО localhost.
"""
import subprocess, json, os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 7778
SECRET = os.environ.get("ARGOS_GATE_SECRET", "valenok_gate")

# Конфиг узлов (SSH ключи уже настроены)
NODES = {
    "orion": {"host": "192.168.1.53", "user": "AvA", "key": "/home/ava/.ssh/id_ed25519"},
    "opi":   {"host": "192.168.2.168", "user": "root", "key": "/home/ava/.ssh/id_ed25519"},
}

class GateHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    def log_message(self, fmt, *args): pass
    
    def do_POST(self):
        if self.client_address[0] != "127.0.0.1":
            self.send_json(403, {"error": "localhost only"})
            return
        
        # /exec/{node}
        path = self.path
        if not path.startswith("/exec/"):
            self.send_json(404, {"error": "use /exec/{node}"})
            return
        
        node = path.split("/")[-1]
        if node not in NODES:
            self.send_json(404, {"error": f"unknown node: {node}"})
            return
        
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        try:
            data = json.loads(body) if body else {}
        except:
            self.send_json(400, {"error": "invalid JSON"})
            return
        
        if data.get("secret") != SECRET:
            self.send_json(403, {"error": "invalid secret"})
            return
        
        cmd = data.get("cmd", "")
        if not cmd:
            self.send_json(400, {"error": "no cmd"})
            return
        
        # Блокировка опасных команд
        FORBIDDEN = ["rm -rf /", "mkfs", "dd if=/dev/zero", "> /dev/sda", "shutdown", "reboot"]
        for f in FORBIDDEN:
            if f in cmd:
                self.send_json(403, {"error": f"forbidden: {f}"})
                return
        
        nc = NODES[node]
        ssh_cmd = ["ssh", "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=no",
            "-i", nc["key"], f"{nc['user']}@{nc['host']}", cmd]
        
        try:
            r = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)
            stdout = r.stdout.strip()
            stderr = r.stderr.strip()
            # Фильтруем SSH warnings
            clean_lines = [l for l in stderr.splitlines() if "post-quantum" not in l.lower() and "warning" not in l.lower()]
            clean_err = "\n".join(clean_lines)[:500]
            
            self.send_json(200, {
                "node": node,
                "cmd": cmd,
                "exit_code": r.returncode,
                "stdout": stdout[:2000],
                "stderr": clean_err
            })
        except subprocess.TimeoutExpired:
            self.send_json(504, {"error": "SSH timeout"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})
    
    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "armed", "port": PORT, "nodes": list(NODES)})
        else:
            self.send_json(404, {"error": "not found"})

if __name__ == "__main__":
    print(f"[GATE] Armed on :{PORT} (localhost only)")
    HTTPServer(("127.0.0.1", PORT), GateHandler).serve_forever()
