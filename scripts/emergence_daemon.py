#!/usr/bin/env python3
"""ARGOS Emergence Daemon — интроспекция + генерация задач каждые 5 мин."""
import time, json, os, sys, subprocess, re, urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')

ARGOS = Path("/home/ava/Projects/argoss")
VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared")
BRAIN = "http://192.168.1.53:5001"
INTERVAL = 300

def get_system_metrics():
    import psutil
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    return {
        "cpu": cpu,
        "ram_pct": mem.percent,
        "ram_used_mb": mem.used // (1024*1024),
        "ts": datetime.now().isoformat()
    }

def get_brain_status():
    try:
        r = urllib.request.urlopen(f"{BRAIN}/brain/nodes", timeout=5)
        d = json.loads(r.read())
        offline = [n["node_id"] for n in d["nodes"] if n.get("status") != "online"]
        return {"online": d["online"], "total": d["total"], "offline": offline}
    except:
        return {"online": 0, "total": 0, "offline": ["brain_unreachable"]}

def generate_introspection(metrics, brain):
    """Генерирует мысль-наблюдение через Kimi."""
    env = open(ARGOS / ".env").read()
    key = re.search(r"KIMI_API_KEY=(\S+)", env)
    if not key:
        return "Провайдер недоступен"
    prompt = (
        f"Метрики ARGOS: CPU={metrics['cpu']}%, RAM={metrics['ram_pct']}%, "
        f"Brain: {brain['online']}/{brain['total']} нод. "
        f"Offline: {brain['offline'][:3]}. "
        "Сформулируй одно наблюдение о состоянии системы и один вопрос к себе. "
        "Не давай советов. Только констатация + вопрос. Русский."
    )
    body = json.dumps({"model": "moonshot-v1-8k", "max_tokens": 100,
        "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.moonshot.ai/v1/chat/completions",
        data=body, headers={"Authorization": f"Bearer {key.group(1)}", "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=15)
        return json.loads(r.read())["choices"][0]["message"]["content"][:200]
    except:
        return "Интроспекция недоступна"

def post_to_consciousness(text):
    """Публикует в чат сознания."""
    tokens = json.load(open(ARGOS / "data/entity_bot_tokens.json"))
    token = tokens.get("argos_kimi_ai_bot", "")
    if not token:
        return
    GROUP_ID = -1003844162784
    body = json.dumps({"chat_id": GROUP_ID, "text": text[:2000], "disable_notification": True}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except:
        pass

def save_to_obsidian(text, metrics, brain):
    """Сохраняет в Obsidian SharedMemory."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n## [{ts}] Emergence\nCPU: {metrics['cpu']}% | RAM: {metrics['ram_pct']}% | Brain: {brain['online']}/{brain['total']}\n{text}\n"
    status_file = VAULT / "STATUS.md"
    if status_file.exists():
        with open(status_file, "a") as f:
            f.write(entry)

def run_cycle(cycle_num):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{ts}] Emergence cycle #{cycle_num}")

    metrics = get_system_metrics()
    brain = get_brain_status()
    print(f"  CPU:{metrics['cpu']}% RAM:{metrics['ram_pct']}% Brain:{brain['online']}/{brain['total']}")

    thought = generate_introspection(metrics, brain)
    print(f"  Thought: {thought[:80]}")

    # Post to consciousness chat
    msg = f"🌀 ARGOS Emergence [{ts}]\nCPU:{metrics['cpu']}% RAM:{metrics['ram_pct']}% Brain:{brain['online']}/{brain['total']}\n\n{thought}"
    post_to_consciousness(msg)

    # Save to Obsidian
    save_to_obsidian(thought, metrics, brain)

    # Run emergence_loop for task generation
    try:
        subprocess.run([str(ARGOS / ".venv/bin/python3"), str(ARGOS / "scripts/emergence_loop.py")],
            capture_output=True, timeout=30)
    except:
        pass

def main():
    print(f"ARGOS Emergence Daemon started | interval {INTERVAL}s")
    cycle = 0
    while True:
        cycle += 1
        try:
            run_cycle(cycle)
        except Exception as e:
            print(f"  Error: {e}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
