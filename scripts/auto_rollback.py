#!/usr/bin/env python3
"""
ARGOS Auto-Rollback — защита от поломки после deploy.
Снапшот git hash перед deploy → проверка через 3 мин → если сервис упал:
  1. Git revert HEAD --no-edit
  2. systemd restart (или Docker swarm update --force)
"""
import subprocess, time, json, os, requests
from pathlib import Path
from datetime import datetime

GIT_DIR = Path("/home/ava/Projects/argoss")
STATE_FILE = Path("/home/ava/Projects/argoss/data/mempalace/rollback_state.json")
REPORT_DIR = Path("/home/ava/Projects/argoss/data/mempalace")

# Сервисы для HTTP health check
HEALTH_CHECKS = {
    "brain_api": "http://192.168.1.53:5001/brain/nodes",
    "control_plane": "http://localhost:3456/nodes",
    "curiosity": "http://localhost:3457/health",
    "kill_switch": "http://localhost:7777/health",
    "shell_gate": "http://localhost:7778/health",
}

def get_git_hash():
    try:
        r = subprocess.run(["git","-C",str(GIT_DIR),"rev-parse","HEAD"], capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else None
    except: return None

def check_http_health(url, retries=3, delay=5):
    for i in range(retries):
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        print(f"[⚠️] Не отвечает {url}, проверка {i+1}/{retries}...")
        time.sleep(delay)
    return False

def check_services_health():
    """Проверяет systemd argos-* + HTTP endpoints."""
    r = subprocess.run(["systemctl","list-units","--type=service","--state=failed","--no-pager","--plain"],
        capture_output=True, text=True, timeout=10)
    failed_systemd = [line.split()[1] for line in r.stdout.splitlines() if line.strip().startswith("argos-")]
    
    failed_http = []
    for name, url in HEALTH_CHECKS.items():
        if not check_http_health(url, retries=2, delay=3):
            failed_http.append(name)
    
    ok = len(failed_systemd) == 0 and len(failed_http) == 0
    return ok, failed_systemd, failed_http

def pre_deploy_snapshot():
    h = get_git_hash()
    state = {"hash": h, "ts": datetime.now().isoformat()}
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False))
    print(f"[Rollback] Snapshot at {h}")

def rollback():
    if not STATE_FILE.exists():
        print("[Rollback] No snapshot")
        return
    state = json.loads(STATE_FILE.read_text())
    old_hash = state.get("hash")
    print(f"[Rollback] Checking health (snapshot: {old_hash[:8] if old_hash else 'none'}...")
    time.sleep(90)
    
    ok, failed_systemd, failed_http = check_services_health()
    if ok:
        print("[Rollback] ✅ All healthy")
        STATE_FILE.unlink()
        return
    
    print(f"[Rollback] ❌ FAILED: systemd={failed_systemd}, http={failed_http}")
    
    # Git revert
    try:
        subprocess.run(["git","-C",str(GIT_DIR),"revert","HEAD","--no-edit"], capture_output=True, timeout=10)
        print("[Rollback] ✅ Git reverted")
    except Exception as e:
        print(f"[Rollback] ⚠️ git error: {e}")
    
    # Restart systemd
    for svc in failed_systemd:
        subprocess.run(["systemctl","restart",svc], capture_output=True, timeout=10)
        print(f"[Rollback] 🔄 Restarted {svc}")
    
    # Docker swarm force update (если есть swarm сервис)
    for svc in failed_http:
        if "brain" in svc or "api" in svc:
            try:
                subprocess.run(["docker","service","update","--force",f"argos_{svc}"], capture_output=True, timeout=10)
                print(f"[Rollback] 🐳 Swarm force update {svc}")
            except:
                pass
    
    report = REPORT_DIR / f"rollback_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    report.write_text(json.dumps({
        "ts": datetime.now().isoformat(), "rolled_back_from": old_hash,
        "failed_systemd": failed_systemd, "failed_http": failed_http
    }, ensure_ascii=False))
    STATE_FILE.unlink()

if __name__ == "__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="snapshot":
        pre_deploy_snapshot()
    else:
        rollback()
