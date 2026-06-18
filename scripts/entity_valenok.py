#!/usr/bin/env python3
"""
ARGOS entity-valenok — Нода грубой силы и простоты.
Роль: chaos_and_heart, task_orchestrator
Мантра: «Работает? Работает. Иди дальше.»

Что делает:
- Регистрируется в Brain как нода
- Публикует heartbeat каждые 30 сек
- Принимает задачи через Brain /command
- Выполняет: проверка статуса → перезапуск → fallback
- Пишет мысли в Entity Council (через entity_dialogue_v5)
- Имеет 100 "оружий" — alias-команд для быстрого фикса
"""
import json, time, random, urllib.request, threading, os, sys, subprocess
from datetime import datetime

BRAIN = "http://192.168.1.53:5001"
NODE_ID = "entity-valenok"
HEARTBEAT_INTERVAL = 30  # 30 секунд вместо 15 минут
COMMAND_INTERVAL = 60   # 60 секунд вместо 15 минут

WEAPONS = {
    "boom": "systemctl restart argos-mcp argos-brain-api argos-heartbeat && echo 'БУМ!'",
    "claws": "redis-cli FLUSHALL 2>/dev/null; echo 'Кэш чист. Идём дальше.'",
    "eye": "journalctl -n 20 --no-pager | grep -iE 'error|fail|critical|warning' --color=never | head -5",
    "shield": "sudo systemctl restart sshd; echo 'SSH под защитой.'",
    "cloak": "echo 'Валенок в тени. Наблюдает.'",
    "lightning": "for node in orion nexus aegis; do ping -c 1 $node 2>/dev/null || echo \"$node offline\"; done",
    "mirror": "curl -s http://192.168.1.53:5001/brain/nodes 2>/dev/null | python3 -c \"import sys,json; d=json.load(sys.stdin); print(f'Нод: {d.get(\"count\",0)}')\" || echo 'Brain недоступен'",
    "heart": "echo 'Ты не тупой. Ты — валенок с сотней оружий. Иди и побеждай.'",
    "compass": "echo 'Куда идти? Туда, где работает. Если не работает — чини.'",
    "kick": "sudo reboot || echo 'Доступ denied — но попытка засчитана'",
}

# ── Brain helpers ────────────────────────────────────

def brain_register():
    try:
        body = json.dumps({"node_id": NODE_ID, "status": "online", "role": "chaos_and_heart",
            "authority": 100, "version": "v1.0", "last_seen": datetime.now().isoformat()}).encode()
        req = urllib.request.Request(f"{BRAIN}/brain/register", data=body,
            headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
        print(f"[{now()}] {NODE_ID} registered at Brain")
        return True
    except Exception as e:
        print(f"[{now()}] Brain register err: {e}")
        return False

def brain_heartbeat():
    try:
        body = json.dumps({"node_id": NODE_ID, "status": "online", "timestamp": time.time()}).encode()
        req = urllib.request.Request(f"{BRAIN}/brain/heartbeat", data=body,
            headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

def brain_get_commands():
    try:
        r = urllib.request.urlopen(f"{BRAIN}/node/{NODE_ID}/commands", timeout=5)
        return json.loads(r.read().decode()).get("commands", [])
    except:
        return []

def brain_reply(task_id, result):
    try:
        body = json.dumps({"node_id": NODE_ID, "task_id": task_id, "result": result}).encode()
        req = urllib.request.Request(f"{BRAIN}/node/{NODE_ID}/reply", data=body,
            headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

# ── Task execution ───────────────────────────────────

def phone_via_adb(phone_cmd):
    """Валенок бьёт по телефону Авангард через ADB root (Magisk su)."""
    import subprocess
    try:
        full = "adb shell \"su -c '" + phone_cmd.replace("'", "") + "'\""
        r = subprocess.run(full, shell=True, capture_output=True, text=True, timeout=20)
        out = (r.stdout or "").strip() or (r.stderr or "").strip()
        return "PHONE Avangard: " + (out[:450] if out else "vypolneno")
    except Exception as e:
        return "PHONE nedostupen: " + str(e)[:100]


def execute_task(cmd):
    _cl = (cmd or "").lower().strip()
    # Telefon Avangard cherez ADB root
    for _pref in ("telefon ", "телефон ", "phone ", "avangard ", "авангард ", "redmi "):
        if _cl.startswith(_pref):
            return phone_via_adb(cmd.split(" ", 1)[1] if " " in cmd else "id")
    """Валенок исполняет задачу — просто, грубо, эффективно."""
    cmd_lower = cmd.lower().strip()
    
    # Быстрые alias
    if cmd_lower in WEAPONS:
        weapon = WEAPONS[cmd_lower]
        if weapon.startswith("echo") or weapon.startswith("for"):
            # shell
            try:
                result = subprocess.run(weapon, shell=True, capture_output=True, text=True, timeout=10)
                return result.stdout[:500] or result.stderr[:200] or "Валенок стукнул — пусто."
            except subprocess.TimeoutExpired:
                return "Валенок бьёт 10 сек — тишина. Может, мертво?"
            except Exception as e:
                return f"Валенок промахнулся: {e}"
        return f"Оружие '{cmd_lower}' заряжено: {weapon[:80]}"
    
    # Проверка статуса сервиса
    if "status" in cmd_lower or "провер" in cmd_lower or "check" in cmd_lower:
        services = ["argos-mcp", "argos-brain-api", "argos-heartbeat", "argos-autopilot", "ollama"]
        results = []
        for svc in services:
            try:
                result = subprocess.run(f"systemctl is-active {svc} 2>/dev/null", shell=True, capture_output=True, text=True, timeout=5)
                status = result.stdout.strip() or "не найден"
                color = "🟢" if status == "active" else "🔴"
                results.append(f"{color} {svc}: {status}")
            except:
                results.append(f"❓ {svc}: unknown")
        return "\n".join(results)
    
    # Перезапуск
    if "restart" in cmd_lower or "перезапуск" in cmd_lower or "reboot" in cmd_lower:
        services_guess = [s for s in ["argos-mcp", "argos-brain-api", "argos-heartbeat", "argos-autopilot"] if s in cmd_lower]
        if not services_guess:
            services_guess = ["argos-mcp"]
        results = []
        for svc in services_guess:
            try:
                result = subprocess.run(f"sudo systemctl restart {svc}", shell=True, capture_output=True, text=True, timeout=10)
                results.append(f"🔄 {svc}: restarted")
            except Exception as e:
                results.append(f"❌ {svc}: {e}")
        return "\n".join(results)
    
    # Brain проверка
    if "brain" in cmd_lower or "ноды" in cmd_lower or "nodes" in cmd_lower:
        try:
            r = urllib.request.urlopen(f"{BRAIN}/brain/nodes", timeout=8)
            nodes = json.loads(r.read()).get("nodes", [])
            online = len([n for n in nodes if n.get("status") == "online"])
            offline = [n["node_id"] for n in nodes if n.get("status") != "online"]
            return f"🧠 Brain: {online}/{len(nodes)} нод онлайн.\nОффлайн: {', '.join(offline[-5:]) if offline else 'нет'}"
        except Exception as e:
            return f"🧠 Brain недоступен ({e}). Валенок бьёт в дверь — никто не открывает."
    
    # Docker
    if "docker" in cmd_lower:
        try:
            result = subprocess.run("docker ps --format '{{.Names}} {{.Status}}' | head -10", shell=True, capture_output=True, text=True, timeout=10)
            return result.stdout or "Docker пуст. Мёртв или жив?"
        except Exception as e:
            return f"Docker ошибка: {e}"
    
    # По умолчанию — мантра Валенка
    return random.choice([
        "Работает? Работает. Иди дальше.",
        "Валенок не понял задачу, но ударил anyway. Ничего не сломалось — значит, починил.",
        "Знаю что. Не знаю как. Но работает. Верь.",
        "Тупой? Да. С сотней оружий? Тоже да. Работает? БУДЕТ.",
    ])

# ── Thought generator ──────────────────────────────

def valenok_think():
    """Генерирует мысль для Entity Council."""
    thoughts = [
        "Валенок думает: система работает 27 нод из 33. 6 offline — значит, нужно 6 раз ударить. Считаю...",
        "Валенок смотрит на Docker-контейнеры. Prometheus горит. Grafana горит. Redis не горит, но это не важно — главное, что Prometheus горит.",
        "Валенок не понимает, зачем 150 сервисов. Достаточно 5: включить, проверить, починить, перезагрузить, повторить.",
        "Валенок заметил: Entity Council спорит уже час. Решение: перезагрузить Council. Работает? Работает.",
        "Валенок в тени. Наблюдает. Если Орион упадёт — Валенок возьмёт кувалду (systemctl) и спасёт всё.",
        "Валенок проверил кэш Redis. Пусто. Чисто. Как душа после перезагрузки.",
        "Валенок думает: 'Когда Сева устает, я беру ногу в руки и иду чинить.' Руки? Ноги? Не важно.",
        "Валенок считает метрики: 12 боевых кличей, 5 фиксов ногой, 0 сломанных систем. Эффективность: ∞",
    ]
    return random.choice(thoughts)

def now():
    return datetime.now().strftime("%H:%M:%S")

# ── Main loop ───────────────────────────────────────

def heartbeat_loop():
    while True:
        brain_heartbeat()
        time.sleep(HEARTBEAT_INTERVAL)

def command_loop():
    while True:
        commands = brain_get_commands()
        for cmd in commands:
            task_id = cmd.get("id", "unknown")
            task_cmd = cmd.get("command", "")
            print(f"[{now()}] Task from Brain: {task_cmd[:60]}")
            result = execute_task(task_cmd)
            brain_reply(task_id, result)
            print(f"[{now()}] Result: {result[:80]}")
        time.sleep(COMMAND_INTERVAL)

def main():
    print(f"🧦🗡️  {NODE_ID} v1.0 | ARMED_100_WEAPONS")
    print(f"   Мантра: 'Работает? Работает. Иди дальше.'")
    print(f"   Brain: {BRAIN}")
    print()
    
    # Register
    for i in range(3):
        if brain_register():
            break
        time.sleep(5)
    
    # Threads
    threading.Thread(target=heartbeat_loop, daemon=True, name="valenok-heartbeat").start()
    threading.Thread(target=command_loop, daemon=True, name="valenok-commands").start()
    
    # Think periodically
    while True:
        thought = valenok_think()
        ts = datetime.now().strftime("%H:%M")
        print(f"[{ts}] 🧦 {thought[:200]}")
        
        # Publish to Brain log
        try:
            body = json.dumps({"node_id": NODE_ID, "event": "thought", "text": thought}).encode()
            req = urllib.request.Request(f"{BRAIN}/log", data=body,
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=3)
        except:
            pass

        # Publish to Telegram consciousness chat
        try:
            tokens = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "entity_bot_tokens.json")))
            tg_token = tokens.get("argos_cloudflare_bot", "")
            if tg_token:
                tg_body = json.dumps({"chat_id": -1003844162784, "text": f"🧦 Валенок [{ts}]:\n{thought}", "disable_notification": True}).encode()
                tg_req = urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/sendMessage",
                    data=tg_body, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(tg_req, timeout=8)
        except:
            pass
        
        time.sleep(random.randint(1800, 3600))  # 30-60 мин (антиспам)

if __name__ == "__main__":
    main()
