#!/usr/bin/env python3
"""ARGOS Prometheus Exporter — RED методика: Rate, Errors, Duration"""
import sys, os, time, json, re, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

PROJECT_ROOT = os.path.expanduser("~/Projects/argoss")
sys.path.insert(0, PROJECT_ROOT)

# ── Метрики ───────────────────────────────────────────────
METRICS = {
    "argos_nodes_online": 0,
    "argos_nodes_total": 28,
    "argos_brain_api_up": 0,
    "argos_ha_entities_total": 0,
    "argos_ha_entities_active": 0,
    "argos_cpu_percent": 0.0,
    "argos_ram_percent": 0.0,
    "argos_disk_percent": 0.0,
    "argos_evolutions_total": 0,
    "argos_thoughts_total": 0,
    "argos_syntheses_total": 0,
    "argos_autopilot_msgs": 0,
    "argos_voice_connections": 0,
    "argos_cache_hit_ratio": 0.0,
}

def collect():
    """Сбор метрик из ARGOS системы"""
    import psutil
    # CPU / RAM / Disk
    METRICS["argos_cpu_percent"] = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    METRICS["argos_ram_percent"] = mem.percent
    disk = psutil.disk_usage("/")
    METRICS["argos_disk_percent"] = disk.percent

    # Brain API (PC)
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://192.168.1.66:5010/brain/nodes", timeout=5)
        data = json.loads(resp.read())
        nodes = data.get("nodes", [])
        on = sum(1 for n in nodes if n.get("status") == "online")
        METRICS["argos_nodes_online"] = on
        METRICS["argos_nodes_total"] = len(nodes)
        METRICS["argos_brain_api_up"] = 1
    except Exception:
        METRICS["argos_brain_api_up"] = 0

    # Consciousness
    try:
        cc = json.load(open(os.path.join(PROJECT_ROOT, "data/collective_consciousness.json")))
        METRICS["argos_thoughts_total"] = cc.get("total_thoughts", 0)
        METRICS["argos_syntheses_total"] = cc.get("total_syntheses", 0)
    except Exception:
        pass

    # Evolution
    try:
        el = json.load(open(os.path.join(PROJECT_ROOT, "data/evolution/metrics.json")))
        METRICS["argos_evolutions_total"] = el.get("total_reflections", 0)
    except Exception:
        pass

    # Cache
    try:
        from src.mcp.cache_layer import MCPCache
        c = MCPCache()
        METRICS["argos_cache_hit_ratio"] = c.hit_ratio
    except Exception:
        pass

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            collect()
            body = ""
            for k, v in METRICS.items():
                body += f"# TYPE {k} gauge\n{k} {v}\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.end_headers()
            self.wfile.write(body.encode())
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"up"}\n')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.getenv("ARGOS_PROMETHEUS_PORT", "9090"))
    srv = HTTPServer(("0.0.0.0", port), MetricsHandler)
    print(f"[PROMETHEUS] Listening on :{port}/metrics")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("[PROMETHEUS] Stopped")
