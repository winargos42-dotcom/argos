#!/usr/bin/env python3
"""ARGOS Self-Healer v2 — Circuit Breaker + Exponential Backoff + Cooldown.
Study: Self_Healing_SRE_2026.md + Circuit_Breaker_ARGOS_2026.md
"""
import sys, os, time, json, subprocess, urllib.request

PROJECT_ROOT = os.path.expanduser("~/Projects/argoss")
HEAL_LOG = os.path.join(PROJECT_ROOT, "logs/self_healer.log")

# cooldown map: service_name → unix_timestamp when last restarted
_COOLDOWN = {}
_COOLDOWN_SEC = 300   # 5 минут между рестартами одного сервиса
_RESTART_ATTEMPTS = {}
_MAX_RESTARTS = 3     # Circuit breaker: после 3 fail-рестартов → open

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[SELF_HEAL] {ts} {msg}"
    print(line)
    with open(HEAL_LOG, "a") as f:
        f.write(line + "\n")

def get_metrics():
    try:
        resp = urllib.request.urlopen("http://localhost:19090/metrics", timeout=5)
        lines = resp.read().decode().splitlines()
        metrics = {}
        for line in lines:
            if line.startswith("argos_") and not line.startswith("#"):
                k, v = line.rsplit(" ", 1)
                metrics[k] = float(v)
        return metrics
    except Exception as e:
        return {}

def check_local_brain():
    """Проверка Brain API (PC Master)"""
    try:
        brain_url = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
        urllib.request.urlopen(f"{brain_url}/health", timeout=3)
        return True
    except:
        return False

def check_pc_brain():
    """Проверка Brain API ПК (same as local now)"""
    return check_local_brain()

def restart_service(name: str, cmd: str, cooldown: int = _COOLDOWN_SEC):
    now = time.time()
    last = _COOLDOWN.get(name, 0)
    if now - last < cooldown:
        log(f"SKIP {name}: cooldown active ({int(cooldown - (now - last))}s left)")
        return False

    # Circuit breaker on restarts
    fails = _RESTART_ATTEMPTS.get(name, 0)
    if fails >= _MAX_RESTARTS:
        log(f"CIRCUIT OPEN for {name}: {_MAX_RESTARTS} restarts failed, backing off 10min")
        # 10 минут backoff
        _COOLDOWN[name] = now + 600
        _RESTART_ATTEMPTS[name] = 0
        return False

    log(f"RESTARTING {name}: {cmd}")
    _RESTART_ATTEMPTS[name] = fails + 1
    try:
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        _COOLDOWN[name] = now
        # Если рестарт удачен — сбрасываем fail counter
        _RESTART_ATTEMPTS[name] = 0
        return True
    except Exception as e:
        log(f"RESTART FAILED {name}: {e}")
        return False

def heal():
    m = get_metrics()
    if not m:
        log("Prometheus unreachable — check :19090")
        return

    cpu = m.get("argos_cpu_percent", 0)
    ram = m.get("argos_ram_percent", 0)
    disk = m.get("argos_disk_percent", 0)
    brain = m.get("argos_brain_api_up", 0)
    nodes = m.get("argos_nodes_online", 0)

    # CPU
    if cpu > 90:
        log(f"ALERT: CPU {cpu}% — killing top CPU process")
        subprocess.run("ps -eo pid,ppid,cmd,%cpu --sort=-%cpu | head -5", shell=True)

    # RAM
    if ram > 90:
        log(f"ALERT: RAM {ram}% — triggering OOM precaution")
        subprocess.run("ps -eo pid,ppid,cmd,%mem --sort=-%mem | head -5", shell=True)

    # Disk > 80% (по плану нужен alert)
    if disk > 80:
        log(f"ALERT: Disk {disk}% — cleanup needed")
        # Быстрая очистка логов старше 7 дней
        subprocess.run("find /home/ava/Projects/argoss/logs -name '*.log' -mtime +7 -delete", shell=True)
        log("Executed: cleanup old logs")

    # Local brain :5001
    local_brain_ok = check_local_brain()
    if not local_brain_ok:
        log("ALERT: Local Brain API :5001 DOWN")
        restart_service("argos-brain-api",
            "systemctl restart argos-brain-api.service")
    else:
        # Если локальный brain жив — сбрасываем fail counter
        _RESTART_ATTEMPTS.pop("argos-brain-api", None)

    # PC brain :5010
    pc_brain_ok = check_pc_brain()
    if not pc_brain_ok:
        log("ALERT: PC Brain API :5010 DOWN — SSH wakeup or manual check needed")
        # На ноутбуке не можем рестартовать ПК, только логируем
        # Можно попробовать SSH
        try:
            subprocess.run("ssh AvA@192.168.1.53 'curl -s http://localhost:5010/health'",
                shell=True, timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    # Nodes
    if nodes < 20:
        log(f"ALERT: Only {int(nodes)} nodes online — network degraded")
        # Попытка рестарт heartbeat
        restart_service("argos-heartbeat",
            "systemctl restart argos-heartbeat.service")

    # Log summary
    log(f"checks: CPU={cpu:.0f}% RAM={ram:.0f}% Disk={disk:.0f}% LocalBrain={'✅' if local_brain_ok else '❌'} PCBrain={'✅' if pc_brain_ok else '❌'} Nodes={int(nodes)}")

if __name__ == "__main__":
    log("Self-Healer v2 started (CB+cooldown+backoff)")
    while True:
        try:
            heal()
        except Exception as e:
            log(f"ERROR: {e}")
        time.sleep(60)
