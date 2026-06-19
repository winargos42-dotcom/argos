#!/data/data/com.termux/files/usr/bin/bash
# ARGOS Daemon Stop Script v4.0

pkill -f "usb_hub.py" 2>/dev/null
pkill -f "usb_scan.py" 2>/dev/null
pkill -f "argos_bridge.py" 2>/dev/null
pkill -f "obd_bridge.py" 2>/dev/null
pkill -f "uart_bridge.py" 2>/dev/null
pkill -f "can_sniff.py" 2>/dev/null
pkill -f "ble_scan.py" 2>/dev/null
pkill -f "qemu-system-i386" 2>/dev/null
pkill -f "argos_mobile_dashboard.py" 2>/dev/null

echo "[ARGOS v4.0] All services stopped."
