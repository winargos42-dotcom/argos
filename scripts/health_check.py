#!/usr/bin/env python3
"""ARGOS Unified Health Check — одна команда, полная картина."""
import json, time, urllib.request, subprocess, sys, os
from pathlib import Path

REPORT = Path("/home/ava/Projects/argoss/data/health_report.json")

def check_url(url, timeout=5):
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return "UP"
    except Exception:
        return "DOWN"

def check_process(name):
    try:
        r = subprocess.run(["pgrep", "-f", name], capture_output=True, text=True, timeout=3)
        return "RUNNING" if r.returncode == 0 else "DOWN"
    except:
        return "UNKNOWN"

def health_check():
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    report = {
        "timestamp": ts,
        "checks": {
            "brain_api_pc": check_url("http://192.168.1.53:5001/health"),
            "brain_api_master": check_url(os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001/health")),
            "mcp_local": check_url("http://localhost:8000/mcp"),
            "mcp_pc": check_url("http://192.168.1.53:8000/mcp"),
            "prometheus": check_url("http://localhost:19090/metrics"),
            "ollama": check_url("http://localhost:11434/api/tags"),
            "orchestrator": check_process("orchestrator.py"),
            "entity_council": check_process("entity_council.py"),
            "self_healer": check_process("self_healer.py"),
            "p2p_mesh": check_process("p2p_mesh.py"),
        }
    }
    up = sum(1 for v in report["checks"].values() if v in ("UP", "RUNNING"))
    total = len(report["checks"])
    report["summary"] = f"{up}/{total} UP"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[{ts}] Health: {up}/{total} UP")
    for k, v in report["checks"].items():
        print(f"  {k:20s}: {v}")
    return report

if __name__ == "__main__":
    health_check()
