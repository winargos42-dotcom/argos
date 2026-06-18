#!/usr/bin/env python3
"""ARGOS ESP Display Manager
Sends system status to ESP32 OLED display (192.168.1.211) 
and ESP8266 ESPHome bridge (192.168.1.181) via MQTT/HTTP

ESP32 Display API (MicroPython SSD1306 + WS2812B):
  - ?text=<msg>     → Display text on OLED
  - ?msg=<msg>       → Scrolling message
  - ?led=<on/off/N>  → LED control
  - ?brightness=<0-255>
  - ?color=<hex>     → LED color
  - ?clear=1         → Clear display
  - ?scroll=<dir>    → Scroll text

ESP8266 ESPHome (192.168.1.181):
  - MQTT: argos-esp-bridge/# topics
  - Sensors: WiFi Signal, Uptime, ADC, IP, SSID
"""

import urllib.request
import urllib.error
import json
import time
import logging
import os
from datetime import datetime

LOG_FILE = '/home/ava/Projects/argoss/logs/esp_display.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a")
    ]
)
logger = logging.getLogger('argos.esp_display')

# Configuration
ESP32_DISPLAY_IP = "192.168.1.211"
ESP8266_MQTT_PREFIX = "argos-esp-bridge"
BRAIN_API = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
DISPLAY_INTERVAL = 30  # seconds between display updates


class ESPDisplayManager:
    def __init__(self):
        self.esp32_url = f"http://{ESP32_DISPLAY_IP}"
        self.last_display = ""
        self.esp32_online = False
        
    def send_to_esp32(self, params: dict) -> bool:
        """Send command to ESP32 display via HTTP GET params"""
        try:
            query = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{self.esp32_url}/?{query}"
            logger.debug(f"ESP32 GET: {url}")
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = resp.read().decode().strip()
                if result == "OK":
                    if not self.esp32_online:
                        logger.info("ESP32 display connected!")
                        self.esp32_online = True
                    return True
                return False
        except urllib.error.URLError as e:
            if self.esp32_online:
                logger.warning(f"ESP32 display went offline: {e}")
                self.esp32_online = False
        except Exception as e:
            logger.debug(f"ESP32 display error: {e}")
        return False
    
    def display_text(self, text: str) -> bool:
        """Display text on ESP32 OLED"""
        return self.send_to_esp32({"text": text})
    
    def display_message(self, msg: str) -> bool:
        """Show scrolling message on ESP32"""
        return self.send_to_esp32({"msg": msg})
    
    def set_led_color(self, color: str) -> bool:
        """Set WS2812B LED color (hex without #)"""
        return self.send_to_esp32({"color": color})
    
    def set_brightness(self, level: int) -> bool:
        """Set LED brightness 0-255"""
        return self.send_to_esp32({"brightness": str(level)})
    
    def led_on(self) -> bool:
        return self.send_to_esp32({"led": "on"})
    
    def led_off(self) -> bool:
        return self.send_to_esp32({"led": "off"})
    
    def clear_display(self) -> bool:
        return self.send_to_esp32({"clear": "1"})
    
    def get_system_status(self) -> dict:
        """Gather system status for display"""
        status = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "nodes": {},
            "cpu": "?",
            "ram": "?",
            "temp": "?",
        }
        
        # Get P2P nodes from Brain API
        try:
            req = urllib.request.Request(f"{BRAIN_API}/brain/nodes")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
                nodes = data if isinstance(data, list) else data.get("nodes", [])
                for node in nodes:
                    nid = node.get("node_id", "?")
                    st = node.get("status", "?")
                    status["nodes"][nid] = st
        except Exception:
            pass
        
        # Get system metrics
        try:
            # CPU usage
            with open("/proc/loadavg") as f:
                status["cpu"] = f.read().split()[0]
        except Exception:
            pass
        
        try:
            # RAM usage
            with open("/proc/meminfo") as f:
                lines = f.readlines()
                total = int(lines[0].split()[1])
                available = int(lines[2].split()[1])
                used_pct = int((1 - available / total) * 100)
                status["ram"] = f"{used_pct}%"
        except Exception:
            pass
        
        try:
            # Temperature
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                status["temp"] = f"{int(f.read().strip()) // 1000}C"
        except Exception:
            pass
        
        return status
    
    def format_status_display(self, status: dict) -> str:
        """Format system status for OLED display (limited chars)"""
        nodes_online = sum(1 for s in status["nodes"].values() if s == "online")
        total_nodes = len(status["nodes"])
        return f"ARGOS {status['time']} CPU:{status['cpu']} RAM:{status['ram']} {status['temp']} N:{nodes_online}/{total_nodes}"
    
    def get_status_color(self, status: dict) -> str:
        """Get LED color based on system status"""
        # Green if all nodes online, yellow if some, red if none
        online = sum(1 for s in status["nodes"].values() if s == "online")
        total = len(status["nodes"])
        if total == 0:
            return "0000FF"  # Blue = no data
        if online == total:
            return "00FF00"  # Green = all online
        if online > 0:
            return "FFFF00"  # Yellow = partial
        return "FF0000"  # Red = all offline
    
    def update_display(self):
        """Update ESP32 display with current system status"""
        status = self.get_system_status()
        
        # Display text on OLED
        display_text = self.format_status_display(status)
        if display_text != self.last_display:
            self.display_text(display_text[:128])
            self.last_display = display_text
        
        # Set LED color based on status
        color = self.get_status_color(status)
        self.set_led_color(color)
        
        # Scrolling message with node details
        nodes_str = " ".join(
            f"{n.replace('argos-','').replace('orangepi-','op-')[:8]}:{s}"
            for n, s in status["nodes"].items()
        )
        self.display_message(nodes_str[:200])
        
        logger.info(f"Display updated: online={sum(1 for s in status['nodes'].values() if s=='online')}/{len(status['nodes'])} color={color}")
    
    def run_display_loop(self):
        """Main display update loop"""
        logger.info("ESP Display Manager started")
        while True:
            try:
                self.update_display()
            except Exception as e:
                logger.error(f"Display update error: {e}")
            time.sleep(DISPLAY_INTERVAL)


def main():
    manager = ESPDisplayManager()
    
    # Initial test
    logger.info("Testing ESP32 display connection...")
    if manager.display_text("ARGOS STARTING"):
        logger.info("ESP32 display OK!")
    else:
        logger.warning("ESP32 display not responding (will retry in loop)")
    
    # Set initial LED to blue (starting)
    manager.set_led_color("0000FF")
    manager.set_brightness(50)
    
    # Set initial LED to blue (starting)
    manager.set_led_color("0000FF")
    manager.set_brightness(50)
    
    # Start display loop
    manager.run_display_loop()


if __name__ == "__main__":
    main()
