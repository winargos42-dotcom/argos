#!/usr/bin/env python3
"""
ARGOS → Home Assistant metrics pusher
Pushes system metrics from all nodes to HA sensors every 60 seconds.
"""
import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

HA_URL = os.getenv("HA_URL", "http://localhost:8123")
HA_TOKEN = os.getenv("HA_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjMWIwZDgxNzdkNDY0NGRjOWM4YmI4OGZiM2VkOGRjZSIsImlhdCI6MTc3NzkyMDY5MiwiZXhwIjoyMDkzMjgwNjkyfQ.nV0ps3wDPz4NAiqwKCyyTLcwK-oxUdvg2ohIG4p6Ozs")
BRAIN_URL = os.getenv("ARGOS_BRAIN_URL", "http://localhost:5001")
ORANGEPI_URL = "http://192.168.2.168:7777"
INTERVAL = int(os.getenv("HA_PUSH_INTERVAL", "60"))


def ha_set(entity_id: str, state: str, attrs: dict = None):
    """Set HA sensor state."""
    payload = {"state": str(state), "attributes": attrs or {}}
    try:
        req = urllib.request.Request(
            f"{HA_URL}/api/states/{entity_id}",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {HA_TOKEN}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  ⚠️ HA set {entity_id} failed: {e}")
        return None


def get_laptop_metrics() -> dict:
    """Collect laptop system metrics."""
    m = {}
    try:
        m["cpu_temp"] = round(int(open("/sys/class/thermal/thermal_zone0/temp").read().strip()) / 1000.0, 1)
    except: m["cpu_temp"] = None
    try:
        load = open("/proc/loadavg").read().split()
        m["load_1m"] = float(load[0])
        m["load_5m"] = float(load[1])
        m["load_15m"] = float(load[2])
    except: pass
    try:
        meminfo = {}
        for line in open("/proc/meminfo"):
            k, v = line.split(":")
            meminfo[k.strip()] = int(v.split()[0])
        total = meminfo.get("MemTotal", 0)
        avail = meminfo.get("MemAvailable", 0)
        m["mem_total_mb"] = round(total / 1024, 1)
        m["mem_avail_mb"] = round(avail / 1024, 1)
        m["mem_used_pct"] = round((1 - avail / total) * 100, 1) if total else 0
    except: pass
    try:
        st = os.statvfs("/")
        m["disk_free_gb"] = round(st.f_bavail * st.f_frsize / 1e9, 1)
        m["disk_used_pct"] = round((1 - st.f_bavail / st.f_blocks) * 100, 1) if st.f_blocks else 0
    except: pass
    return m


def get_orangepi_metrics() -> dict:
    """Collect Orange Pi metrics via HTTP."""
    try:
        req = urllib.request.Request(f"{ORANGEPI_URL}/system")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read()).get("system", {})
    except:
        return {}


def get_brain_status() -> dict:
    """Get Brain API P2P status."""
    try:
        req = urllib.request.Request(f"{BRAIN_URL}/brain/nodes")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            nodes = data.get("nodes", [])
            return {
                "total_nodes": len(nodes),
                "online_nodes": sum(1 for n in nodes if n.get("status") == "online"),
                "nodes": [n.get("node_id", "?") for n in nodes],
            }
    except:
        return {"total_nodes": 0, "online_nodes": 0, "nodes": []}


def get_esp_status() -> dict:
    """Check ESP devices status."""
    esp = {}
    # ESP32 Display (MicroPython, SSD1306 + WS2812B)
    try:
        req = urllib.request.Request("http://192.168.1.211/?text=HEARTBEAT")
        with urllib.request.urlopen(req, timeout=5) as resp:
            ok = resp.read().decode().strip() == "OK"
        esp["esp32_display"] = {"online": ok, "ip": "192.168.1.211", "type": "esp32"}
    except:
        esp["esp32_display"] = {"online": False, "ip": "192.168.1.211", "type": "esp32"}
    # ESP8266 Bridge (ESPHome, WiFi+MQTT)
    try:
        req = urllib.request.Request("http://192.168.1.181/")
        with urllib.request.urlopen(req, timeout=5) as resp:
            ok = resp.status == 200
        esp["esp8266_bridge"] = {"online": ok, "ip": "192.168.1.181", "type": "esp8266"}
    except:
        esp["esp8266_bridge"] = {"online": False, "ip": "192.168.1.181", "type": "esp8266"}
    return esp


def send_pc_heartbeat():
    """Send heartbeat for argos-pc via Brain API (PC P2P agent may not be running)."""
    PC_BRAIN_URL = "http://192.168.1.53:5001"
    try:
        # First check if PC Brain is alive
        req = urllib.request.Request(f"{PC_BRAIN_URL}/health")
        with urllib.request.urlopen(req, timeout=5):
            pass
    except:
        print("  ⚠️ PC Brain unreachable, skipping PC heartbeat")
        return False

    # Get PC Ollama models
    pc_models = []
    try:
        req = urllib.request.Request(f"http://192.168.1.53:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            pc_models = [m["name"] for m in data.get("models", [])]
    except:
        pass

    # Send heartbeat to laptop's Brain API on behalf of PC
    try:
        payload = json.dumps({
            "node_id": "argos-pc",
            "status": "online",
            "models": pc_models,
        }).encode()
        req = urllib.request.Request(
            f"{BRAIN_URL}/brain/heartbeat",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            if result.get("status") == "ok":
                print(f"  ✅ PC heartbeat sent ({len(pc_models)} models)")
                return True
    except Exception as e:
        print(f"  ⚠️ PC heartbeat failed: {e}")
    return False


def push_all_metrics():
    """Push all metrics to HA."""
    ts = datetime.now(timezone.utc).isoformat()
    print(f"\n📊 [{ts}] Pushing metrics to HA...")

    # Laptop metrics
    laptop = get_laptop_metrics()
    if laptop.get("cpu_temp"):
        ha_set("sensor.argos_x230_argos_x230_cpu_temperatura",
               str(laptop["cpu_temp"]),
               {"unit_of_measurement": "°C", "friendly_name": "ARGOS X230 CPU Температура",
                "icon": "mdi:thermometer", "source": "argos_metrics_pusher"})
        print(f"  ✅ CPU temp: {laptop['cpu_temp']}°C")

    if laptop.get("load_1m"):
        ha_set("sensor.argos_x230_argos_x230_cpu_nagruzka",
               str(laptop["load_1m"]),
               {"unit_of_measurement": "load", "friendly_name": "ARGOS X230 CPU Нагрузка",
                "icon": "mdi:cpu-64-bit", "source": "argos_metrics_pusher",
                "load_5m": laptop.get("load_5m"), "load_15m": laptop.get("load_15m")})
        print(f"  ✅ CPU load: {laptop['load_1m']}")

    if laptop.get("mem_used_pct"):
        ha_set("sensor.argos_x230_argos_x230_ram_ispolzovanie",
               str(laptop["mem_used_pct"]),
               {"unit_of_measurement": "%", "friendly_name": "ARGOS X230 RAM Использование",
                "icon": "mdi:memory", "source": "argos_metrics_pusher",
                "mem_total_mb": laptop.get("mem_total_mb"), "mem_avail_mb": laptop.get("mem_avail_mb")})
        print(f"  ✅ RAM: {laptop['mem_used_pct']}%")

    # Orange Pi metrics
    opi = get_orangepi_metrics()
    if opi.get("cpu_temp"):
        ha_set("sensor.orange_pi_one_orangepi_cpu_temperatura",
               str(opi["cpu_temp"]),
               {"unit_of_measurement": "°C", "friendly_name": "OrangePi CPU Температура",
                "icon": "mdi:thermometer", "source": "argos_metrics_pusher"})
        print(f"  ✅ OPi temp: {opi['cpu_temp']}°C")

    if opi.get("load"):
        ha_set("sensor.orange_pi_one_orangepi_cpu_nagruzka",
               str(opi["load"][0]) if isinstance(opi["load"], list) else str(opi["load"]),
               {"unit_of_measurement": "load", "friendly_name": "OrangePi CPU Нагрузка",
                "icon": "mdi:cpu-32-bit", "source": "argos_metrics_pusher"})
        print(f"  ✅ OPi load: {opi.get('load')}")

    # Brain status
    brain = get_brain_status()
    ha_set("sensor.argos_brain_status",
           str(brain.get("online_nodes", 0)),
           {"friendly_name": "ARGOS Brain Nodes Online",
            "icon": "mdi:server-network", "source": "argos_metrics_pusher",
            "total_nodes": brain.get("total_nodes", 0),
            "nodes": ", ".join(brain.get("nodes", []))})
    print(f"  ✅ Brain nodes: {brain.get('online_nodes', 0)}/{brain.get('total_nodes', 0)}")

    # ESP devices status
    esp = get_esp_status()
    esp_online = sum(1 for v in esp.values() if v["online"])
    ha_set("sensor.argos_esp_devices",
           str(esp_online),
           {"friendly_name": "ARGOS ESP Devices Online",
            "icon": "mdi:chip", "source": "argos_metrics_pusher",
            "total_esp": len(esp),
            "devices": ", ".join(f"{k}:{'online' if v['online'] else 'offline'}" for k, v in esp.items())})
    print(f"  ✅ ESP devices: {esp_online}/{len(esp)} online")
    
    # Individual ESP sensors
    for name, data in esp.items():
        ha_set(f"binary_sensor.argos_{name}",
               "on" if data["online"] else "off",
               {"friendly_name": f"ARGOS {name.replace('_', ' ').title()}",
                "device_class": "connectivity", "source": "argos_metrics_pusher",
                "ip": data["ip"], "type": data["type"]})
    
    # PC heartbeat (keep P2P node alive)
    send_pc_heartbeat()


def main():
    print(f"📊 ARGOS HA Metrics Pusher — interval: {INTERVAL}s")
    while True:
        try:
            push_all_metrics()
        except Exception as e:
            print(f"  ❌ Error: {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()


def push_argos_system_to_ha():
    """Push all 5 ARGOS machines status to HA."""
    import urllib.request, json, os
    HA = os.getenv("HA_URL", "http://localhost:8123")
    TOKEN = os.getenv("HA_TOKEN", "")
    if not TOKEN:
        return

    machines = {
        "sensor.argos_laptop": {"state": "online", "attrs": {"role": "dev_station", "ip": "192.168.1.53"}},
    }

    # Проверяем каждую машину
    checks = [
        ("sensor.argos_pc_v2", "http://192.168.1.53:8000/health", "server"),
        ("sensor.argos_opiiot", "http://192.168.2.168:7777", "iot"),
        ("sensor.argos_gcp_v2", "https://argos-core-m3gk27ccqa-uc.a.run.app/health", "cloud"),
    ]
    for entity, url, role in checks:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=6) as r:
                d = json.loads(r.read())
                state = "online" if d.get("ok", d.get("node")) else "offline"
        except:
            state = "offline"
        machines[entity] = {"state": state, "attrs": {"role": role}}

    for eid, info in machines.items():
        try:
            payload = json.dumps({"state": info["state"], "attributes": info["attrs"]}).encode()
            req = urllib.request.Request(
                f"{HA}/api/states/{eid}",
                data=payload,
                headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
                method="POST"
            )
            urllib.request.urlopen(req, timeout=5)
        except:
            pass
