#!/usr/bin/env python3
"""
Self-Heal Watchdog — следит за всеми сервисами ARGOS.
Если dead → restart. Если 3 fails → задача в WORKING.md.
Если RAM > 95% → убивает lowest-priority процессы.
"""
import subprocess, json, datetime
from pathlib import Path

WORKING = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md")
LOG = Path("/home/ava/Projects/argoss/data/mempalace/self_heal.log")
COUNTER = Path("/home/ava/Projects/argoss/data/mempalace/heal_counter.json")

# ensure dirs exist
LOG.parent.mkdir(parents=True, exist_ok=True)

# Только сервисы (не таймеры)
SERVICES = [
    "argos-entity-bus", "argos-entity-council",
    "argos-control-plane", "argos-curiosity",
    "argos-kill-switch"
]

TIMERS = [  # таймеры — не рестартуем, просто проверяем статус
    "argos-auto-tasker", "argos-idea-scorer", "argos-meta-tasker",
    "argos-survival", "argos-hive", "argos-ab-test", "argos-auto-deploy"
]

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def load_counter():
    if COUNTER.exists():
        return json.loads(COUNTER.read_text())
    return {}

def save_counter(c):
    COUNTER.write_text(json.dumps(c, indent=2), encoding="utf-8")

def get_ram_pct():
    try:
        r = subprocess.run(["free","-m"], capture_output=True, text=True, timeout=5)
        for line in r.stdout.splitlines():
            if line.startswith("Mem:"):
                parts = line.split()
                return int(parts[2]) / int(parts[1]) * 100
    except: pass
    return 0.0

def restart_service(svc):
    r = subprocess.run(["sudo","systemctl","restart",svc], capture_output=True, text=True, timeout=15)
    return r.returncode == 0

def get_service_status(svc):
    # Сначала проверяем существует ли unit
    r = subprocess.run(["systemctl","list-unit-files",svc + ".service"],
        capture_output=True, text=True, timeout=3)
    if svc not in r.stdout:
        return "not-installed"
    r2 = subprocess.run(["systemctl","is-active",svc], capture_output=True, text=True, timeout=5)
    if r2.returncode != 0:
        r3 = subprocess.run(["systemctl","is-failed",svc], capture_output=True, text=True, timeout=5)
        if r3.returncode == 0:
            return "failed"
    return r2.stdout.strip() or "unknown"

def kill_lowest_priority():
    """При RAM > 95% — убиваем контейнеры с low priority и процессы ollama."""
    log("RAM CRITICAL — killing low-priority processes")
    # Сначала docker контейнеры с низким приоритетом
    low = ["jaeger", "pgadmin", "portainer", "n8n"]
    for name in low:
        try:
            r = subprocess.run(["docker","stop",f"argoss-{name}-1"],
                capture_output=True, timeout=10)
            if r.returncode == 0:
                log(f"Stopped docker: {name}")
        except Exception:
            pass
    # Процессы ollama
    try:
        subprocess.run(["pkill","-f","ollama"], capture_output=True, timeout=5)
        log("Killed ollama processes")
    except: pass

def add_task(svc, reason):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"- [ ] **{ts}** [HEAL] {svc}: {reason}\n"
    with open(WORKING, "a", encoding="utf-8") as f:
        f.write(line)
    log(f"TASK ADDED: {svc} — {reason}")

if __name__ == "__main__":
    log("="*40)
    log("SELF-HEAL CHECK STARTED")
    
    counter = load_counter()
    
    # 1. Проверка сервисов (рестартуем)
    for svc in SERVICES:
        status = get_service_status(svc)
        log(f"[SVC] {svc}: {status}")
        
        if status in ("failed", "inactive"):
            count = counter.get(svc, 0) + 1
            counter[svc] = count
            
            if count <= 3:
                log(f"  → RESTARTING (attempt {count})")
                ok = restart_service(svc)
                if ok:
                    log(f"  → RESTARTED OK")
                    counter[svc] = 0
                else:
                    log(f"  → RESTART FAILED")
            else:
                log(f"  → CRITICAL: 3 failures, adding task")
                add_task(svc, f"Failed {count} times")
                counter[svc] = 0
        else:
            counter[svc] = 0
    
    # 2. Проверка таймеров (только логируем)
    for tmr in TIMERS:
        status = get_service_status(tmr)
        log(f"[TMR] {tmr}: {status}")
        if status == "failed":
            log(f"  → Timer failed (will check next)")
    
    # 2. RAM check
    ram = get_ram_pct()
    log(f"RAM: {ram:.1f}%")
    if ram > 95:
        kill_lowest_priority()
        add_task("system", f"RAM was {ram:.1f}% — killed low-priority containers")
    elif ram > 85:
        log(f"  → WARNING: RAM high ({ram:.1f}%)")
    
    save_counter(counter)
    log("SELF-HEAL COMPLETE")
    log("="*40)
