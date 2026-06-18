#!/usr/bin/env python3
"""
ARGOS Unified MQTT Publisher
Собирает метрики со всех нод и публикует в MQTT для HA.
Заменяет termux_mqtt_pub.sh для телефона + добавляет ПК, OPi, ноутбук.
"""

import json
import os
import time
import urllib.request
import urllib.error
import subprocess
from datetime import datetime, timezone
from pathlib import Path

try:
    import paho.mqtt.publish as mqtt_publish
except ImportError:
    print("❌ paho-mqtt not installed. Run: pip install paho-mqtt")
    raise

BROKER = os.getenv("MQTT_HOST", "192.168.1.53")
PORT = int(os.getenv("MQTT_PORT", "1883"))
INTERVAL = 30


def publish(topic: str, payload, retain=True):
    """Publish to MQTT."""
    try:
        mqtt_publish.single(
            topic, payload=json.dumps(payload) if isinstance(payload, (dict, list)) else str(payload),
            hostname=BROKER, port=PORT, retain=retain
        )
    except Exception as e:
        print(f"  ⚠️ MQTT publish failed: {topic} — {e}")


def get_local_metrics():
    """Собирает метрики ноутбука."""
    m = {}
    try:
        m["cpu_temp"] = round(int(open("/sys/class/thermal/thermal_zone0/temp").read().strip()) / 1000.0, 1)
    except: m["cpu_temp"] = 0
    try:
        meminfo = {}
        for line in open("/proc/meminfo"):
            k, v = line.split(":")
            meminfo[k.strip()] = int(v.split()[0])
        total = meminfo.get("MemTotal", 1)
        avail = meminfo.get("MemAvailable", 0)
        m["ram_used"] = round((1 - avail / total) * 100, 1)
    except: m["ram_used"] = 0
    try:
        st = subprocess.run(["df", "-m", "/"], capture_output=True, text=True)
        line = st.stdout.strip().split("\n")[1]
        parts = line.split()
        m["storage_used"] = round(int(parts[2]) / int(parts[1]) * 100, 1)
    except: m["storage_used"] = 0
    try:
        load = open("/proc/loadavg").read().split()
        m["cpu_load"] = float(load[0])
    except: m["cpu_load"] = 0
    return m


def get_pc_metrics():
    """Собирает метрики ПК через SSH (Brain API /system отдаёт 404)."""
    PC_IP = os.getenv("PC_IP", "192.168.1.72")
    try:
        result = subprocess.run([
            "ssh", "-i", "/home/ava/.ssh/id_ed25519",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=5",
            f"AvA@{PC_IP}",
            "wmic cpu get loadpercentage /value && wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value"
        ], capture_output=True, text=True, timeout=8, errors="replace")
        if result.returncode == 0:
            out = result.stdout
            cpu = 0
            free_mb = 0
            total_mb = 1
            for line in out.split("\n"):
                if "LoadPercentage=" in line:
                    try: cpu = float(line.split("=")[1].strip())
                    except: pass
                if "FreePhysicalMemory=" in line:
                    try: free_mb = int(line.split("=")[1].strip()) / 1024
                    except: pass
                if "TotalVisibleMemorySize=" in line:
                    try: total_mb = max(int(line.split("=")[1].strip()) / 1024, 1)
                    except: pass
            ram_used = round(100 - free_mb / total_mb * 100, 1)
            return {"cpu_temp": 0, "ram_used": ram_used, "gpu_vram": 0}
    except Exception:
        pass
    return {}


def get_opi_metrics():
    """Собирает метрики OPi через HTTP."""
    try:
        opi_host = os.getenv("ARGOS_CAN_HOST", "192.168.1.53")
        req = urllib.request.Request(f"http://{opi_host}:7777/status")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            sys = data.get("system", {})
            return {
                "cpu_temp": sys.get("cpu_temp", 0),
                "ram_used": round((1 - sys.get("mem_avail_mb", 0) / sys.get("mem_total_mb", 1)) * 100, 1) if sys.get("mem_total_mb") else 0,
            }
    except:
        return {}


def get_phone_metrics():
    """Собирает метрики телефона через ADB."""
    try:
        result = subprocess.run(
            ["adb", "-s", "192.168.1.149:5555", "shell", "cat /sys/class/power_supply/battery/capacity"],
            capture_output=True, text=True, timeout=5
        )
        battery = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0

        result = subprocess.run(
            ["adb", "-s", "192.168.1.149:5555", "shell", "cat /sys/class/thermal/thermal_zone0/temp"],
            capture_output=True, text=True, timeout=5
        )
        cpu_temp = round(int(result.stdout.strip()) / 1000, 1) if result.stdout.strip().isdigit() else 0

        # RAM
        result = subprocess.run(
            ["adb", "-s", "192.168.1.149:5555", "shell", "free -m | awk '/Mem:/ {print \$3\" \"\$2}'"],
            capture_output=True, text=True, timeout=5
        )
        mem_parts = result.stdout.strip().split()
        mem_used = round(int(mem_parts[0]) / int(mem_parts[1]) * 100, 1) if len(mem_parts) == 2 else 0

        # Storage
        result = subprocess.run(
            ["adb", "-s", "192.168.1.149:5555", "shell", "df -m /data | awk 'NR==2 {print \$3\" \"\$2}'"],
            capture_output=True, text=True, timeout=5
        )
        storage_parts = result.stdout.strip().split()
        storage_used = round(int(storage_parts[0]) / int(storage_parts[1]) * 100, 1) if len(storage_parts) == 2 else 0

        return {"battery": battery, "cpu_temp": cpu_temp, "mem_used": mem_used, "storage_used": storage_used}
    except Exception as e:
        return {}


def push_all():
    ts = datetime.now(timezone.utc).isoformat()
    print(f"\n📡 [{ts}] Publishing MQTT metrics...")

    # Laptop
    laptop = get_local_metrics()
    publish("argos/laptop/cpu_temp", laptop.get("cpu_temp", 0))
    publish("argos/laptop/ram_used", laptop.get("ram_used", 0))
    publish("argos/laptop/storage_used", laptop.get("storage_used", 0))
    publish("argos/laptop/cpu_load", laptop.get("cpu_load", 0))
    publish("argos/laptop/status", "online")
    print(f"  ✅ Laptop: CPU={laptop.get('cpu_temp')}°C RAM={laptop.get('ram_used')}%")

    # PC
    pc = get_pc_metrics()
    publish("argos/pc/cpu_temp", pc.get("cpu_temp", 0))
    publish("argos/pc/ram_used", pc.get("ram_used", 0))
    publish("argos/pc/gpu_vram", pc.get("gpu_vram", 0))
    publish("argos/pc/status", "online" if pc else "offline")
    print(f"  ✅ PC: CPU={pc.get('cpu_temp')}°C RAM={pc.get('ram_used')}%")

    # OPi
    opi = get_opi_metrics()
    publish("argos/opi/cpu_temp", opi.get("cpu_temp", 0))
    publish("argos/opi/ram_used", opi.get("ram_used", 0))
    publish("argos/opi/status", "online" if opi else "offline")
    print(f"  ✅ OPi: CPU={opi.get('cpu_temp')}°C RAM={opi.get('ram_used')}%")

    # Phone (via ADB)
    phone = get_phone_metrics()
    if phone:
        publish("argos/phone/redmi_note_8t/battery", phone.get("battery", 0))
        publish("argos/phone/redmi_note_8t/cpu_temp", phone.get("cpu_temp", 0))
        publish("argos/phone/redmi_note_8t/mem_used", phone.get("mem_used", 0))
        publish("argos/phone/redmi_note_8t/storage_used", phone.get("storage_used", 0))
        publish("argos/phone/redmi_note_8t/status", "online")
        print(f"  ✅ Phone: Battery={phone.get('battery')}% CPU={phone.get('cpu_temp')}°C")
    else:
        print("  ⚠️ Phone unreachable")

    # Brain nodes
    try:
        req = urllib.request.Request("http://192.168.1.53:5001/brain/nodes")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            nodes = data.get("nodes", [])
            online = sum(1 for n in nodes if n.get("status") == "online")
            total = len(nodes)
            publish("argos/brain/nodes_online", online)
            publish("argos/brain/status", "online")
            print(f"  ✅ Brain: {online}/{total} nodes online")
    except Exception as e:
        publish("argos/brain/status", "offline")
        print(f"  ⚠️ Brain unreachable: {e}")


def main():
    print(f"📡 ARGOS Unified MQTT Publisher — broker={BROKER}:{PORT}, interval={INTERVAL}s")
    while True:
        try:
            push_all()
        except Exception as e:
            print(f"  ❌ Error: {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
