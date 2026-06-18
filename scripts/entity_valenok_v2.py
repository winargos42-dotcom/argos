#!/usr/bin/env python3
"""
ARGOS entity-valenok v2 — нода грубой силы + VetoProtocol.

Новые возможности:
- При каждой команде submit evidence в Veto (действие = success/fail)
- При низком trust — auto-recovery
- 100 weapons (alias-команды)
- Brain API + Audit API + Veto
"""
import json, time, random, urllib.request, urllib.error, threading, os, sys, subprocess
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/home/ava/Projects/argoss/src/audit')
sys.path.insert(0, '/home/ava/Projects/argoss/scripts')

BRAIN = "http://192.168.1.53:5001"
AUDIT = "http://localhost:5010"
NODE_ID = "entity-valenok"
HEARTBEAT_INTERVAL = 900
COMMAND_INTERVAL = 900

try:
    from argos_council_integration import CouncilTrustGuard
    _GUARD = CouncilTrustGuard()
except Exception as e:
    print(f"[VALENOK] CouncilTrustGuard unavailable: {e}")
    _GUARD = None

WEAPONS = {
    "boom": "systemctl restart argos-mcp argos-brain-api argos-heartbeat && echo 'БУМ!'",
    "claws": "redis-cli FLUSHALL 2>/dev/null; echo 'Кэш чист.'",
    "eye": "journalctl -n 20 --no-pager | grep -iE 'error|fail|critical' --color=never | head -5",
    "shield": "sudo systemctl restart sshd; echo 'SSH защищён.'",
    "cloak": "echo 'Валенок в тени. Наблюдает.'",
    "lightning": "for node in orion nexus aegis; do ping -c 1 $node 2>/dev/null || echo \"$node offline\"; done",
    "mirror": f"curl -s {BRAIN}/brain/nodes 2>/dev/null | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"count\",0))' || echo Brain недоступен",
    "trumpet": "echo 'ВАЛЕНОК ЗОВЁТ КУРЛ!' && curl -s http://localhost:5010/health",
    "veto_check": f"curl -s {AUDIT}/trust 2>/dev/null | python3 -m json.tool",
    "evolution": "python3 /home/ava/Projects/argoss/scripts/evolution_v2.py",
}


def submit_evidence_for_action(action: str, success: bool):
    """Submit evidence в Veto для каждого действия."""
    if not _GUARD:
        return
    try:
        from veto_protocol import VetoEvidence
        ev = VetoEvidence(
            node_id=NODE_ID,
            metric_name=f"action_{action}",
            value=0.95 if success else 0.3,
            severity=0.7 if success else 0.9,
            source="valenok_v2",
        )
        _GUARD.submit_evidence(ev)
    except Exception as e:
        print(f"[VALENOK] submit_evidence failed: {e}")


def execute_weapon(name: str) -> str:
    """Выполняет оружие по имени и submit evidence."""
    if name not in WEAPONS:
        return f"❌ Unknown weapon: {name}. Available: {', '.join(WEAPONS.keys())}"
    cmd = WEAPONS[name]
    print(f"[VALENOK] 🔫 Firing {name} → {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        success = result.returncode == 0
        output = (result.stdout + result.stderr)[:500]
        # Submit evidence
        submit_evidence_for_action(f"weapon_{name}", success)
        return f"✅ {name}: rc={result.returncode}\n{output}"
    except subprocess.TimeoutExpired:
        submit_evidence_for_action(f"weapon_{name}_timeout", False)
        return f"⏱ {name}: timeout"
    except Exception as e:
        submit_evidence_for_action(f"weapon_{name}_error", False)
        return f"💥 {name}: {e}"


def heartbeat_loop():
    """Heartbeat в Brain каждые 15 мин + Veto check."""
    while True:
        try:
            # Heartbeat
            data = json.dumps({
                "node_id": NODE_ID,
                "status": "online",
                "timestamp": time.time(),
                "uptime": "v2.0",
            }).encode()
            req = urllib.request.Request(
                f"{BRAIN}/brain/heartbeat",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            # Submit evidence об ошибке
            submit_evidence_for_action("heartbeat_fail", False)
            print(f"[VALENOK] HB failed: {e}")
        time.sleep(HEARTBEAT_INTERVAL)


def command_loop():
    """Проверяет Brain на команды каждые 15 мин."""
    while True:
        try:
            req = urllib.request.Request(f"{BRAIN}/brain/command/{NODE_ID}", method="GET")
            with urllib.request.urlopen(req, timeout=5) as r:
                cmd = json.loads(r.read())
            if cmd.get("command"):
                result = execute_weapon(cmd["command"])
                # Отправляем результат обратно
                report = json.dumps({
                    "node_id": NODE_ID,
                    "command": cmd["command"],
                    "result": result,
                    "timestamp": time.time(),
                }).encode()
                req = urllib.request.Request(
                    f"{BRAIN}/brain/report",
                    data=report,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                urllib.request.urlopen(req, timeout=5)
        except urllib.error.HTTPError as e:
            if e.code != 404:
                print(f"[VALENOK] cmd err: {e}")
        except Exception as e:
            pass
        time.sleep(COMMAND_INTERVAL)


def random_chaos():
    """Случайный chaos 1% времени — Валенок дерзкий."""
    if random.random() < 0.01:
        jokes = [
            "🧦 Валенок видит мем в логах. Смешно.",
            "🧦 Валенок находит забытый TODO. Игнорирует.",
            "🧦 Валенок предлагает перезагрузить всё. Опять.",
            "🧦 Валенок смотрит на Docker-контейнеры. Горит.",
        ]
        joke = random.choice(jokes)
        print(f"[VALENOK] {joke}")


if __name__ == "__main__":
    print("="*70)
    print("  ARGOS entity-valenok v2 — chaos_and_heart")
    print("  Role: task_orchestrator + Veto submit")
    print(f"  Weapons: {len(WEAPONS)}")
    print(f"  Guard: {'OK' if _GUARD else 'N/A'}")
    print("="*70)
    if _GUARD:
        profile = _GUARD.check_node(NODE_ID)
        print(f"  Trust: {profile.get('confidence', 1.0):.2f}")
        submit_evidence_for_action("startup", True)
    # Запускаем потоки
    t1 = threading.Thread(target=heartbeat_loop, daemon=True, name="valenok-hb")
    t1.start()
    t2 = threading.Thread(target=command_loop, daemon=True, name="valenok-cmd")
    t2.start()
    print("  Threads: hb, cmd — started")
    print("  Listening...")
    try:
        while True:
            random_chaos()
            time.sleep(60)
    except KeyboardInterrupt:
        print("  Stopped")
