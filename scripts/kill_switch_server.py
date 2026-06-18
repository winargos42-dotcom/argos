#!/usr/bin/env python3
"""
Kill Switch Server — аварийная остановка всего ARGOS.
POST /kill с правильным токеном → останавливает все сервисы.
Порт 7777, доступ ТОЛЬКО с localhost (/127.0.0.1).
"""
import os, sys, subprocess, json
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 7777
# Читаем секрет из .env.docker
SECRET = os.environ.get("ARGOS_KILL_SECRET", "valenok_death")

SERVICES = [
    "argos-entity-bus", "argos-entity-council", "argos-valenok",
    "argos-control-plane", "autopilot_v3", "argos-hive",
    "argos-curiosity", "argos-auto-tasker", "argos-memory",
    "argos-idea-scorer", "argos-meta-tasker", "argos-ab-test",
    "argos-survival"
]

class KillHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, fmt, *args):
        # Тихий лог
        pass
    
    def do_POST(self):
        client = self.client_address[0]
        if client not in ("127.0.0.1", "::1", "localhost"):
            self.send_json(403, {"error": "localhost only"})
            return
        
        if self.path != "/kill":
            self.send_json(404, {"error": "not found"})
            return
        
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        if data.get("secret") != SECRET:
            self.send_json(403, {"error": "invalid secret"})
            return
        
        # Консенсус перед убийством
        log("Requesting consensus for KILL...")
        try:
            import consensus_vote
            passed, votes = consensus_vote.vote_on_action(f"kill_switch from {client}")
            if not passed:
                self.send_json(403, {"error": "consensus blocked", "votes": votes})
                log("KILL BLOCKED by consensus")
                return
        except Exception as e:
            log(f"Consensus error: {e} — proceeding anyway (danger zone)")
        
        # KILL SEQUENCE
        results = {}
        for svc in SERVICES:
            r = subprocess.run(["sudo", "systemctl", "stop", svc],
                capture_output=True, text=True, timeout=10)
            results[svc] = "stopped" if r.returncode == 0 else f"err: {r.stderr[:50]}"
        
        # Убиваем процесс autopilot_v3 если он в screen
        subprocess.run(["pkill", "-f", "autopilot_v3.py"], capture_output=True)
        
        self.send_json(200, {
            "status": "ARGOS HALTED",
            "stopped": results,
            "secret_ok": True
        })
    
    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "armed", "port": PORT})
        else:
            self.send_json(404, {"error": "not found"})

if __name__ == "__main__":
    print(f"[KILL-SWITCH] Armed on :{PORT} (localhost only)")
    srv = HTTPServer(("127.0.0.1", PORT), KillHandler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("[KILL-SWITCH] Shutdown")
