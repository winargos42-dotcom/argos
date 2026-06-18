#!/bin/bash
# Orange Pi Full Deploy — Zigbee + ESPs + UART
# Run on Orange Pi as root

set -euo pipefail

NODE="orangepi"
LOG="/var/log/argos_orangepi_deploy.log"
Z2M_DIR="/opt/zigbee2mqtt"
ESPHOME_DIR="/root/esphome"

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "$(timestamp) $*" | tee -a "$LOG"; }

mkdir -p "$Z2M_DIR" "$ESPHOME_DIR"

# ============== DETECT USB ==============
log "=== USB Detection ==="
ZIGBEE_PORT=""
ESP_PORTS=()
for dev in /dev/ttyUSB* /dev/ttyACM*; do
    [ -e "$dev" ] || continue
    log "Found: $dev"
    UDEV=$(udevadm info -q property -n "$dev" 2>/dev/null || true)
    if echo "$UDEV" | grep -qiE 'cc253|cc265|silabs|conbee|zb|slzb'; then
        ZIGBEE_PORT="$dev"
        log "  -> ZIGBEE: $dev"
    elif echo "$UDEV" | grep -qiE 'ch340|cp210|ftdi'; then
        ESP_PORTS+=("$dev")
        log "  -> ESP/USB: $dev"
    fi
done

# ============== ZIGBEE2MQTT ==============
if [ -n "$ZIGBEE_PORT" ]; then
    log "=== Zigbee2MQTT Setup ==="
    mkdir -p "$Z2M_DIR/data"
    
    cat > "$Z2M_DIR/data/configuration.yaml" <<Z2MCFG
homeassistant: true
permit_join: false
mqtt:
  base_topic: zigbee2mqtt
  server: mqtt://192.168.1.53:1883
  user: argos
  password: argos_mqtt_pass
serial:
  port: $ZIGBEE_PORT
  adapter: zstack
frontend:
  port: 8099
  host: 0.0.0.0
advanced:
  log_level: info
  pan_id: 6754
  channel: 11
  network_key: GENERATE
Z2MCFG
    
    touch "$Z2M_DIR/data/devices.yaml" "$Z2M_DIR/data/groups.yaml"
    
    # Fix debounce ESM issue (already done, but ensure)
    if [ -d "$Z2M_DIR/node_modules" ]; then
        DEBOUNCE_DIR=$(find "$Z2M_DIR/node_modules" -name "debounce" -type d | head -1)
        if [ -n "$DEBOUNCE_DIR" ] && [ -f "$DEBOUNCE_DIR/index.js" ]; then
            if grep -q "export default" "$DEBOUNCE_DIR/index.js" 2>/dev/null; then
                log "Fixing debounce ESM->CJS..."
                cat > "$DEBOUNCE_DIR/index.js" <<'EOF'
module.exports = function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};
EOF
            fi
        fi
    fi
    
    log "Z2M config at $Z2M_DIR/data/configuration.yaml"
    log "Start with: cd $Z2M_DIR && npm start"
else
    log "WARNING: No Zigbee coordinator detected"
fi

# ============== ESPHOME ==============
log "=== ESPHome Setup ==="
mkdir -p "$ESPHOME_DIR"

# ESP8266 config (USB sensor node)
cat > "$ESPHOME_DIR/esp-usb-sensor.yaml" <<'EOF'
esphome:
  name: argos-esp-usb-sensor
  friendly_name: ARGOS USB Sensor

esp8266:
  board: d1_mini

wifi:
  ssid: "SiG"
  password: "argos_wifi_pass"
  ap:
    ssid: "ARGOS-USB-Fallback"
    password: "argos12345"

captive_portal:

api:
  encryption:
    key: "REPLACE_WITH_GENERATED_KEY"

mqtt:
  broker: 192.168.1.53
  username: argos
  password: argos_mqtt_pass
  topic_prefix: argos/esp/usb-sensor

i2c:
  sda: GPIO4
  scl: GPIO5
  scan: true

sensor:
  - platform: dht
    pin: GPIO14
    temperature:
      name: "USB Sensor Temperature"
    humidity:
      name: "USB Sensor Humidity"
    update_interval: 60s
  - platform: wifi_signal
    name: "USB Sensor WiFi Signal"
    update_interval: 60s

status_led:
  pin: GPIO2
EOF

# ESP32 config (actuator node)
cat > "$ESPHOME_DIR/esp32-usb-actuator.yaml" <<'EOF'
esphome:
  name: argos-esp32-usb-actuator
  friendly_name: ARGOS USB Actuator

esp32:
  board: esp32dev
  framework:
    type: arduino

wifi:
  ssid: "SiG"
  password: "argos_wifi_pass"
  ap:
    ssid: "ARGOS-ACTUATOR-Fallback"
    password: "argos12345"

captive_portal:

api:
  encryption:
    key: "REPLACE_WITH_GENERATED_KEY"

mqtt:
  broker: 192.168.1.53
  username: argos
  password: argos_mqtt_pass
  topic_prefix: argos/esp/usb-actuator

switch:
  - platform: gpio
    pin: GPIO25
    name: "USB Actuator Relay 1"
  - platform: gpio
    pin: GPIO26
    name: "USB Actuator Relay 2"

sensor:
  - platform: adc
    pin: GPIO34
    name: "USB Actuator ADC"
    update_interval: 5s
    attenuation: auto

status_led:
  pin:
    number: GPIO2
    inverted: true
EOF

# Generate secrets
cat > "$ESPHOME_DIR/secrets.yaml" <<'EOF'
wifi_ssid: "SiG"
wifi_password: "your-wifi-password"
EOF

log "ESPHome configs: $ESPHOME_DIR/"

# ============== UART FIX ==============
if [ -f /boot/armbianEnv.txt ]; then
    if ! grep -q "uart" /boot/armbianEnv.txt; then
        log "Enabling UART overlays..."
        sed -i 's/^overlays=/overlays=uart1 uart2 uart3 /' /boot/armbianEnv.txt 2>/dev/null || true
        log "REBOOT REQUIRED for UART activation"
    fi
fi

# ============== DONE ==============
log ""
log "======================================"
log "ORANGE PI DEPLOY COMPLETE"
log "Zigbee:   ${ZIGBEE_PORT:-NOT FOUND}"
log "ESP USBs: ${#ESP_PORTS[@]} device(s)"
log "Z2M:      $Z2M_DIR/data/configuration.yaml"
log "ESPHome:  $ESPHOME_DIR/"
log "======================================"
