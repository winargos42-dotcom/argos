#!/usr/bin/env python3
"""Runner для recovered демонов ARGOS"""
import sys, os, time, re, logging
sys.path.insert(0, os.path.expanduser("~/Projects/argoss/src"))

from integrations.anomaly_detector import AnomalyDetector
from integrations.argos_emergence_daemon import EmergenceDaemon

def genv(k):
    env = open(os.path.expanduser("~/Projects/argoss/.env")).read()
    m = re.search(rf"{k}=([^\n\s]+)", env)
    return m.group(1).strip().strip('"').strip("'") if m else ""

TOKEN = genv("TELEGRAM_BOT_TOKEN")
CHAT = genv("ENTITY_COUNCIL_GROUP_ID") or genv("ARGOS_TG_PERSONAL_ID")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

ad = AnomalyDetector(TOKEN, CHAT)
ed = EmergenceDaemon(TOKEN, CHAT)

print("[DAEMONS] Starting anomaly + emergence loops (Ctrl+C to stop)")
while True:
    try:
        r = ad.run_detection_cycle()
        if r.get("status") != "clean":
            print("[ANOMALY]", r)
        else:
            print("[ANOMALY] clean")
    except Exception as e:
        print("[ANOMALY ERROR]", e)

    try:
        ed.run_introspection_cycle()
        print("[EMERGENCE] sent")
    except Exception as e:
        print("[EMERGENCE ERROR]", e)

    time.sleep(300)  # 5 мин
