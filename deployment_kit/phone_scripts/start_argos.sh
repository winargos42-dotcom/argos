#!/data/data/com.termux/files/usr/bin/bash
# ARGOS Daemon Start Script v4.0
# Launches all background services and bridges

export PATH="/data/data/com.termux/files/usr/bin:$PATH"
export HOME="/data/data/com.termux/files/home"
ARGOS_HOME="$HOME/argos-mobile"
LOG="$ARGOS_HOME/logs"
mkdir -p "$LOG"

echo "[ARGOS v4.0] Starting services..."

# OTG permissions fix
bash "$ARGOS_HOME/scripts/otg_setup.sh" 2>/dev/null || true

# USB hub monitor (auto-detect + launch)
nohup python3 "$ARGOS_HOME/scripts/usb_hub.py" --auto > "$LOG/usb_hub.log" 2>&1 &
echo "[OK] USB hub PID: $!"

# ARGOS network bridge (MQTT + commands)
export ARGOS_BRAIN_HOST="${ARGOS_BRAIN_HOST:-192.168.1.53}"
nohup python3 "$ARGOS_HOME/scripts/argos_bridge.py" > "$LOG/argos_bridge.log" 2>&1 &
echo "[OK] Bridge PID: $!"

# OBD bridge (if ELM327 present)
nohup python3 "$ARGOS_HOME/scripts/obd_bridge.py" > "$LOG/obd_bridge.log" 2>&1 &
echo "[OK] OBD PID: $!"

# KolibriOS QEMU (optional)
# nohup qemu-system-i386 -fda ~/argos-kolibri/images/kolibri.img -display none > "$LOG/kolibri.log" 2>&1 &

echo "[ARGOS v4.0] All services started. Logs: $LOG"
