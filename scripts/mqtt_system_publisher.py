#!/usr/bin/env python3
"""Publish system metrics to MQTT for HA ARGOS integration."""
import os, time, json, subprocess, logging
import paho.mqtt.publish as publish

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("mqtt-pub")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
INTERVAL = int(os.getenv("PUBLISH_INTERVAL", "30"))
NODE = os.getenv("ARGOS_NODE", "laptop")

def get_cpu_temp():
    try:
        out = subprocess.check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"]).decode().strip()
        return round(int(out) / 1000, 1)
    except Exception:
        return None

def get_ram_percent():
    try:
        out = subprocess.check_output(["free", "-m"]).decode().splitlines()
        mem = [l for l in out if l.startswith("Mem:")][0].split()
        total, used = int(mem[1]), int(mem[2])
        return round(used / total * 100, 1)
    except Exception:
        return None

def get_disk_percent():
    try:
        out = subprocess.check_output(["df", "-h", "/"]).decode().splitlines()[1].split()
        return int(out[4].replace("%", ""))
    except Exception:
        return None

def publish_metrics():
    msgs = []
    temp = get_cpu_temp()
    ram = get_ram_percent()
    disk = get_disk_percent()
    if temp is not None:
        msgs.append((f"argos/{NODE}/cpu_temp", temp))
    if ram is not None:
        msgs.append((f"argos/{NODE}/ram_used", ram))
    if disk is not None:
        msgs.append((f"argos/{NODE}/disk_used", disk))
    msgs.append((f"argos/{NODE}/status", "online"))
    try:
        for topic, payload in msgs:
            publish.single(topic, payload, hostname=MQTT_HOST, port=MQTT_PORT, retain=True)
        log.info(f"Published {len(msgs)} metrics for {NODE}")
    except Exception as e:
        log.warning(f"Publish failed: {e}")

def main():
    log.info(f"MQTT publisher started → {MQTT_HOST}:{MQTT_PORT} interval={INTERVAL}s node={NODE}")
    while True:
        publish_metrics()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
