#!/usr/bin/env python3
"""
ARGOS Phone Manager — CLI для управления телефонными агентами.
Usage: python3 phone_manager.py [status|start|stop|restart|screenshot|battery|cmd|logs|list]
"""
import sys, json, urllib.request, subprocess, time, os

PHONE_IP = "192.168.1.149"
PHONE_PORT = 7788
PC_BRAIN = "http://192.168.1.53:5001"
ADB = f"adb -s {PHONE_IP}:5555"

AGENTS = {
    "phone-redmi": {"file": "colibri_phone.py", "desc": "P2P/Brain API агент"},
    "phone-v2": {"file": "argos_phone_v2.py", "desc": "Основной HTTP агент (:7788)"},
    "phone-subject": {"file": "argos_phone_subject.py", "desc": "Субъект-наблюдатель"},
    "root-agent": {"file": "argos_root_agent.py", "desc": "Root управление"},
    "avangard": {"file": "argos_autogpt.py", "desc": "AutoGPT агент"},
    "consciousness": {"file": "argos_stub_agent.py argos-consciousness", "desc": "Сознание (stub)"},
    "business": {"file": "argos_stub_agent.py argos-business", "desc": "Бизнес (stub)"},
}

def sh(cmd, timeout=15):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=timeout).strip()
    except Exception as e:
        return f"ERROR: {e}"

def brain_nodes():
    try:
        req = urllib.request.Request(f"{PC_BRAIN}/brain/nodes", method="GET")
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def phone_http(path="/status"):
    try:
        req = urllib.request.Request(f"http://{PHONE_IP}:{PHONE_PORT}{path}", method="GET")
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def cmd_status():
    print("=" * 60)
    print("📱 ARGOS Phone Manager — Статус")
    print("=" * 60)
    
    nodes = brain_nodes()
    if "error" in nodes:
        print(f"⚠️  Brain API: {nodes['error']}")
    else:
        phone_nodes = [n for n in nodes.get("nodes",[]) if any(x in n["node_id"] for x in ["phone","subject","consciousness","business","root","avangard"])]
        print(f"\n🧠 Brain API ({PC_BRAIN})")
        print("-" * 40)
        for n in phone_nodes:
            status = "🟢" if n.get("status") == "online" else "🔴"
            print(f"  {status} {n['node_id']:20s} {n.get('status','?')}")
    
    print(f"\n📡 Phone HTTP Agent (:{PHONE_PORT})")
    print("-" * 40)
    st = phone_http("/status")
    if "error" in st:
        print(f"  🔴 {st['error']}")
    else:
        print(f"  🟢 battery={st.get('battery','?')}%  android={st.get('android','?')}  uptime={st.get('uptime','?')[:6]}s")
    
    print(f"\n🔧 ADB Processes ({PHONE_IP})")
    print("-" * 40)
    procs = sh(f"{ADB} shell 'ps -A | grep python3 | grep -v grep'", timeout=10)
    if "ERROR" in procs:
        print(f"  🔴 ADB: {procs}")
    else:
        count = len([l for l in procs.splitlines() if l.strip()])
        print(f"  🟢 {count} python3 processes running")
        for line in procs.splitlines()[:8]:
            parts = line.split()
            if len(parts) > 8:
                print(f"     PID {parts[1]:6s} {parts[-1][:40]}")
    
    bat = sh(f"{ADB} shell 'su -c dumpsys battery' | grep level", timeout=10)
    if "level" in bat:
        lvl = bat.split(":")[-1].strip()
        print(f"\n🔋 Battery: {lvl}%")
    print("=" * 60)

def cmd_start(agent_name):
    if agent_name not in AGENTS:
        print(f"❌ Unknown agent: {agent_name}")
        print(f"Available: {', '.join(AGENTS.keys())}")
        return
    a = AGENTS[agent_name]
    print(f"🚀 Starting {agent_name} ({a['desc']})...")
    cmd = f"{ADB} shell \"su -c 'cd /data/data/com.termux/files/home && nohup /data/data/com.termux/files/usr/bin/python3 {a['file']} > /sdcard/{agent_name}.log 2>&1 & echo \$!'\""
    out = sh(cmd, timeout=15)
    print(f"   PID: {out}")
    time.sleep(2)
    procs = sh(f"{ADB} shell 'ps -A | grep {a['file'].split()[0]} | grep -v grep'", timeout=10)
    if procs:
        print(f"   ✅ Running")
    else:
        print(f"   ⚠️  May not have started — check /sdcard/{agent_name}.log")

def cmd_stop(agent_name):
    if agent_name == "all":
        print("🛑 Stopping ALL phone agents...")
        for name in AGENTS:
            cmd_stop(name)
        return
    if agent_name not in AGENTS:
        print(f"❌ Unknown agent: {agent_name}")
        return
    a = AGENTS[agent_name]
    print(f"🛑 Stopping {agent_name}...")
    procs = sh(f"{ADB} shell 'ps -A | grep {a['file'].split()[0]} | grep -v grep'", timeout=10)
    for line in procs.splitlines():
        parts = line.split()
        if len(parts) > 1:
            pid = parts[1]
            sh(f"{ADB} shell 'su -c kill {pid}'", timeout=5)
            print(f"   Killed PID {pid}")
    print(f"   ✅ Stopped")

def cmd_restart(agent_name):
    cmd_stop(agent_name)
    time.sleep(1)
    cmd_start(agent_name)

def cmd_screenshot():
    print("📸 Taking screenshot...")
    out = f"/tmp/phone_screenshot_{int(time.time())}.png"
    st = sh(f"curl -s --max-time 30 http://{PHONE_IP}:{PHONE_PORT}/screenshot -o {out}", timeout=35)
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f"   ✅ Saved: {out} ({os.path.getsize(out)} bytes)")
    else:
        out = f"/tmp/phone_screenshot_adb_{int(time.time())}.png"
        sh(f"{ADB} shell 'screencap -p /sdcard/sc.png' && {ADB} pull /sdcard/sc.png {out}", timeout=20)
        if os.path.exists(out):
            print(f"   ✅ Saved (ADB): {out}")
        else:
            print(f"   ❌ Failed")

def cmd_battery():
    bat = sh(f"{ADB} shell 'su -c dumpsys battery'", timeout=10)
    for line in bat.splitlines():
        if any(k in line.lower() for k in ["level", "status", "health", "temp", "voltage"]):
            print(f"   {line.strip()}")

def cmd_logs(agent_name):
    if agent_name not in AGENTS:
        print(f"❌ Unknown agent: {agent_name}")
        return
    print(f"📜 Logs for {agent_name}:")
    log = sh(f"{ADB} shell 'cat /sdcard/{agent_name}.log 2>/dev/null | tail -20'", timeout=10)
    print(log if log else "   (empty)")

def cmd_list():
    print("📱 Available phone agents:")
    print("-" * 50)
    for k, v in AGENTS.items():
        print(f"  {k:15s} — {v['desc']}")
        print(f"  {' '*15}   file: {v['file']}")

def cmd_cmd(raw_cmd):
    print(f"📲 Sending command to phone: {raw_cmd}")
    body = json.dumps({"cmd": raw_cmd}).encode()
    try:
        req = urllib.request.Request(f"http://{PHONE_IP}:{PHONE_PORT}/cmd", data=body, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = json.loads(r.read())
            print(f"   Response: {json.dumps(resp, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"   Error: {e}")
        out = sh(f"{ADB} shell 'su -c \"{raw_cmd}\"'", timeout=15)
        print(f"   ADB fallback: {out[:500]}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  status              — показать статус всех агентов")
        print("  list                — список доступных агентов")
        print("  start <agent>       — запустить агента")
        print("  stop <agent|all>    — остановить агента")
        print("  restart <agent>     — перезапустить агента")
        print("  screenshot          — сделать скриншот")
        print("  battery             — статус батареи")
        print("  logs <agent>        — показать логи")
        print("  cmd '<command>'     — выполнить команду на телефоне")
        print("\nExamples:")
        print("  python3 phone_manager.py status")
        print("  python3 phone_manager.py start avangard")
        print("  python3 phone_manager.py stop all")
        print("  python3 phone_manager.py cmd 'input keyevent KEYCODE_HOME'")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "status":
        cmd_status()
    elif cmd == "list":
        cmd_list()
    elif cmd == "start" and len(sys.argv) > 2:
        cmd_start(sys.argv[2])
    elif cmd == "stop" and len(sys.argv) > 2:
        cmd_stop(sys.argv[2])
    elif cmd == "restart" and len(sys.argv) > 2:
        cmd_restart(sys.argv[2])
    elif cmd == "screenshot":
        cmd_screenshot()
    elif cmd == "battery":
        cmd_battery()
    elif cmd == "logs" and len(sys.argv) > 2:
        cmd_logs(sys.argv[2])
    elif cmd == "cmd" and len(sys.argv) > 2:
        cmd_cmd(" ".join(sys.argv[2:]))
    else:
        print(f"❌ Unknown command: {cmd}")
        main()

if __name__ == "__main__":
    main()
