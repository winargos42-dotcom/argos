#!/bin/bash
# Orange Pi auto-detect USB devices and start services
# To be installed as systemd service or run via cron every minute

LOG="/var/log/argos_usb_autostart.log"
Z2M_DIR="/opt/zigbee2mqtt"
Z2M_PID=""

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "$(timestamp) $*" | tee -a "$LOG"; }

# Detect zigbee dongle
detect_zigbee() {
    for dev in /dev/ttyUSB* /dev/ttyACM*; do
        [ -e "$dev" ] || continue
        # Check udev for known zigbee IDs
        local udev=$(udevadm info -q property -n "$dev" 2>/dev/null || true)
        if echo "$udev" | grep -qiE 'cc253|cc265|silabs|conbee|sonoff.*zb|slzb|dresden|telink'; then
            echo "$dev"
            return 0
        fi
    done
    # Fallback: check by USB ids from sysfs
    for devpath in /sys/bus/usb/devices/*-*; do
        [ -d "$devpath" ] || continue
        local vid=$(cat "$devpath/idVendor" 2>/dev/null || true)
        local pid=$(cat "$devpath/idProduct" 2>/dev/null || true)
        case "${vid}:${pid}" in
            "10c4:ea60"|"1a86:7523"|"1cf1:0030"|"0451:*"|"1915:*")
                echo "auto"
                return 0
                ;;
        esac
    done
    return 1
}

# Start zigbee2mqtt
start_z2m() {
    local port="$1"
    log "Starting Z2M on $port..."
    if [ -f "$Z2M_DIR/data/configuration.yaml" ]; then
        # Update port in config
        sed -i "s/port: .*/port: $port/" "$Z2M_DIR/data/configuration.yaml"
    fi
    if pgrep -f "zigbee2mqtt" >/dev/null; then
        log "Z2M already running"
    else
        cd "$Z2M_DIR"
        nohup npm start >> /var/log/zigbee2mqtt.log 2>&1 &
        log "Z2M started"
    fi
}

# Detect ESPs
detect_esps() {
    local esp_count=0
    for dev in /dev/ttyUSB*; do
        [ -e "$dev" ] || continue
        esp_count=$((esp_count+1))
    done
    echo "$esp_count"
}

# Main
log "--- USB scan ---"
ZIGBEE=$(detect_zigbee)
ESPS=$(detect_esps)

if [ -n "$ZIGBEE" ]; then
    log "Zigbee detected on $ZIGBEE"
    start_z2m "$ZIGBEE"
else
    log "Zigbee: not detected"
fi

log "ESP serial ports: $ESPS"

# Auto-flash ESPs if configs exist and esphome available
if command -v esphome >/dev/null 2>&1; then
    ESPHOME_DIR="/root/esphome"
    PORT_IDX=0
    for dev in /dev/ttyUSB*; do
        [ -e "$dev" ] || continue
        PORT_IDX=$((PORT_IDX+1))
        # Skip if already flashed ESPHome (check if api responds)
        log "ESP port $dev ready for flashing"
    done
fi

log "--- done ---"
