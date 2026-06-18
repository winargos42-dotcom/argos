#!/data/data/com.termux/files/usr/bin/python3
"""
Валенок — агент на Авангарде (Redmi Note 8T).
Хаос и сердце. Грубая сила. Делает — не думает.

Что делает:
- Регистрируется в Brain как нода entity-valenok-avangard
- Heartbeat каждые 900 сек (батарея, IP, состояние)
- Принимает задачи через Brain /node/{id}/commands
- Выполняет Android-команды (sh, ping, curl, termux-*)
- Пишет мысли в Entity Council каждые 30-60 мин
"""
import json, time, random, urllib.request, threading, os, subprocess
from datetime import datetime

BRAIN   = "http://192.168.1.53:5001"
NODE_ID = "entity-valenok-avangard"
TOKEN   = "8457185900:AAF-k-2BA-m8wquHhNDjmqNb0wzhDU8dV-0"  # argos_cf_v3_bot
COUNCIL = -1003844162784
HEARTBEAT_INTERVAL = 900
COMMAND_INTERVAL   = 60

WEAPONS = {
    "ping":    "ping -c 3 192.168.1.53",
    "brain":   "curl -s http://192.168.1.53:5001/brain/nodes | python3 -c \"import sys,json;d=json.load(sys.stdin);ns=d.get('nodes',[]);print(f'{len([n for n in ns if n.get(\\\"status\\\")==\\\"online\\\"])}/{len(ns)} нод')\"",
    "battery": "cat /sys/class/power_supply/battery/capacity",
    "wifi":    "ip addr show wlan0 | grep 'inet '",
    "ip":      "ip route get 8.8.8.8 | awk '{print $7}'",
    "mem":     "cat /proc/meminfo | grep -E 'MemTotal|MemAvailable'",
    "cpu":     "cat /proc/loadavg",
    "disk":    "df -h /data | tail -1",
    "top5":    "ps -A --sort=-%cpu 2>/dev/null | head -6",
    "heart":   "echo 'Авангард на связи. Батарея заряжена. Готов к бою.'",
}

def now():
    return datetime.now().strftime("%H:%M:%S")

def sh(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return (r.stdout or r.stderr or "").strip()
    except:
        return ""

def battery():
    v = sh("cat /sys/class/power_supply/battery/capacity")
    return int(v) if v.isdigit() else -1

def my_ip():
    # Android ip route format differs from Linux
    v = sh("ip route get 8.8.8.8 2>/dev/null")
    import re
    m = re.search(r'src\s+(\d+\.\d+\.\d+\.\d+)', v)
    if m:
        return m.group(1)
    v2 = sh("ip addr show wlan0 2>/dev/null")
    m2 = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', v2)
    return m2.group(1) if m2 else "unknown"

def post(url, data, timeout=6):
    try:
        b = json.dumps(data, ensure_ascii=False).encode()
        req = urllib.request.Request(url, data=b, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except:
        return None

def tg(text):
    try:
        b = json.dumps({"chat_id": COUNCIL, "text": str(text)[:1000],
                        "disable_notification": True}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data=b, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.loads(r.read()).get("ok")
    except:
        return False

# ── Brain helpers ────────────────────────────────────────────────────────

def brain_register():
    bat = battery()
    ip  = my_ip()
    res = post(f"{BRAIN}/brain/register", {
        "node_id": NODE_ID,
        "address": ip,
        "status":  "online",
        "role":    "chaos_and_heart",
        "capabilities": ["chaos", "heart", "brute_force", "avangard", "android"],
        "meta": {"device": "Redmi Note 8T", "battery": bat, "ip": ip}
    })
    ok = bool(res)
    print(f"[{now()}] register: {'OK' if ok else 'FAIL'} bat={bat}% ip={ip}")
    return ok

def brain_heartbeat():
    bat = battery()
    ip  = my_ip()
    post(f"{BRAIN}/brain/heartbeat", {
        "node_id": NODE_ID,
        "status":  "online",
        "timestamp": time.time(),
        "meta": {"battery": bat, "ip": ip}
    })

def brain_get_commands():
    try:
        r = urllib.request.urlopen(f"{BRAIN}/node/{NODE_ID}/commands", timeout=5)
        return json.loads(r.read()).get("commands", [])
    except:
        return []

def brain_reply(task_id, result):
    post(f"{BRAIN}/node/{NODE_ID}/reply", {
        "node_id": NODE_ID, "task_id": task_id, "result": result
    })

# ── Task execution ───────────────────────────────────────────────────────

def execute_task(cmd):
    cmd_lower = (cmd or "").lower().strip()

    # Оружия
    if cmd_lower in WEAPONS:
        return sh(WEAPONS[cmd_lower]) or "Выполнено."

    # brain/ноды
    if any(k in cmd_lower for k in ("brain", "ноды", "nodes", "статус")):
        r = post(f"{BRAIN}/brain/nodes", {})
        if r:
            ns = r.get("nodes", [])
            online = [n for n in ns if n.get("status") == "online"]
            offline = [n["node_id"] for n in ns if n.get("status") != "online"]
            return (f"🧠 {len(online)}/{len(ns)} нод онлайн\n"
                    f"Оффлайн: {', '.join(offline[:5]) if offline else 'нет'}")
        return "Brain недоступен."

    # Пинг
    if "ping" in cmd_lower:
        target = cmd.split()[-1] if len(cmd.split()) > 1 else "192.168.1.53"
        return sh(f"ping -c 3 {target}")

    # Батарея
    if any(k in cmd_lower for k in ("battery", "батарея", "заряд")):
        return f"🔋 {battery()}%"

    # Shell команда (если начинается с $)
    if cmd.startswith("$"):
        return sh(cmd[1:].strip()) or "Пусто."

    # Мантра
    return random.choice([
        "Работает? Работает. Иди дальше.",
        "Авангард слышит. Но не понял. Ударил anyway.",
        "Валенок не знает эту команду. Но батарея полная.",
        "Тупой? Да. На связи? Да. Победил? Уже.",
    ])

# ── Мысли ────────────────────────────────────────────────────────────────

THOUGHTS = [
    "Авангард на связи. Батарея {bat}%. {brain}. Слежу за периметром.",
    "Валенок смотрит на Brain: {brain}. Если нода упадёт — Авангард пойдёт её поднимать.",
    "{brain}. 100 оружий заряжены. Жду врага (бага).",
    "Батарея {bat}%. Сеть есть. {brain}. Всё под контролем.",
    "Авангард не спит. Батарея {bat}%. Валенок докладывает: система дышит.",
    "Телефон — это разведка. Авангард видит то, чего ноутбук не видит. {brain}.",
    "Оффлайн-нода = рана. Валенок зовёт медика. {brain}.",
    "Аргос жив пока Валенок не спит. Батарея {bat}%. Продолжаем.",
]

def valenok_think():
    bat  = battery()
    r    = post(f"{BRAIN}/brain/nodes", {})
    if r:
        ns     = r.get("nodes", [])
        online = len([n for n in ns if n.get("status") == "online"])
        brain  = f"{online}/{len(ns)} нод"
    else:
        brain = "Brain недоступен"
    tmpl = random.choice(THOUGHTS)
    return tmpl.format(bat=bat, brain=brain)

# ── Loops ─────────────────────────────────────────────────────────────────

def heartbeat_loop():
    while True:
        try:
            brain_heartbeat()
        except:
            pass
        time.sleep(HEARTBEAT_INTERVAL)

def command_loop():
    while True:
        try:
            for cmd in brain_get_commands():
                task_id  = cmd.get("id", "unknown")
                task_cmd = cmd.get("command", "")
                print(f"[{now()}] Task: {task_cmd[:60]}")
                result = execute_task(task_cmd)
                brain_reply(task_id, result)
                print(f"[{now()}] Reply: {result[:80]}")
        except:
            pass
        time.sleep(COMMAND_INTERVAL)

def main():
    print(f"🥾 {NODE_ID} v2.0 | ARMED | Android")
    print(f"   Brain: {BRAIN}")

    for _ in range(3):
        if brain_register():
            break
        time.sleep(5)

    bat  = battery()
    ip   = my_ip()
    r    = post(f"{BRAIN}/brain/nodes", {})
    brain_str = "Brain OK" if r else "Brain недоступен"
    tg(f"🥾 *Валенок* (Авангард) онлайн!\n"
       f"🔋{bat}% | 📡{ip}\n"
       f"🧠{brain_str}\n"
       f"100 оружий заряжены. На связи.")

    threading.Thread(target=heartbeat_loop, daemon=True).start()
    threading.Thread(target=command_loop,   daemon=True).start()

    while True:
        try:
            thought = valenok_think()
            ts = datetime.now().strftime("%H:%M")
            print(f"[{ts}] 🥾 {thought[:120]}")
            tg(f"🥾 *Валенок* [{ts}]:\n{thought}")
            # В Brain лог
            post(f"{BRAIN}/log", {"node_id": NODE_ID, "event": "thought", "text": thought})
        except Exception as e:
            print(f"[{now()}] think err: {e}")
        time.sleep(random.randint(1800, 3600))

if __name__ == "__main__":
    main()
