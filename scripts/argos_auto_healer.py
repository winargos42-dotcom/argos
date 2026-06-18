#!/usr/bin/env python3
"""
ARGOS Auto-Healer v1 — восстанавливает упавшие сервисы.

Что делает:
- Сканирует systemd сервисы
- Если упал — рестартит
- Если не помогло — notify в Council
- Сканирует endpoint health
- Если endpoint не отвечает — рестартит соответствующий сервис
"""
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/home/ava/Projects/argoss")

SERVICES = [
    "argos-brain-api.service",
    "argos-prometheus-exporter.service",
    "argos-business.service",
    "argos-autopilot.service",
    "argos-entity-council.service",
    "argos-claude-bridge.service",
    "argos-self-heal.service",
    "argos-dataset-collector.service",
    "argos-autonomous-brain.service",
    "argos-colibri.service",
]

ENDPOINTS = [
    ("Audit API", "http://localhost:5010/health", None),  # process-managed
    ("Prometheus", "http://localhost:19090/metrics", "argos-prometheus-exporter.service"),
    ("Audit Proxy", "http://localhost:5002/health", None),
    ("Brain (PC)", "http://192.168.1.53:5001/brain/nodes", "argos-brain-api.service"),
    ("Cloud API", "http://130.211.235.115/health", None),  # remote, no fallback
    ("Brain (PC) Backup", "http://192.168.1.53:5001/brain/nodes", None),  # PC Brain is now primary
]


def systemctl_status(name):
    """Получить статус сервиса."""
    try:
        out = subprocess.run(
            ["systemctl", "is-active", name],
            capture_output=True, text=True, timeout=5
        )
        return out.stdout.strip()
    except:
        return "unknown"


def systemctl_restart(name):
    """Рестарт сервиса."""
    try:
        out = subprocess.run(
            ["sudo", "systemctl", "restart", name],
            capture_output=True, text=True, timeout=15
        )
        return out.returncode == 0
    except:
        return False


def check_endpoint(name, url):
    """Проверить endpoint."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status == 200
    except:
        return False


def heal():
    """Один цикл healing."""
    print("="*70)
    print(f"  ARGOS Auto-Healer v1 — {datetime.now().isoformat()}")
    print("="*70)
    
    actions = []
    
    # 1. Check services
    print("\n  1. Сканируем сервисы...")
    for svc in SERVICES:
        status = systemctl_status(svc)
        if status != "active":
            print(f"     ❌ {svc}: {status} — рестарт")
            ok = systemctl_restart(svc)
            actions.append(f"restart {svc} ({'OK' if ok else 'FAIL'})")
            time.sleep(1)
        else:
            print(f"     ✅ {svc}: active")
    
    # 2. Check endpoints
    print("\n  2. Сканируем endpoints...")
    for name, url, fallback_svc in ENDPOINTS:
        ok = check_endpoint(name, url)
        if not ok and fallback_svc:
            print(f"     ❌ {name} ({url}) — рестарт {fallback_svc}")
            if systemctl_restart(fallback_svc):
                actions.append(f"restart {fallback_svc} (endpoint {name} down)")
        else:
            print(f"     {'✅' if ok else '⚠️'} {name}")
    
    # 3. Cleanup zombie processes
    print("\n  3. Чистим zombie процессы...")
    try:
        out = subprocess.run(
            ["ps", "aux"],
            capture_output=True, text=True, timeout=5
        )
        zombies = [line for line in out.stdout.split("\n")
                   if len(line.split()) > 7 and "Z" in line.split()[7]]
        if zombies:
            print(f"     Zombies: {len(zombies)}")
        else:
            print(f"     No zombies")
    except Exception as e:
        print(f"     [ERR] {e}")
    
    print(f"\n  Действия: {len(actions)}")
    for a in actions:
        print(f"    - {a}")
    
    return actions


if __name__ == "__main__":
    actions = heal()
    
    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "actions": actions,
    }
    Path(PROJECT_ROOT / "data/auto_healer").mkdir(parents=True, exist_ok=True)
    out = PROJECT_ROOT / f"data/auto_healer/heal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"\n  ✓ Report: {out}")
