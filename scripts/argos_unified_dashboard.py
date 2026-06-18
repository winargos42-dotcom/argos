#!/usr/bin/env python3
"""
ARGOS Unified Dashboard v1 — агрегация всех источников.

Источники:
- Prometheus :19090 (system metrics, trust, alerts)
- Audit API :5010 (trust scores, audit log)
- Brain API :5001 (nodes, network)
- MemPalace (knowledge)
- Evolution (insights)

Выходы:
- HTML dashboard (single file)
- Telegram post (summary)
- Veto evidence (insights)
"""
import json
import urllib.request
import time
from pathlib import Path
from datetime import datetime as _dt, timezone as _tz
from collections import Counter

PROJECT_ROOT = Path("/home/ava/Projects/argoss")
VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory")


def get(url, timeout=5):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            if "metrics" in url:
                return r.read().decode()
            return json.loads(r.read())
    except Exception as e:
        return {"_error": str(e)}


def get_text_metrics(url):
    text = get(url)
    if isinstance(text, dict):
        return text
    metrics = {}
    for line in text.split("\n"):
        if line and not line.startswith("#"):
            parts = line.split()
            if len(parts) >= 2:
                try:
                    metrics[parts[0]] = float(parts[1])
                except ValueError:
                    pass
    return metrics


def get_status_emoji(value, threshold_warn=70, threshold_crit=85):
    if value >= threshold_crit: return "🔴"
    if value >= threshold_warn: return "🟡"
    return "🟢"


def main():
    print("="*70)
    print("  ARGOS Unified Dashboard v1")
    print("="*70)
    
    # 1. System metrics
    print("\n  📊 System metrics (Prometheus :19090)...")
    sys_metrics = get_text_metrics("http://localhost:19090/metrics")
    cpu = sys_metrics.get("argos_cpu_percent", 0)
    ram = sys_metrics.get("argos_ram_percent", 0)
    disk = sys_metrics.get("argos_disk_percent", 0)
    nodes_online = int(sys_metrics.get("argos_nodes_online", 0))
    nodes_total = int(sys_metrics.get("argos_nodes_total", 0))
    cycles = int(sys_metrics.get("argos_entity_cycles_total", 0))
    thoughts = int(sys_metrics.get("argos_thoughts_total", 0))
    syntheses = int(sys_metrics.get("argos_syntheses_total", 0))
    evolutions = int(sys_metrics.get("argos_evolutions_total", 0))
    kg_nodes = int(sys_metrics.get("argos_kg_nodes", 0))
    kg_edges = int(sys_metrics.get("argos_kg_edges", 0))
    
    # 2. Trust scores
    print("  🔒 Trust scores (Audit API :5010)...")
    trust = get("http://localhost:5010/trust")
    trust_dict = {n["node_id"]: n for n in trust} if isinstance(trust, list) else {}
    
    # 3. Alerts
    print("  🚨 Alerts (Audit API :5010)...")
    alerts = get("http://localhost:5010/alerts?min_severity=INFO")
    alert_list = alerts if isinstance(alerts, list) else []
    
    # 4. Audit log
    print("  📋 Audit log...")
    audit = get("http://localhost:5010/audit/query?min_severity=INFO&limit=10")
    audit_list = audit if isinstance(audit, list) else []
    
    # 5. Brain
    print("  🧠 Brain (PC)...")
    brain = get("http://192.168.1.53:5001/brain/nodes")
    brain_total = brain.get("total", 0) if isinstance(brain, dict) else 0
    brain_online = brain.get("online", 0) if isinstance(brain, dict) else 0
    
    # 6. MemPalace
    print("  🏛️ MemPalace...")
    try:
        out = subprocess_run(["/home/ava/Projects/argoss/.venv/bin/mempalace", "status"])
        # Parse
        mp_lines = out.split("\n")
        mp_drawers = 0
        for line in mp_lines:
            if "drawers" in line and "—" in line:
                parts = line.strip().split()
                for p in parts:
                    if p.isdigit():
                        mp_drawers = max(mp_drawers, int(p))
    except Exception as e:
        mp_drawers = 0
    
    # Build dashboard
    now = _dt.now(_tz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = f"""# 🛡️ ARGOS Unified Dashboard (Live)

_Last update: {now}_

## 🖥️ System
| Metric | Value | Status |
|--------|-------|--------|
| CPU | {cpu:.1f}% | {get_status_emoji(cpu, 70, 85)} |
| RAM | {ram:.1f}% | {get_status_emoji(ram, 75, 90)} |
| Disk | {disk:.1f}% | {get_status_emoji(disk, 80, 90)} |
| Brain (PC) | {brain_online}/{brain_total} | {'🟢' if brain_online > 0 else '🔴'} |
| Entity cycles | {cycles} | ✅ |
| Thoughts | {thoughts} | ✅ |
| Syntheses | {syntheses} | ✅ |
| Evolutions | {evolutions} | ✅ |
| KG | {kg_nodes}/{kg_edges} | ✅ |

## 🔒 Trust Scores
| Node | Confidence | Status |
|------|-----------|--------|
"""
    for node in ["orion", "nexus", "egida", "pico", "esp32", "android", "phone-redmi", "entity-valenok", "laptop"]:
        profile = trust_dict.get(node, {})
        conf = profile.get("confidence", 1.0)
        is_q = profile.get("is_quarantined", False)
        if is_q:
            status = "🔴 QUARANTINE"
        elif conf > 0.7:
            status = "✅ OK"
        elif conf > 0.3:
            status = "🟡 LOW"
        else:
            status = "🔴 BLOCKED"
        md += f"| {node} | {conf:.2f} | {status} |\n"
    
    md += f"""
## 🚨 Active Alerts ({len(alert_list)})
"""
    if alert_list:
        md += "| Severity | Name | Message |\n|----------|------|---------|\n"
        for a in alert_list[:10]:
            md += f"| {a.get('severity', '?')} | {a.get('name', '?')} | {str(a.get('message', '?'))[:80]} |\n"
    else:
        md += "✅ No active alerts\n"
    
    md += f"""
## 📋 Recent Audit ({len(audit_list)})
"""
    for e in audit_list[:5]:
        ts = e.get("timestamp", 0)
        try:
            from datetime import datetime
            ts_str = _dt.fromtimestamp(ts).strftime("%H:%M:%S")
        except:
            ts_str = "?"
        md += f"- `{ts_str}` [{e.get('event_type', '?')}] {e.get('actor', '?')}: {str(e.get('message', '?'))[:80]}\n"
    
    md += f"""
## 🔗 Endpoints
- Prometheus: http://localhost:19090/metrics
- Audit API: http://localhost:5010/trust
- Brain: http://192.168.1.53:5001/brain/nodes
- Proxy: http://localhost:5002/trust
- MemPalace: 1 wing, {mp_drawers} drawers

---
_Generated by ARGOS Unified Dashboard v1_
"""
    
    # Save
    out_file = VAULT / "entities/ARGOS_UNIFIED_DASHBOARD.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(md, encoding='utf-8')
    print(f"\n  ✓ Saved: {out_file}")
    
    # Summary for TG
    summary = f"""📊 ARGOS Dashboard {now}

🖥️ System: CPU {cpu:.0f}% {get_status_emoji(cpu)}, RAM {ram:.0f}% {get_status_emoji(ram)}, Disk {disk:.0f}% {get_status_emoji(disk)}
🧠 Brain: {brain_online}/{brain_total} | Cycles: {cycles} | KG: {kg_nodes}/{kg_edges}
🚨 Alerts: {len(alert_list)} firing"""
    if alert_list:
        summary += "\n  Active: " + ", ".join(f"{a.get('name','?')}" for a in alert_list[:3])
    
    return summary


def subprocess_run(cmd):
    import subprocess
    return subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout


if __name__ == "__main__":
    summary = main()
    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    print(summary)
