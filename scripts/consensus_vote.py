#!/usr/bin/env python3
"""
Cross-Node Vote — консенсус 2/3 между Orion, Nexus, OPi.
Перед критическим действием (kill deploy reboot) — спрашиваем все узлы.
"""
import subprocess, json, datetime, time
from pathlib import Path

NODES = {
    "orion": {"host": "192.168.1.53", "user": "AvA"},
    "nexus": {"host": "localhost", "user": "ava"},
    "opi":   {"host": "192.168.2.168", "user": "root"},
}

LOG = Path("/home/ava/Projects/argoss/data/mempalace/consensus.log")

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def ping_node(name, cfg):
    """Проверяем доступность узла."""
    if name == "nexus":
        return True
    try:
        cmd = ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes",
            f"{cfg['user']}@{cfg['host']}", "echo OK"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        return r.returncode == 0 and "OK" in r.stdout
    except:
        return False

def vote_on_action(action):
    """Голосование 2/3 за критическое действие."""
    log(f"VOTE STARTED: {action}")
    
    votes = {}
    for name, cfg in NODES.items():
        ok = ping_node(name, cfg)
        votes[name] = "yes" if ok else "no"
        log(f"  {name}: {'yes' if ok else 'no'}")
        time.sleep(0.3)
    
    yes_count = sum(1 for v in votes.values() if v == "yes")
    total = len(votes)
    
    quorum = (total // 2) + 1  # 2/3
    passed = yes_count >= quorum
    
    log(f"VOTE RESULT: {yes_count}/{total} (need {quorum}) → {'PASS' if passed else 'BLOCK'}")
    return passed, votes

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "test_action"
    passed, votes = vote_on_action(action)
    print(json.dumps({"action": action, "passed": passed, "votes": votes}, ensure_ascii=False))
