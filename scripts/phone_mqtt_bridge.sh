#!/bin/bash
# ARGOS Phone MQTT Bridge - reads phone sensors via ADB, publishes to MQTT
PHONE="192.168.1.149:5555"
MQTT="127.0.0.1"
MQTT_PORT=1883
DEVICE="redmi_note_8t"

while true; do
    # CPU Temp
    CPU_TEMP=$(adb -s $PHONE shell "cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -1" | tr -d '\r' | awk '{printf "%.1f", $1/1000}')
    
    # Memory
    MEM_TOTAL=$(adb -s $PHONE shell "cat /proc/meminfo | grep MemTotal" | tr -d '\r' | awk '{print $2}')
    MEM_AVAIL=$(adb -s $PHONE shell "cat /proc/meminfo | grep MemAvailable" | tr -d '\r' | awk '{print $2}')
    if [ -n "$MEM_TOTAL" ] && [ -n "$MEM_AVAIL" ] && [ "$MEM_TOTAL" -gt 0 ]; then
        MEM_USED=$((100 - (MEM_AVAIL * 100 / MEM_TOTAL)))
    else
        MEM_USED=0
    fi
    
    # Storage
    STORAGE=$(adb -s $PHONE shell "df /data 2>/dev/null | tail -1" | tr -d '\r' | awk '{print $5}' | tr -d '%')
    
    # Publish
    [ -n "$CPU_TEMP" ] && mosquitto_pub -h $MQTT -p $MQTT_PORT -t "argos/phone/$DEVICE/cpu_temp" -m "$CPU_TEMP"
    mosquitto_pub -h $MQTT -p $MQTT_PORT -t "argos/phone/$DEVICE/mem_used" -m "$MEM_USED"
    [ -n "$STORAGE" ] && mosquitto_pub -h $MQTT -p $MQTT_PORT -t "argos/phone/$DEVICE/storage_used" -m "$STORAGE"
    
    sleep 60
done
