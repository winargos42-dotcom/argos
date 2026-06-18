#!/usr/bin/env python3
"""Публикует статус всех ARGOS машин в MQTT для Home Assistant binary_sensor."""
import os, time, json, subprocess, requests, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("mqtt_pub")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = os.getenv("MQTT_PORT", "1883")
INTERVAL  = int(os.getenv("MQTT_PUB_INTERVAL", "30"))

BRAIN_URL = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
OPI_URL   = "http://192.168.2.168:7777/status"


def pub(topic: str, payload: str):
    subprocess.run(
        ["mosquitto_pub", "-h", MQTT_HOST, "-p", MQTT_PORT, "-t", topic, "-m", payload],
        capture_output=True, timeout=5
    )


def get_laptop_stats():
    import psutil
    cpu_temp = 0
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = next(iter(temps.values()), [{}])[0].current if temps else 0
    except Exception:
        pass
    return {
        "cpu_temp": round(cpu_temp, 1),
        "ram_used": round(psutil.virtual_memory().percent, 1),
        "disk_used": round(psutil.disk_usage("/").percent, 1),
    }


def get_brain_stats():
    try:
        r = requests.get(f"{BRAIN_URL}/brain/nodes", timeout=5).json()
        return {"online": r.get("online", 0), "total": r.get("total", 0)}
    except Exception:
        return None


def get_opi_stats():
    try:
        r = requests.get(OPI_URL, timeout=5).json()
        s = r.get("system", {})
        return {
            "cpu_temp": s.get("cpu_temp", 0),
            "ram_used": round(100 - s.get("mem_free_mb", 0) / max(s.get("mem_total_mb", 1), 1) * 100, 1),
        }
    except Exception:
        return None


def get_pc_stats():
    """Получаем PC stats через SSH на Windows"""
    import subprocess
    try:
        result = subprocess.run([
            "ssh", "-i", "/home/ava/.ssh/id_ed25519",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=5",
            "AvA@192.168.1.53",
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
            ram_used = round(100 - free_mb/total_mb*100, 1)
            return {"cpu_load": round(cpu, 1), "ram_used": ram_used, "cpu_temp": 0}
    except Exception as e:
        log.debug(f"PC stats error: {e}")
    return None


def publish_all():
    # Ноутбук X230
    laptop = get_laptop_stats()
    pub("argos/laptop/status",   "online")
    pub("argos/laptop/cpu_temp", str(laptop["cpu_temp"]))
    pub("argos/laptop/ram_used", str(laptop["ram_used"]))
    pub("argos/laptop/disk_used", str(laptop["disk_used"]))

    # Brain ПК
    brain = get_brain_stats()
    if brain:
        pub("argos/brain/status",      "online")
        pub("argos/brain/nodes_online", str(brain["online"]))
        pub("argos/pc/status",         "online")
    else:
        pub("argos/brain/status", "offline")
        pub("argos/pc/status",    "offline")

    # Orange Pi
    opi = get_opi_stats()
    if opi:
        pub("argos/opi/status",   "online")
        pub("argos/opi/cpu_temp", str(opi["cpu_temp"]))
        pub("argos/opi/ram_used", str(opi["ram_used"]))
    else:
        pub("argos/opi/status", "offline")

    # ПК stats
    pc = get_pc_stats()
    if pc:
        pub("argos/pc/cpu_load", str(pc["cpu_load"]))
        pub("argos/pc/ram_used", str(pc["ram_used"]))
        pub("argos/pc/gpu_vram", "0")  # GPU VRAM через другой метод
        pub("argos/pc/status", "online")

    # Brain nodes count
    if brain:
        pub("argos/brain/nodes_online", str(brain["online"]))

    log.info(f"Published: laptop={laptop['cpu_temp']}°C brain={'ok' if brain else 'err'} opi={'ok' if opi else 'err'} pc={'ok' if pc else 'no'}")


def main():
    log.info(f"MQTT HA publisher started → {MQTT_HOST}:{MQTT_PORT} interval={INTERVAL}s")
    while True:
        try:
            publish_all()
        except Exception as e:
            log.warning(f"Publish error: {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
# PC stats via SSH

