#!/usr/bin/env python3
"""
ARGOS Termux Agent v2 — запускается на телефоне (Termux).

Возможности:
- Регистрирует телефон в Brain API
- Регистрирует в Trust (Veto) с capabilities
- Публикует hardware capabilities (sensors, GPS, camera)
- Отправляет heartbeats каждые 30 сек
- Принимает команды от Brain (через polling или push)
- Репортит health метрики

Endpoints (HTTP server на порту 7890):
  GET  /status         — статус агента
  POST /cmd            — выполнить shell команду
  GET  /sensors        — данные сенсоров
  GET  /location       — GPS
  POST /brain/heartbeat— отправить heartbeat в Brain
  POST /brain/caps     — обновить capabilities
"""
import os
import sys
import json
import time
import threading
import subprocess
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PROJECT_ROOT = Path("/home/ava/Projects/argoss")


def get_termux_info():
    """Получить информацию о Termux и устройстве."""
    info = {
        "platform": "android",
        "termux": True,
    }
    
    # Termux version
    try:
        with open("/data/data/com.termux/files/usr/VERSION") as f:
            info["termux_version"] = f.read().strip()
    except:
        info["termux_version"] = "unknown"
    
    # Android version
    try:
        out = subprocess.run(
            ["getprop", "ro.build.version.release"],
            capture_output=True, text=True, timeout=5
        )
        info["android_version"] = out.stdout.strip()
    except:
        pass
    
    # Device model
    try:
        out = subprocess.run(
            ["getprop", "ro.product.model"],
            capture_output=True, text=True, timeout=5
        )
        info["device_model"] = out.stdout.strip()
    except:
        pass
    
    # Device name
    try:
        out = subprocess.run(
            ["getprop", "ro.product.device"],
            capture_output=True, text=True, timeout=5
        )
        info["device_name"] = out.stdout.strip()
    except:
        pass
    
    # Battery
    try:
        out = subprocess.run(
            ["termux-battery-status"],
            capture_output=True, text=True, timeout=5
        )
        info["battery"] = json.loads(out.stdout)
    except:
        info["battery"] = {}
    
    # IP
    try:
        out = subprocess.run(
            ["ip", "addr", "show", "wlan0"],
            capture_output=True, text=True, timeout=5
        )
        import re
        m = re.search(r'inet\s+(\S+)', out.stdout)
        if m:
            info["ip"] = m.group(1)
    except:
        pass
    
    return info


def get_capabilities():
    """Определить capabilities телефона."""
    caps = ["android", "phone", "termux"]
    
    # Termux API
    for api in ["termux-battery-status", "termux-location", "termux-sensor", 
                "termux-camera-photo", "termux-sms-list", "termux-contact-list"]:
        try:
            r = subprocess.run(["which", api], capture_output=True, text=True, timeout=3)
            if r.stdout.strip():
                cap = api.replace("termux-", "")
                caps.append(cap)
        except:
            pass
    
    # Camera
    if os.path.exists("/dev/video0"):
        caps.append("camera")
    
    # GPS
    if "location" in caps:
        caps.append("gps")
    
    return list(set(caps))


def send_heartbeat(brain_url: str, node_id: str, caps: list):
    """Отправить heartbeat в Brain."""
    info = get_termux_info()
    
    data = json.dumps({
        "node_id": node_id,
        "status": "online",
        "capabilities": caps,
        "meta": {
            "device_model": info.get("device_model"),
            "android_version": info.get("android_version"),
            "battery": info.get("battery", {}).get("percentage", 0),
            "termux": True,
            "ip": info.get("ip"),
        }
    }).encode()
    
    try:
        req = urllib.request.Request(
            f"{brain_url}/brain/register",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"_error": str(e)}


def register_in_trust(node_id: str, audit_url: str = "http://192.168.1.53:5010"):
    """Регистрация в Trust (Veto)."""
    data = json.dumps({"node_id": node_id, "capabilities": get_capabilities()}).encode()
    try:
        req = urllib.request.Request(
            f"{audit_url}/trust/{node_id}/evidence",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"_error": str(e)}


class TermuxHandler(BaseHTTPRequestHandler):
    """HTTP handler для команд от Brain."""
    
    def do_GET(self):
        if self.path == "/status":
            info = get_termux_info()
            info["capabilities"] = get_capabilities()
            self.respond(200, info)
        elif self.path == "/sensors":
            try:
                out = subprocess.run(
                    ["termux-sensor", "-l"],
                    capture_output=True, text=True, timeout=10
                )
                self.respond(200, {"sensors": out.stdout})
            except Exception as e:
                self.respond(500, {"error": str(e)})
        elif self.path == "/location":
            try:
                out = subprocess.run(
                    ["termux-location"],
                    capture_output=True, text=True, timeout=15
                )
                self.respond(200, json.loads(out.stdout))
            except Exception as e:
                self.respond(500, {"error": str(e)})
        else:
            self.respond(404, {"error": "not found"})
    
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode() if length else "{}"
        
        if self.path == "/cmd":
            try:
                data = json.loads(body)
                cmd = data.get("cmd", "")
                out = subprocess.run(
                    cmd, shell=True,
                    capture_output=True, text=True, timeout=30
                )
                self.respond(200, {"stdout": out.stdout, "stderr": out.stderr})
            except Exception as e:
                self.respond(500, {"error": str(e)})
        elif self.path == "/brain/heartbeat":
            # Trigger heartbeat
            data = json.loads(body)
            r = send_heartbeat(
                data.get("brain_url", "http://192.168.1.53:5001"),
                data.get("node_id", "argos-phone-termux"),
                get_capabilities()
            )
            self.respond(200, r)
        elif self.path == "/brain/caps":
            self.respond(200, {"capabilities": get_capabilities()})
        else:
            self.respond(404, {"error": "not found"})
    
    def respond(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def log_message(self, format, *args):
        print(f"  [HTTP] {args}")


def heartbeat_loop(brain_url: str, node_id: str, interval: int = 30):
    """Background thread для heartbeat."""
    caps = get_capabilities()
    while True:
        try:
            r = send_heartbeat(brain_url, node_id, caps)
            if "_error" not in r:
                print(f"  [HB] OK ({time.strftime('%H:%M:%S')})")
            else:
                print(f"  [HB] FAIL: {r['_error']}")
        except Exception as e:
            print(f"  [HB] ERR: {e}")
        time.sleep(interval)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--brain", default="http://192.168.1.53:5001")
    parser.add_argument("--audit", default="http://192.168.1.53:5010")
    parser.add_argument("--node-id", default="argos-phone-termux")
    parser.add_argument("--port", type=int, default=7890)
    parser.add_argument("--no-server", action="store_true", help="Only register, no HTTP server")
    parser.add_argument("--no-heartbeat", action="store_true", help="No background heartbeat")
    args = parser.parse_args()
    
    print("="*70)
    print(f"  ARGOS Termux Agent v2 — {args.node_id}")
    print("="*70)
    
    # Info
    info = get_termux_info()
    caps = get_capabilities()
    
    print(f"\n  Device: {info.get('device_model', '?')}")
    print(f"  Android: {info.get('android_version', '?')}")
    print(f"  Termux: {info.get('termux_version', '?')}")
    print(f"  IP: {info.get('ip', '?')}")
    print(f"  Battery: {info.get('battery', {}).get('percentage', '?')}%")
    print(f"  Capabilities: {caps}")
    
    # Register in Brain
    print(f"\n  Registering in Brain ({args.brain})...")
    r = send_heartbeat(args.brain, args.node_id, caps)
    if "_error" not in r:
        print(f"  ✓ Brain: OK")
    else:
        print(f"  ✗ Brain: {r['_error']}")
    
    # Register in Trust
    print(f"  Registering in Trust ({args.audit})...")
    r = register_in_trust(args.node_id, args.audit)
    if "_error" not in r:
        print(f"  ✓ Trust: OK (conf={r.get('confidence', '?')})")
    else:
        print(f"  ✗ Trust: {r['_error']}")
    
    if args.no_server:
        print("\n  Done (no server mode)")
        return
    
    # Start heartbeat
    if not args.no_heartbeat:
        t = threading.Thread(
            target=heartbeat_loop,
            args=(args.brain, args.node_id, 30),
            daemon=True
        )
        t.start()
        print(f"\n  Heartbeat thread started (30s interval)")
    
    # Start HTTP server
    server = HTTPServer(("0.0.0.0", args.port), TermuxHandler)
    print(f"\n  HTTP server listening on :{args.port}")
    print(f"    GET  /status")
    print(f"    GET  /sensors")
    print(f"    GET  /location")
    print(f"    POST /cmd")
    print(f"    POST /brain/heartbeat")
    print(f"    POST /brain/caps")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped")


if __name__ == "__main__":
    main()
