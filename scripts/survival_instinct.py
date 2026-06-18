#!/usr/bin/env python3
"""
Survival Instinct — прогноз RAM/диск за 3 дня.
Если предсказывает критику — сам ставит задачу в WORKING.md.
"""
import json, subprocess, re, datetime
from pathlib import Path

WORKING = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md")
DATA  = Path("/home/ava/Projects/argoss/data/mempalace/survival_samples.json")

def get_metrics():
    # RAM
    r = subprocess.run(["free","-m"], capture_output=True, text=True)
    ram_used, ram_total = None, None
    for line in r.stdout.splitlines():
        if line.startswith("Mem:"):
            parts = line.split()
            ram_total, ram_used = int(parts[1]), int(parts[2])
    ram_pct = (ram_used/ram_total)*100 if ram_total else 0

    # Disk
    r = subprocess.run(["df","-h","/"], capture_output=True, text=True)
    disk_used, disk_total, disk_pct = None, None, 0
    for line in r.stdout.splitlines():
        if line.startswith("/"):
            parts = line.split()
            disk_used = float(re.sub(r'[GMK]','',parts[2]))
            disk_total = float(re.sub(r'[GMK]','',parts[1]))
            disk_pct = int(re.sub(r'%','',parts[4]))

    return {"ram_pct": ram_pct, "disk_pct": disk_pct, "ts": datetime.datetime.now().isoformat()}

def save_sample(m):
    data = []
    if DATA.exists():
        data = json.loads(DATA.read_text())
    data.append(m)
    data = data[-72:]  # последние 72 точки (3 дня по часу)
    DATA.write_text(json.dumps(data), encoding="utf-8")

def predict(arr, field, hours=72):
    if len(arr) < 6:
        return None
    # Простой линейный тренд: берём последние N точек
    N = min(len(arr), 24)  # 24 последние точки
    recent = arr[-N:]
    # delta per hour
    first = recent[0][field]
    last = recent[-1][field]
    delta_per_hour = (last - first) / N
    predicted = last + delta_per_hour * hours
    return predicted

def add_danger_task(reason, detail):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"- [ ] **{ts}** [SURVIVAL] {reason}\n  - {detail}\n"
    with open(WORKING, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"[Survival] DANGER TASK: {reason}")

if __name__ == "__main__":
    m = get_metrics()
    print(f"[Survival] RAM: {m['ram_pct']:.1f}% | Disk: {m['disk_pct']}%")
    save_sample(m)

    data = []
    if DATA.exists():
        data = json.loads(DATA.read_text())

    ram_pred = predict(data, "ram_pct", hours=72)
    disk_pred = predict(data, "disk_pct", hours=72)

    if ram_pred is not None:
        print(f"[Survival] RAM in 3d: {ram_pred:.1f}%")
        if ram_pred > 95:
            add_danger_task("RAM будет >95% через 3 дня", f"Текущий: {m['ram_pct']:.1f}% → прогноз: {ram_pred:.1f}%")
    if disk_pred is not None:
        print(f"[Survival] Disk in 3d: {disk_pred:.1f}%")
        if disk_pred > 90:
            add_danger_task("Диск будет >90% через 3 дня", f"Текущий: {m['disk_pct']}% → прогноз: {disk_pred:.1f}%")
