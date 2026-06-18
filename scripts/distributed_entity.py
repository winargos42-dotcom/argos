#!/usr/bin/env python3
"""
Distributed Entity Council — запускает entity на удалённых нодах.
Если Nexus перегружен — перенаправляет на Orion (GPU) или OPi (edge).
"""
import subprocess, requests, json, time, re
from datetime import datetime

NODES = {
    "nexus": {"ip": "192.168.1.53", "weight": 5,  "max_ram_mb": 14000},
    "orion": {"ip": "192.168.1.53", "weight": 10, "max_ram_mb": 48000, "ssh_user": "AvA"},
    "opi":   {"ip": "192.168.2.168", "weight": 3,  "max_ram_mb": 8000,  "ssh_user": "root"},
}

# Threshold для переключения на другую ноду
RAM_THRESHOLD_MB = 12000

def get_node_ram(node):
    """Запрашивает RAM usage ноды через Prometheus node_exporter."""
    try:
        if node == "nexus":
            # Локально — через /proc
            with open("/proc/meminfo") as f:
                info = f.read()
            total = int(re.search(r"MemTotal:\s+(\d+)", info).group(1)) / 1024
            avail = int(re.search(r"MemAvailable:\s+(\d+)", info).group(1)) / 1024
            return total - avail
        else:
            # Удалённо — node_exporter metrics
            url = f"http://{NODES[node]['ip']}:9100/metrics"
            r = requests.get(url, timeout=5)
            # Парсим node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes
            avail = re.search(r'node_memory_MemAvailable_bytes\s+(\d+)', r.text)
            total = re.search(r'node_memory_MemTotal_bytes\s+(\d+)', r.text)
            if avail and total:
                return (float(total.group(1)) - float(avail.group(1))) / (1024*1024)
    except Exception as e:
        return None

def elect_node():
    """Выбирает наименее загруженную ноду."""
    scores = {}
    for node, cfg in NODES.items():
        ram = get_node_ram(node)
        if ram is None:
            scores[node] = float('inf')
        else:
            # Score = текущая RAM / вес (чем меньше, тем лучше)
            scores[node] = ram / cfg["weight"]
    best = min(scores, key=scores.get)
    return best, scores

def spawn_entity(entity_name, node="auto"):
    """Запускает entity на выбранной ноде."""
    if node == "auto":
        node, scores = elect_node()
    
    ts = datetime.now().isoformat()
    print(f"[{ts}] Spawning {entity_name} on {node} (scores: {scores})")
    
    if node == "nexus":
        cmd = ["python3", f"scripts/{entity_name}.py"]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        cfg = NODES[node]
        ssh = [
            "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
            f"{cfg['ssh_user']}@{cfg['ip']}",
            f"cd ~/argoss && source .venv/bin/activate && nohup python3 scripts/{entity_name}.py > /tmp/{entity_name}.log 2>>1 &"
        ]
        subprocess.Popen(ssh)

def heartbeat_all():
    """Отправляет heartbeat для всех узлов в Brain API."""
    for node, cfg in NODES.items():
        try:
            requests.post(
                "http://192.168.1.53:5001/brain/nodes/status",
                json={
                    "node_id": f"distributed_entity_{node}",
                    "status": "active",
                    "weight": cfg["weight"],
                    "ts": datetime.now().isoformat()
                },
                timeout=3
            )
        except:
            pass

if __name__ == "__main__":
    node, scores = elect_node()
    print(f"Optimal node: {node} (scores: {scores})")
    heartbeat_all()
