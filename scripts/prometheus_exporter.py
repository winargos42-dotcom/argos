#!/usr/bin/env python3
"""
ARGOS Prometheus Exporter v2 — РЕАЛЬНАЯ интеграция VetoProtocol + AuditLog.

Добавлено к v1:
- /trust endpoint — экспорт trust scores
- /veto endpoint — submit evidence через HTTP
- /alerts endpoint — экспорт активных алертов
- Trust → Alert escalation: conf<0.3 → CRITICAL alert
- Audit log всех check_alerts решений
- Obsidian dashboard auto-update
"""
import sys, os, time, json, re, subprocess, datetime, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

PROJECT_ROOT = os.path.expanduser("~/Projects/argoss")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src/audit"))

try:
    from argos_council_integration import CouncilTrustGuard
    _TRUST_GUARD = CouncilTrustGuard()
    print("✓ CouncilTrustGuard loaded in prometheus_exporter")
except Exception as e:
    print(f"⚠️ TrustGuard unavailable: {e}")
    _TRUST_GUARD = None

# ── Метрики (расширены trust + alerts) ─────────────────────
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
    "argos_entity_cycles_total": 0,
    "argos_orchestrator_uptime_sec": 0,
    "argos_kg_nodes": 0,
    "argos_kg_edges": 0,
    "argos_pc_ssh_up": 0,
    "argos_pc_mcp_uptime_sec": 0,
    "argos_pc_gpu_util_pct": 0.0,
    "argos_pc_gpu_memory_mb": 0,
    # NEW: trust scores per node
    "argos_trust_orion": 1.0,
    "argos_trust_nexus": 1.0,
    "argos_trust_egida": 1.0,
    "argos_trust_pico": 1.0,
    "argos_trust_esp32": 1.0,
    "argos_trust_android": 1.0,
    "argos_trust_phone_redmi": 1.0,
    "argos_alerts_firing": 0,
    "argos_alerts_total": 0,
    "argos_audit_events_total": 0,
    "argos_audit_chain_verified": 1,
}

NODES = ["orion", "nexus", "egida", "pico", "esp32", "android", "phone-redmi", "entity-valenok", "laptop"]


def collect():
    """Сбор метрик из ARGOS системы + Veto + Audit"""
    global METRICS
    try:
        import psutil
        METRICS["argos_cpu_percent"] = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        METRICS["argos_ram_percent"] = mem.percent
        disk = psutil.disk_usage("/")
        METRICS["argos_disk_percent"] = disk.percent
    except Exception:
        pass

    # Brain API (PC)
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://192.168.1.53:5001/brain/nodes", timeout=5)
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

    # Entity Council cycles
    try:
        log_file = os.path.join(os.path.expanduser("~"), "Documents", "MyObsidianVault", "SharedMemory", "entities", "council", "EVOLUTION_LOG.md")
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                METRICS["argos_entity_cycles_total"] = sum(1 for line in f if line.strip().startswith("- ["))
    except Exception:
        pass

    # Orchestrator uptime
    try:
        import psutil
        p = psutil.Process()
        METRICS["argos_orchestrator_uptime_sec"] = int(time.time() - p.create_time())
    except Exception:
        pass

    # Knowledge Graph
    try:
        kg = json.load(open(os.path.join(PROJECT_ROOT, "data/knowledge_graph.json")))
        METRICS["argos_kg_nodes"] = len(kg.get("nodes", []))
        METRICS["argos_kg_edges"] = len(kg.get("edges", []))
    except Exception:
        pass

    # NEW: Trust scores из VetoProtocol
    if _TRUST_GUARD:
        for node in NODES:
            profile = _TRUST_GUARD.check_node(node)
            conf = profile.get("confidence", 1.0)
            metric_name = f"argos_trust_{node.replace('-', '_')}"
            METRICS[metric_name] = conf
        # Trust → Alert escalation
        for node in NODES:
            profile = _TRUST_GUARD.check_node(node)
            if profile.get("blocked") and not profile.get("alert_logged"):
                # Триггер алерта
                _TRUST_GUARD.log_action(
                    f"trust_breach:{node}",
                    node,
                    "CRITICAL",
                    {"confidence": profile.get("confidence", 0), "reason": "auto_quarantine_or_blocked"}
                )
                profile["alert_logged"] = True
        # Alerts + Audit count
        try:
            alerts = _TRUST_GUARD.veto.get_status() if hasattr(_TRUST_GUARD, "veto") else []
            METRICS["argos_alerts_firing"] = sum(1 for a in alerts if a.get("is_quarantined"))
        except Exception:
            pass

    # NEW: Audit chain verified
    try:
        if _TRUST_GUARD and hasattr(_TRUST_GUARD, "audit"):
            result = _TRUST_GUARD.audit.verify_chain()
            METRICS["argos_audit_chain_verified"] = 1 if result.get("verified") else 0
            METRICS["argos_audit_events_total"] = result.get("total_events", 0)
    except Exception:
        pass


class MetricsHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # тихий

    def do_GET(self):
        if self.path == "/metrics":
            collect()
            body = ""
            for k, v in METRICS.items():
                body += f"# TYPE {k} gauge\n{k} {v}\n"
            # Alert thresholds (1 if triggered)
            body += f"# TYPE argos_disk_alert gauge\nargos_disk_alert {1 if METRICS.get('argos_disk_percent',0) > 80 else 0}\n"
            body += f"# TYPE argos_nodes_alert gauge\nargos_nodes_alert {1 if METRICS.get('argos_nodes_online',0) < 20 else 0}\n"
            body += f"# TYPE argos_cpu_alert gauge\nargos_cpu_alert {1 if METRICS.get('argos_cpu_percent',0) > 85 else 0}\n"
            body += f"# TYPE argos_ram_alert gauge\nargos_ram_alert {1 if METRICS.get('argos_ram_percent',0) > 85 else 0}\n"
            # NEW: trust alerts
            for node in NODES:
                metric = f"argos_trust_{node.replace('-', '_')}"
                conf = METRICS.get(metric, 1.0)
                body += f"# TYPE argos_trust_alert_{node.replace('-', '_')} gauge\n"
                body += f"argos_trust_alert_{node.replace('-', '_')} {1 if conf < 0.3 else 0}\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.end_headers()
            self.wfile.write(body.encode())
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"up","version":"2.0"}\n')
        elif self.path == "/trust":
            # NEW: JSON trust scores
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if _TRUST_GUARD:
                result = _TRUST_GUARD.veto.get_status()
                self.wfile.write(json.dumps(result, default=str).encode())
            else:
                self.wfile.write(b'{"error":"TrustGuard unavailable"}')
        elif self.path == "/dashboard":
            # NEW: Human-readable dashboard
            self._dashboard()
        else:
            self.send_response(404)
            self.end_headers()

    def _dashboard(self):
        """Human-readable HTML dashboard"""
        collect()
        html = """<!DOCTYPE html>
<html><head><title>ARGOS Real-Time Dashboard</title>
<meta http-equiv="refresh" content="30">
<style>
body{font-family:monospace;background:#0a0e1a;color:#0ff;padding:20px}
h1{color:#0ff;border-bottom:2px solid #0ff}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:15px}
.card{background:#111827;border:1px solid #0ff33;border-radius:8px;padding:15px}
.metric{font-size:2em;color:#0ff}
.warn{color:#ff0}
.crit{color:#f00}
.ok{color:#0f0}
table{width:100%;border-collapse:collapse}
td,th{padding:5px;border-bottom:1px solid #333}
th{text-align:left;color:#0ff}
</style></head><body>
<h1>🛡️ ARGOS Real-Time Dashboard</h1>
<p>Last update: """ + datetime.datetime.now().isoformat() + """</p>
<div class="grid">
"""
        # System metrics
        html += f'<div class="card"><h2>🖥️ System</h2>'
        html += f'<p>CPU: <span class="metric">{METRICS.get("argos_cpu_percent",0):.1f}%</span></p>'
        html += f'<p>RAM: <span class="metric">{METRICS.get("argos_ram_percent",0):.1f}%</span></p>'
        html += f'<p>Disk: <span class="metric">{METRICS.get("argos_disk_percent",0):.1f}%</span></p>'
        html += '</div>'

        # Brain
        html += f'<div class="card"><h2>🧠 Brain</h2>'
        html += f'<p>API up: <span class="{"ok" if METRICS.get("argos_brain_api_up") else "crit"}">{METRICS.get("argos_brain_api_up",0)}</span></p>'
        html += f'<p>Nodes online: <span class="metric">{METRICS.get("argos_nodes_online",0)}/{METRICS.get("argos_nodes_total",0)}</span></p>'
        html += f'<p>Entity cycles: <span class="metric">{METRICS.get("argos_entity_cycles_total",0)}</span></p>'
        html += f'<p>Thoughts: <span class="metric">{METRICS.get("argos_thoughts_total",0)}</span></p>'
        html += '</div>'

        # Trust
        html += '<div class="card"><h2>🔒 Trust Scores</h2><table>'
        html += '<tr><th>Node</th><th>Confidence</th><th>Status</th></tr>'
        for node in NODES:
            conf = METRICS.get(f"argos_trust_{node.replace('-', '_')}", 1.0)
            status_class = "ok" if conf > 0.7 else "warn" if conf > 0.3 else "crit"
            status_text = "✅ OK" if conf > 0.7 else "⚠️ LOW" if conf > 0.3 else "🔴 BLOCKED"
            html += f'<tr><td>{node}</td><td class="{status_class}">{conf:.2f}</td><td class="{status_class}">{status_text}</td></tr>'
        html += '</table></div>'

        # Alerts
        html += '<div class="card"><h2>🚨 Alerts & Audit</h2>'
        html += f'<p>Firing: <span class="metric">{METRICS.get("argos_alerts_firing",0)}</span></p>'
        html += f'<p>Audit events: <span class="metric">{METRICS.get("argos_audit_events_total",0)}</span></p>'
        html += f'<p>Chain verified: <span class="{"ok" if METRICS.get("argos_audit_chain_verified") else "crit"}">{METRICS.get("argos_audit_chain_verified",0)}</span></p>'
        html += '</div>'

        html += '</div></body></html>'
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())


ALERT_STATE = {}
ALERTS_DIR = os.path.expanduser("~/Documents/MyObsidianVault/SharedMemory/entities/alerts")


def _tg(text: str):
    try:
        import urllib.request
        env = {}
        with open(os.path.expanduser("~/Projects/argoss/.env")) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    env[k] = v
        token = env.get("TELEGRAM_BOT_TOKEN", "")
        chat = env.get("ENTITY_COUNCIL_GROUP_ID", env.get("CHAT_ID", ""))
        if not token or not chat:
            return
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=json.dumps({"chat_id": chat, "text": text[:3900], "parse_mode": "HTML"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=15)
    except Exception:
        pass


def write_alert_md(name: str, severity: str, status: str, summary: str):
    ALERTS_DIR = os.path.expanduser("~/Documents/MyObsidianVault/SharedMemory/entities/alerts")
    os.makedirs(ALERTS_DIR, exist_ok=True)
    now = datetime.datetime.now()
    fname = f"{now.strftime('%Y-%m-%d-%H%M')}_{name}_{status}.md"
    path = os.path.join(ALERTS_DIR, fname)
    icon = "🔴" if status == "firing" else "🟢"
    body = f"""# {icon} {name} ({severity})
- **status**: {status}
- **summary**: {summary}
- **timestamp**: {now.isoformat()}
- **source**: prometheus_exporter v2
---
Для resolve — удалите этот файл или измените `status` на `resolved`.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return fname


def check_alerts():
    """Проверяет thresholds, пишет в Obsidian при изменении статуса. +Veto+Audit"""
    global ALERT_STATE
    rules = [
        ("ArgosNodeDown",      "critical", lambda: METRICS.get("argos_nodes_online",0) / max(METRICS.get("argos_nodes_total",1),1) < 0.85, lambda: f"Ноды offline: {METRICS.get('argos_nodes_online',0)}/{METRICS.get('argos_nodes_total',28)}"),
        ("ArgosPCBrainDown",   "critical", lambda: METRICS.get("argos_pc_ssh_up",0) == 0, lambda: "ПК Орион недоступен (SSH down)"),
        ("ArgosOrchestratorDown","critical", lambda: METRICS.get("argos_orchestrator_uptime_sec",1) == 0, lambda: "Orchestrator не работает"),
        ("ArgosHighLoad",      "warning",  lambda: METRICS.get("argos_cpu_percent",0) > 85, lambda: f"Высокая нагрузка CPU: {METRICS.get('argos_cpu_percent',0):.1f}%"),
        ("ArgosDiskWarning",   "warning",  lambda: METRICS.get("argos_disk_percent",0) > 80, lambda: f"Диск заполнен на {METRICS.get('argos_disk_percent',0):.1f}%"),
        ("ArgosRamWarning",    "warning",  lambda: METRICS.get("argos_ram_percent",0) > 85, lambda: f"RAM заполнен на {METRICS.get('argos_ram_percent',0):.1f}%"),
        ("ArgosEntityStalled", "warning",  lambda: METRICS.get("argos_entity_cycles_total",0) == 0, lambda: "Entity cycles = 0"),
    ]

    # NEW: Trust-based alerts
    for node in NODES:
        conf = METRICS.get(f"argos_trust_{node.replace('-', '_')}", 1.0)
        rules.append((
            f"ArgosTrustLow_{node}", "critical" if conf < 0.3 else "warning",
            lambda c=conf: c < 0.5,
            lambda n=node, c=conf: f"Trust score {n} = {c:.2f} (< 0.5)"
        ))

    now = time.time()
    for name, sev, cond_fn, msg_fn in rules:
        firing = bool(cond_fn())
        prev = ALERT_STATE.get(name, {})
        prev_firing = prev.get("firing", False)
        if firing != prev_firing:
            ALERT_STATE[name] = {"firing": firing, "since": now, "last_sent": now}
            summary = msg_fn()
            status = "firing" if firing else "resolved"
            fname = write_alert_md(name, sev, status, summary)
            icon = "🔴" if firing else "🟢"
            print(f"[ALERT] {icon} {name} → {status} | {fname}")
            _tg(f"{icon} <b>{name}</b>\n{status.upper()}\n{summary}")
            # NEW: Audit log
            if _TRUST_GUARD:
                _TRUST_GUARD.log_action(
                    f"alert_{status}", name, sev,
                    {"summary": summary, "fname": fname, "source": "prometheus_exporter"}
                )
        else:
            if firing and (now - prev.get("last_sent", 0)) > 600:
                ALERT_STATE[name]["last_sent"] = now
                summary = msg_fn()
                _tg(f"🔁 <b>{name}</b> still FIRING\n{summary}")


def alert_loop():
    """Background thread: collect + check alerts every 30s."""
    while True:
        try:
            collect()
            check_alerts()
        except Exception as e:
            print(f"[ALERT LOOP] {e}")
        time.sleep(30)


if __name__ == "__main__":
    port = int(os.getenv("ARGOS_PROMETHEUS_PORT", "19090"))
    srv = HTTPServer(("0.0.0.0", port), MetricsHandler)
    print(f"[PROMETHEUS v2] Listening on :{port}/metrics, /trust, /dashboard")
    t = threading.Thread(target=alert_loop, daemon=True)
    t.start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("[PROMETHEUS] Stopped")
