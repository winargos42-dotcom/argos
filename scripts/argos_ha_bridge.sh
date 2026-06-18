#!/bin/bash
# ARGOS HA Bridge - collects sensor data from all machines, publishes to MQTT
MQTT="127.0.0.1"
PORT=1883

# ── Laptop X230 ──
L_CPU=$(cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -1 | awk '{printf "%.1f",$1/1000}')
L_RAM_TOTAL=$(free | grep Mem | awk '{print $2}')
L_RAM_USED=$(free | grep Mem | awk '{print $3}')
L_RAM_PCT=$((L_RAM_USED * 100 / L_RAM_TOTAL))
L_DISK=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

mosquitto_pub -h $MQTT -p $PORT -t "argos/laptop/cpu_temp" -m "$L_CPU"
mosquitto_pub -h $MQTT -p $PORT -t "argos/laptop/ram_used" -m "$L_RAM_PCT"
mosquitto_pub -h $MQTT -p $PORT -t "argos/laptop/disk_used" -m "$L_DISK"
mosquitto_pub -h $MQTT -p $PORT -t "argos/laptop/status" -m "online"

# ── PC via SSH ──
PC_DATA=$(ssh -i /home/ava/.ssh/id_ed25519 -o ConnectTimeout=5 -o StrictHostKeyChecking=no AvA@192.168.1.66 "wsl bash -c 'echo CPU=\$(cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -1); echo RAM_TOTAL=\$(free | grep Mem | awk \"{print \\\$2}\"); echo RAM_USED=\$(free | grep Mem | awk \"{print \\\$3}\"); echo GPU_VRAM=\$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null || echo 0)'" 2>/dev/null)

PC_CPU=$(echo "$PC_DATA" | grep "^CPU=" | cut -d= -f2 | awk '{printf "%.1f",$1/1000}')
PC_RAM_TOTAL=$(echo "$PC_DATA" | grep "^RAM_TOTAL=" | cut -d= -f2)
PC_RAM_USED=$(echo "$PC_DATA" | grep "^RAM_USED=" | cut -d= -f2)
PC_GPU_VRAM=$(echo "$PC_DATA" | grep "^GPU_VRAM=" | cut -d= -f2)
if [ -n "$PC_RAM_TOTAL" ] && [ "$PC_RAM_TOTAL" -gt 0 ] 2>/dev/null; then
    PC_RAM_PCT=$((PC_RAM_USED * 100 / PC_RAM_TOTAL))
else
    PC_RAM_PCT=0
fi

[ -n "$PC_CPU" ] && mosquitto_pub -h $MQTT -p $PORT -t "argos/pc/cpu_temp" -m "$PC_CPU"
[ -n "$PC_RAM_PCT" ] && [ "$PC_RAM_PCT" -gt 0 ] && mosquitto_pub -h $MQTT -p $PORT -t "argos/pc/ram_used" -m "$PC_RAM_PCT"
[ -n "$PC_GPU_VRAM" ] && mosquitto_pub -h $MQTT -p $PORT -t "argos/pc/gpu_vram" -m "$PC_GPU_VRAM"
mosquitto_pub -h $MQTT -p $PORT -t "argos/pc/status" -m "online"

# ── Orange Pi via SSH ──
OPI_DATA=$(ssh -i /home/ava/.ssh/id_ed25519 -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@192.168.2.168 "echo CPU=\$(cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -1); echo RAM_TOTAL=\$(free | grep Mem | awk \"{print \\\$2}\"); echo RAM_USED=\$(free | grep Mem | awk \"{print \\\$3}\")" 2>/dev/null)

OPI_CPU=$(echo "$OPI_DATA" | grep "^CPU=" | cut -d= -f2 | awk '{printf "%.1f",$1/1000}')
OPI_RAM_TOTAL=$(echo "$OPI_DATA" | grep "^RAM_TOTAL=" | cut -d= -f2)
OPI_RAM_USED=$(echo "$OPI_DATA" | grep "^RAM_USED=" | cut -d= -f2)
if [ -n "$OPI_RAM_TOTAL" ] && [ "$OPI_RAM_TOTAL" -gt 0 ] 2>/dev/null; then
    OPI_RAM_PCT=$((OPI_RAM_USED * 100 / OPI_RAM_TOTAL))
else
    OPI_RAM_PCT=0
fi

[ -n "$OPI_CPU" ] && mosquitto_pub -h $MQTT -p $PORT -t "argos/opi/cpu_temp" -m "$OPI_CPU"
[ -n "$OPI_RAM_PCT" ] && [ "$OPI_RAM_PCT" -gt 0 ] && mosquitto_pub -h $MQTT -p $PORT -t "argos/opi/ram_used" -m "$OPI_RAM_PCT"
mosquitto_pub -h $MQTT -p $PORT -t "argos/opi/status" -m "online"

# ── Phone via ADB ──
PHONE="192.168.1.149:5555"
PH_CPU=$(adb -s $PHONE shell "cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null | head -1" | tr -d '\r' | awk '{printf "%.1f",$1/1000}')
PH_MEM_TOTAL=$(adb -s $PHONE shell "cat /proc/meminfo | grep MemTotal" | tr -d '\r' | awk '{print $2}')
PH_MEM_AVAIL=$(adb -s $PHONE shell "cat /proc/meminfo | grep MemAvailable" | tr -d '\r' | awk '{print $2}')
PH_STORAGE=$(adb -s $PHONE shell "df /data | tail -1" | tr -d '\r' | awk '{print $5}' | tr -d '%')

if [ -n "$PH_MEM_TOTAL" ] && [ "$PH_MEM_TOTAL" -gt 0 ] 2>/dev/null; then
    PH_MEM_PCT=$((100 - (PH_MEM_AVAIL * 100 / PH_MEM_TOTAL)))
else
    PH_MEM_PCT=0
fi

[ -n "$PH_CPU" ] && mosquitto_pub -h $MQTT -p $PORT -t "argos/phone/redmi_note_8t/cpu_temp" -m "$PH_CPU"
mosquitto_pub -h $MQTT -p $PORT -t "argos/phone/redmi_note_8t/mem_used" -m "$PH_MEM_PCT"
[ -n "$PH_STORAGE" ] && mosquitto_pub -h $MQTT -p $PORT -t "argos/phone/redmi_note_8t/storage_used" -m "$PH_STORAGE"

# ── Brain ──
BRAIN_NODES=$(curl -s http://192.168.1.66:5010/brain/nodes 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('nodes',[])))" 2>/dev/null || echo 0)
mosquitto_pub -h $MQTT -p $PORT -t "argos/brain/nodes_online" -m "$BRAIN_NODES"
mosquitto_pub -h $MQTT -p $PORT -t "argos/brain/status" -m "online"

echo "$(date) | Laptop: ${L_CPU}°C RAM ${L_RAM_PCT}% Disk ${L_DISK}% | PC: ${PC_CPU}°C RAM ${PC_RAM_PCT}% GPU ${PC_GPU_VRAM}MB | OPi: ${OPI_CPU}°C RAM ${OPI_RAM_PCT}% | Phone: ${PH_CPU}°C RAM ${PH_MEM_PCT}% Disk ${PH_STORAGE}% | Brain: ${BRAIN_NODES} nodes"
