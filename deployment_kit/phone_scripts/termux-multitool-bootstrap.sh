#!/data/data/com.termux/files/usr/bin/bash
#===============================================================================
#  ARGOS Mobile Multi-Tool Bootstrap v4.0 — FULL PROTOCOL ARSENAL
#  Redmi Note 8T (willow) — LineageOS 21 + Magisk
#  Устанавливает софт для ВСЕХ протоколов и устройств
#===============================================================================
set -euo pipefail

ARGOS_MOBILE="$HOME/argos-mobile"
SCRIPTS="$ARGOS_MOBILE/scripts"
LOGS="$ARGOS_MOBILE/logs"
CAPTURES="$ARGOS_MOBILE/captures"
CAN_DUMPS="$ARGOS_MOBILE/can_dumps"
FIRMWARES="$ARGOS_MOBILE/firmwares"
USB_CAPTURES="$ARGOS_MOBILE/usb_captures"

echo -e "\e[36m[ARGOS Mobile Multi-Tool v4.0 — FULL ARSENAL]\e[0m"
echo "Target: willow/ginkgo | Magisk required for OTG full access"
echo "Protocols: USB-Serial, CAN, OBD-II, BLE, WiFi, JTAG/SWD, SPI/I2C"
echo ""

# ── 1. Обновление ────────────────────────────────────────────────────────────
echo "[1/10] Обновление пакетов..."
apt update -y
apt upgrade -y || true

# ── 2. Полный арсенал ───────────────────────────────────────────────────────
echo "[2/10] Установка пакетов..."
pkg install -y \
    tsu openssh git curl wget \
    nano vim python python-pip \
    nmap netcat-openbsd busybox procps htop \
    usbutils bluez \
    termux-api termux-exec \
    iproute2 can-utils || warn "can-utils not in repo" \
    clang make cmake ninja rust \
    libusb libftdi1 libserialport || true \
    aircrack-ng || true \
    mosquitto || true

# ── 3. Python стек ─────────────────────────────────────────────────────────
echo "[3/10] Python библиотеки..."
pip install --upgrade pip
pip install --upgrade \
    pyserial pyusb pyftdi \
    requests websocket-client \
    paho-mqtt colorama rich prompt-toolkit \
    bleak bluepy 2>/dev/null || true

# ── 4. ARGOS директории ─────────────────────────────────────────────────────
echo "[4/10] Директории..."
mkdir -p "$ARGOS_MOBILE" "$SCRIPTS" "$LOGS" "$CAPTURES" "$CAN_DUMPS" "$FIRMWARES" "$USB_CAPTURES" "$HOME/.termux"

# ── 5. SSH ──────────────────────────────────────────────────────────────────
echo "[5/10] SSH сервер..."
sshd 2>/dev/null || true
WHOAMI=$(whoami)
echo "SSH :8022 | ssh -p 8022 ${WHOAMI}@<IP>"

# ── 6. Storage ──────────────────────────────────────────────────────────────
echo "[6/10] Storage..."
termux-setup-storage 2>/dev/null || true
ln -sf /sdcard/Download "$HOME/Download" 2>/dev/null || true

# ── 7. System wrappers ──────────────────────────────────────────────────────
echo "[7/10] System wrappers..."
mkdir -p "$ARGOS_MOBILE/bin"
for util in argos-status argos-usb-setup argos-can-up argos-bridge; do
    cat > "$ARGOS_MOBILE/bin/$util" << EOF
#!/data/data/com.termux/files/usr/bin/sh
exec su -c "/system/xbin/$util \"\$@\""
EOF
    chmod +x "$ARGOS_MOBILE/bin/$util"
done

# ── 8. Скрипты мультитула — ВСЕ ПРОТОКОЛЫ ──────────────────────────────────
echo "[8/10] Создание скриптов..."

# ====== USB SCANNER (все VID:PID из арсенала) ======
cat > "$SCRIPTS/usb_scan.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
import subprocess, sys, re, json, os, time

ARSENAL = {
    "0403:b470": "FTDI OBD-II ELM327",
    "0403:6001": "FT232 USB-UART",
    "1a86:7523": "CH340 USB-UART",
    "1a86:5523": "CH341A SPI/I2C/EEPROM Programmer",
    "0483:5740": "ST-Link V2 (SWD/JTAG)",
    "1366:0105": "J-Link V9 (SWD/JTAG)",
    "2e8a:000c": "Raspberry Pi Pico (RP2040 CDC)",
    "2e8a:000a": "Raspberry Pi Pico (Bootloader)",
    "1234:abcd": "XGecu T48/T56 (ISP)",
    "1234:ef01": "FNIRSI 2C23T (Scope)",
    "1234:ef02": "FNIRSI FZ-53 (Multimeter)",
    "16c0:05dc": "Flipper Zero (USB CDC)",
    "04d8:fa2e": "Scanmatik SM-2 PRO",
}

def scan_usb():
    print("═"*70)
    print("  ARGOS USB Arsenal Scanner — Full Device Detection")
    print("═"*70)
    try:
        out = subprocess.check_output(['su', '-c', 'lsusb'], text=True, stderr=subprocess.DEVNULL)
        root_mode = True
    except:
        try:
            out = subprocess.check_output(['lsusb'], text=True, stderr=subprocess.DEVNULL)
            root_mode = False
        except Exception as e:
            print(f"[ERR] lsusb failed: {e}")
            return []
    
    devices = []
    for line in out.strip().split('\n'):
        m = re.match(r'Bus (\d+) Device (\d+): ID ([0-9a-f]{4}):([0-9a-f]{4}) (.*)', line)
        if m:
            bus, dev, vid, pid, name = m.groups()
            key = f"{vid}:{pid}"
            known = ARSENAL.get(key, None)
            marker = " 🎯" if known else ""
            print(f"  [{vid}:{pid}] {name.strip()}{marker}")
            if known:
                print(f"      → {known}")
            devices.append({"bus": bus, "dev": dev, "vid": vid, "pid": pid, "name": name.strip(), "known": known})
    
    if not devices:
        print("[INFO] Нет USB устройств. Подключите OTG адаптер.")
    else:
        print(f"\n[OK] Найдено {len(devices)} устройств (root={root_mode})")
        known_cnt = len([d for d in devices if d["known"]])
        if known_cnt:
            print(f"[OK] Распознано из арсенала: {known_cnt}")
    
    os.makedirs(os.path.expanduser("~/argos-mobile/logs"), exist_ok=True)
    with open(os.path.expanduser("~/argos-mobile/logs/usb_scan.json"), "w") as f:
        json.dump(devices, f, indent=2, ensure_ascii=False)
    return devices

if __name__ == '__main__':
    scan_usb()
PYEOF
chmod +x "$SCRIPTS/usb_scan.py"

# ====== OBD-II (ELM327 / FTDI) — LIVE STREAM ======
cat > "$SCRIPTS/obd_bridge.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""OBD-II Bridge — ELM327 / FTDI / CH340 OBD adapters — LIVE STREAM"""
import sys, serial, time, subprocess, re, json, os, signal, threading

LOG_DIR = os.path.expanduser("~/argos-mobile/logs")
CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD = 38400

PIDS = {
    "010C": {"name": "RPM",          "unit": "rpm",   "fmt": lambda v: int(v.replace(" ",""),16) // 4},
    "010D": {"name": "Speed",        "unit": "km/h",  "fmt": lambda v: int(v.replace(" ",""),16)},
    "0105": {"name": "Coolant",      "unit": "°C",    "fmt": lambda v: int(v.replace(" ",""),16) - 40},
    "015C": {"name": "Oil Temp",     "unit": "°C",    "fmt": lambda v: int(v.replace(" ",""),16) - 40},
    "0142": {"name": "Voltage",     "unit": "V",     "fmt": lambda v: int(v.replace(" ",""),16) / 1000},
    "012F": {"name": "Fuel Level",   "unit": "%",    "fmt": lambda v: int(v.replace(" ",""),16) * 100 // 255},
    "0110": {"name": "MAF",          "unit": "g/s",   "fmt": lambda v: int(v.replace(" ",""),16) / 100},
    "015E": {"name": "Fuel Rate",    "unit": "L/h",  "fmt": lambda v: int(v.replace(" ",""),16) * 0.05},
}

def find_obd_port():
    for method in [
        lambda: subprocess.check_output(['su','-c','ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null'],text=True,stderr=subprocess.DEVNULL).strip().split(),
        lambda: subprocess.check_output(['ls','/dev/ttyUSB*'],shell=True,text=True,stderr=subprocess.DEVNULL).strip().split(),
    ]:
        try:
            ports = method()
            for p in ports:
                if not p: continue
                try:
                    s = serial.Serial(p, 38400, timeout=1)
                    s.write(b"ATZ\r")
                    time.sleep(0.5)
                    resp = s.read(s.in_waiting or 1).decode('ascii', errors='ignore')
                    s.close()
                    if any(x in resp for x in ["ELM","OK","atz"]):
                        return p
                except: continue
            if ports:
                return ports[0]
        except: continue
    return None

def send_cmd(ser, cmd, timeout=0.2):
    ser.reset_input_buffer()
    ser.write(f"{cmd}\r".encode())
    time.sleep(timeout)
    raw = ser.read(ser.in_waiting or 256).decode('ascii', errors='ignore')
    # Extract hex value (last non-empty line before prompt)
    lines = [l.strip() for l in raw.split('\r') if l.strip() and l.strip() != '>']
    return lines[-1] if lines else ""

def init_elm(ser):
    cmds = [
        ("ATZ",    "Reset",       1.0),
        ("ATE0",   "Echo off",    0.2),
        ("ATL0",   "Linefeeds off",0.2),
        ("ATS0",   "Spaces off",  0.2),
        ("ATH1",   "Headers on",  0.2),
        ("ATSP0",  "Auto proto",  0.5),
    ]
    for cmd, desc, wait in cmds:
        ser.write(f"{cmd}\r".encode())
        time.sleep(wait)
        ser.read(ser.in_waiting or 64)
    # Check supported PIDs
    ser.write(b"0100\r")
    time.sleep(0.5)
    resp = ser.read(ser.in_waiting or 256).decode('ascii', errors='ignore')
    return "41 00" in resp or "4100" in resp.replace(" ","")

def read_pid(ser, pid):
    ser.reset_input_buffer()
    ser.write(f"{pid}\r".encode())
    time.sleep(0.15)
    raw = ser.read(ser.in_waiting or 256).decode('ascii', errors='ignore')
    for line in raw.split('\r'):
        line = line.strip().replace(" ","")
        if line.startswith("41") and len(line) >= 8:
            data = line[4:]  # Skip mode+pid response bytes
            return data
    return None

def live_stream(ser, pids=None, interval=0.5, log_file=None):
    if pids is None:
        pids = ["010C","010D","0105","012F"]
    
    print(f"\n[ LIVE OBD-II ] {len(pids)} PIDs, interval={interval}s")
    print("─" * 60)
    
    header = "  ".join(f"{PIDS[p]['name']:>10}" for p in pids if p in PIDS)
    units  = "  ".join(f"{PIDS[p]['unit']:>10}" for p in pids if p in PIDS)
    print(f"  {header}")
    print(f"  {units}")
    print("─" * 60)
    
    log_fh = None
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        log_fh = open(log_file, "w")
        log_fh.write("timestamp," + ",".join(PIDS[p]['name'] for p in pids if p in PIDS) + "\n")
    
    snapshot = {}
    try:
        while True:
            row = []
            for pid in pids:
                info = PIDS.get(pid)
                if not info: 
                    row.append("---")
                    continue
                data = read_pid(ser, pid)
                if data:
                    try:
                        val = info["fmt"](data)
                        row.append(f"{val:>10}")
                        snapshot[info["name"]] = val
                    except:
                        row.append(f"{'ERR':>10}")
                else:
                    row.append(f"{'---':>10}")
            
            line = "  ".join(row)
            ts = time.strftime("%H:%M:%S")
            print(f"\r  {line}  [{ts}]", end="", flush=True)
            
            if log_fh and snapshot:
                log_fh.write(f"{time.time()}" + ",".join(str(snapshot.get(PIDS[p]['name'],'')) for p in pids if p in PIDS) + "\n")
                log_fh.flush()
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n[OK] OBD stream остановлен")
    finally:
        if log_fh:
            log_fh.close()

def main():
    print("═" * 60)
    print("  ARGOS OBD-II Bridge v4.0 — Live Stream")
    print("═" * 60)
    
    port = find_obd_port()
    if not port:
        print("[ERR] OBD адаптер не найден. Подключите OTG + ELM327.")
        print("[HINT] su -c 'ls /dev/ttyUSB* /dev/ttyACM*'")
        sys.exit(1)
    
    baud = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BAUD
    print(f"[OK] Порт: {port} @ {baud}")
    
    try:
        ser = serial.Serial(port, baud, timeout=2)
        if not init_elm(ser):
            print("[WARN] ELM init неполный, пробуем дальше...")
        else:
            print("[OK] ELM327 инициализирован")
        
        log_file = os.path.join(CAPTURE_DIR, f"obd_{int(time.time())}.csv")
        live_stream(ser, log_file=log_file)
        ser.close()
    except Exception as e:
        print(f"[ERR] {e}")

if __name__ == '__main__':
    main()
PYEOF
chmod +x "$SCRIPTS/obd_bridge.py"

# ====== UART TERMINAL — INTERACTIVE ======
cat > "$SCRIPTS/uart_bridge.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""USB-UART Terminal v4.0 — CH340/FT232/CP210x/PL2303"""
import serial, sys, time, os, select, threading, re, binascii

PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1',
         '/dev/ttyCH340USB0', '/dev/serial0']
BAUDS = [115200, 9600, 38400, 57600, 921600, 4800, 2400, 19200, 230400, 460800]
LOG_DIR = os.path.expanduser("~/argos-mobile/logs")

hex_mode = False
log_file = None

def find_port():
    # Try root first
    try:
        ports = os.popen("su -c 'ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null'").read().strip().split()
        for p in ports:
            if not p: continue
            try:
                s = serial.Serial(p, 115200, timeout=0.1)
                s.close()
                return p
            except: continue
    except: pass
    for p in PORTS:
        try:
            s = serial.Serial(p, 115200, timeout=0.1)
            s.close()
            return p
        except: continue
    return None

def auto_baud(port):
    """Пробуем стандартные скорости, ищем читаемые данные"""
    for baud in BAUDS:
        try:
            s = serial.Serial(port, baud, timeout=0.5)
            s.write(b"\r\n")
            time.sleep(0.3)
            data = s.read(s.in_waiting or 64)
            s.close()
            if data and any(0x20 <= b < 0x7f for b in data):
                return baud
        except: continue
    return 115200  # default

def reader_thread(ser, stop_event):
    """Читает данные из порта в фоне"""
    while not stop_event.is_set():
        try:
            n = ser.in_waiting
            if not n:
                time.sleep(0.01)
                continue
            data = ser.read(n)
            if not data:
                continue
            if hex_mode:
                hex_str = ' '.join(f'{b:02X}' for b in data)
                print(f"\r[RX] {hex_str}", end='', flush=True)
            else:
                sys.stdout.buffer.write(data)
                sys.stdout.flush()
            if log_file:
                log_file.write(data)
                log_file.flush()
        except: break

def interactive(port, baud):
    global hex_mode, log_file
    print(f"[UART] {port} @ {baud} | Ctrl+C выход")
    print("[CMD] \\h=hex \\a=ascii \\b=baud \\l=log \\r= RTS \\d=DTR \\q=quit")
    
    try:
        ser = serial.Serial(port, baud, timeout=0.05)
    except Exception as e:
        print(f"[ERR] {e}")
        return
    
    stop = threading.Event()
    t = threading.Thread(target=reader_thread, args=(ser, stop), daemon=True)
    t.start()
    
    try:
        while True:
            try:
                line = input()
                if line == '\\q':
                    break
                elif line == '\\h':
                    hex_mode = True
                    print("[MODE] Hex")
                elif line == '\\a':
                    hex_mode = False
                    print("[MODE] ASCII")
                elif line == '\\b':
                    try:
                        new_baud = int(input("Baud: "))
                        ser.baudrate = new_baud
                        print(f"[OK] Baud: {new_baud}")
                    except: pass
                elif line == '\\l':
                    fname = os.path.join(LOG_DIR, f"uart_{int(time.time())}.bin")
                    log_file = open(fname, "wb")
                    print(f"[LOG] {fname}")
                elif line == '\\r':
                    ser.rts = not ser.rts
                    print(f"[RTS] {ser.rts}")
                elif line == '\\d':
                    ser.dtr = not ser.dtr
                    print(f"[DTR] {ser.dtr}")
                elif line.startswith('\\x'):
                    # Send hex bytes
                    try:
                        raw = bytes.fromhex(line[2:].replace(' ',''))
                        ser.write(raw)
                    except: print("[ERR] Invalid hex")
                elif line:
                    ser.write(line.encode() + b'\n')
            except EOFError:
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        ser.close()
        if log_file:
            log_file.close()
        print("\n[OK] Закрыто")

def main():
    print("═"*60)
    print("  ARGOS UART Bridge v4.0")
    print("═"*60)
    port = sys.argv[1] if len(sys.argv) > 1 else find_port()
    if not port:
        print("[ERR] USB-UART не найден. su -c 'ls /dev/ttyUSB*'")
        sys.exit(1)
    baud = int(sys.argv[2]) if len(sys.argv) > 2 else None
    if baud is None:
        baud = auto_baud(port)
        print(f"[OK] Auto-baud: {baud}")
    interactive(port, baud)

if __name__ == '__main__':
    main()
PYEOF
chmod +x "$SCRIPTS/uart_bridge.py"

# ====== CAN SNIFFER ======
cat > "$SCRIPTS/can_sniff.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""CAN bus sniffer — requires root + can-utils + CAN adapter"""
import subprocess, sys, os, signal, time

IFACE = sys.argv[1] if len(sys.argv) > 1 else 'can0'
BITRATE = int(sys.argv[2]) if len(sys.argv) > 2 else 500000

def up():
    try:
        subprocess.run(['su', '-c', f'ip link set {IFACE} down'], check=False)
        subprocess.run(['su', '-c', f'ip link set {IFACE} type can bitrate {BITRATE}'], check=True)
        subprocess.run(['su', '-c', f'ip link set {IFACE} up'], check=True)
        return True
    except Exception as e:
        print(f"[ERR] CAN up failed: {e}")
        return False

def sniff():
    logfile = os.path.expanduser(f"~/argos-mobile/can_dumps/can_{IFACE}_{int(time.time())}.log")
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    print(f"[CAN] Sniffing {IFACE} @ {BITRATE} → {logfile}")
    print("Ctrl+C для остановки")
    f = open(logfile, "w")
    try:
        proc = subprocess.Popen(['su', '-c', f'candump {IFACE} -ta'], stdout=subprocess.PIPE, text=True)
        for line in proc.stdout:
            line = line.strip()
            print(line)
            f.write(line + "\n")
            f.flush()
    except KeyboardInterrupt:
        proc.send_signal(signal.SIGINT)
        print("\n[OK] Остановлено")
    finally:
        f.close()

if __name__ == '__main__':
    print("═"*70)
    print("  ARGOS CAN Sniffer")
    print("═"*70)
    if not up():
        print("[HINT] Проверьте USB-CAN адаптер (MCP2515/PCAN/Seeed)")
        sys.exit(1)
    sniff()
PYEOF
chmod +x "$SCRIPTS/can_sniff.py"

# ====== BLE SCANNER — ENHANCED ======
cat > "$SCRIPTS/ble_scan.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""BLE Scanner v4.0 — nRF/Flipper/HID/custom, rich output + logging"""
import asyncio, sys, os, json, time

try:
    from bleak import BleakScanner
except ImportError:
    print("[ERR] bleak не установлен. pip install bleak")
    sys.exit(1)

LOG_DIR = os.path.expanduser("~/argos-mobile/logs")

# Known BLE service UUIDs
BLE_SERVICES = {
    "1800": "Generic Access",
    "1801": "Generic Attribute",
    "180A": "Device Information",
    "180F": "Battery Service",
    "1812": "HID over GATT",
    "FE59": "Nordic DFU",
    "8EC90001": "Flipper Zero",
    "6E400001": "Nordic UART",
    "F000FFC0": "TI CC2652",
    "0000FFE0": "HM-10/11",
    "0000FFF0": "JDY-xx",
}

def service_name(uuid):
    uid = uuid.replace("-","").upper()
    for k, v in BLE_SERVICES.items():
        if uid.startswith(k) or uid.endswith(k):
            return v
    return None

async def scan(timeout=10, output_json=False):
    print("═"*60)
    print("  ARGOS BLE Scanner v4.0")
    print("═"*60)
    print(f"[INFO] Scanning {timeout}s...")
    
    devices = await BleakScanner.discover(timeout=timeout, return_adv=True)
    
    results = []
    for addr, (d, adv) in devices.items():
        name = d.name or "(Unknown)"
        rssi = adv.rssi if hasattr(adv, 'rssi') else (d.rssi or "?")
        
        # Service identification
        svc_names = []
        uuids = adv.service_uuids if hasattr(adv, 'service_uuids') else []
        for u in uuids:
            sn = service_name(str(u))
            svc_names.append(sn or str(u))
        
        entry = {
            "name": name,
            "address": d.address,
            "rssi": rssi,
            "services": svc_names,
            "time": time.strftime("%H:%M:%S")
        }
        results.append(entry)
        
        if not output_json:
            rssi_bar = "█" * max(0, (int(rssi) + 100) // 10) if isinstance(rssi, (int, float)) else 0
            print(f"  [{rssi:>3} dBm] {name}")
            print(f"       MAC: {d.address}")
            if svc_names:
                print(f"       SVC: {', '.join(svc_names)}")
    
    # Save results
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"ble_scan_{int(time.time())}.json")
    with open(log_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Найдено {len(results)} устройств | Log: {log_path}")
    
    if output_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    timeout = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
    json_out = "--json" in sys.argv
    try:
        asyncio.run(scan(timeout, json_out))
    except KeyboardInterrupt:
        print("\n[STOPPED]")
PYEOF
chmod +x "$SCRIPTS/ble_scan.py"

# ====== CH341A EEPROM/FLASH DUMPER — REAL PROTOCOL ======
cat > "$SCRIPTS/ch341a_dump.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""CH341A SPI EEPROM/Flash Dumper v4.0 — Real protocol"""
import usb.core, usb.util, sys, os, time, struct

CH341_VID = 0x1A86
CH341_PID = 0x5512  # CH341A in SPI mode

# CH341A SPI commands
CH341_CMD_SPI_DIRECT = 0x80
CH341_CMD_SPI_STREAM = 0x81
CH341_CMD_SPI_INIT   = 0xA3
CH341_CMD_CLR_PIPE   = 0xAB

# Common EEPROM sizes
CHIP_DB = {
    "W25Q32":  {"size": 4194304,  "page": 256},
    "W25Q64":  {"size": 8388608,  "page": 256},
    "W25Q128": {"size": 16777216, "page": 256},
    "MX25L3206":{"size": 4194304, "page": 256},
    "EN25QH32": {"size": 4194304, "page": 256},
    "GD25Q32": {"size": 4194304, "page": 256},
    "SST25VF016B":{"size": 2097152, "page": 256},
}

CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")

def find_ch341a():
    dev = usb.core.find(idVendor=CH341_VID, idProduct=CH341_PID)
    if dev is None:
        return None
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    dev.set_configuration()
    return dev

def spi_transaction(dev, w_data, r_len=0):
    """CH341A SPI transaction via control transfer"""
    # EP_OUT = 0x02, EP_IN = 0x82
    try:
        if w_data:
            dev.write(0x02, w_data, timeout=1000)
        if r_len > 0:
            return dev.read(0x82, r_len, timeout=1000)
    except usb.USBError as e:
        print(f"[USB ERR] {e}")
    return b""

def read_jedec_id(dev):
    """Read JEDEC ID: cmd 0x9F + 3 dummy bytes"""
    dev.write(0x02, b'\x9F\x00\x00\x00\x00')
    resp = dev.read(0x82, 5, timeout=1000)
    if len(resp) >= 5:
        mfr = resp[2]
        typ = resp[3]
        cap = resp[4]
        return mfr, typ, cap
    return None

def identify_chip(mfr, typ, cap):
    """Map JEDEC ID to chip name"""
    size = 1 << cap
    # Common MFR codes
    mfr_names = {0xEF: "Winbond", 0xC2: "Macronix", 0x1C: "EON",
                 0xC8: "GigaDevice", 0xBF: "SST", 0x20: "Micron",
                 0x1F: "Atmel", 0x9D: "ISSI"}
    name = mfr_names.get(mfr, f"MFR:0x{mfr:02X}")
    return f"{name} 0x{typ:02X}0x{cap:02X} ({size//1024}KB)"

def spi_read(dev, addr, length, page_size=256):
    """Read from SPI flash with 03h read command"""
    data = bytearray()
    for offset in range(0, length, page_size):
        chunk_len = min(page_size, length - offset)
        a = addr + offset
        cmd = b'\x03' + struct.pack('>I', a)[1:]  # 24-bit address
        dev.write(0x02, cmd + b'\x00' * chunk_len)
        resp = dev.read(0x82, chunk_len + 4, timeout=2000)
        if len(resp) > 4:
            data.extend(resp[4:4+chunk_len])
        pct = (offset + chunk_len) * 100 // length
        print(f"\r[READ] {offset+chunk_len}/{length} ({pct}%)", end='', flush=True)
    print()
    return bytes(data)

def dump_flash(dev, filename, size=4194304):
    """Full dump with JEDEC ID verification"""
    jedec = read_jedec_id(dev)
    if jedec:
        mfr, typ, cap = jedec
        chip_name = identify_chip(mfr, typ, cap)
        detected_size = 1 << cap
        print(f"[CHIP] {chip_name}")
        if size > detected_size:
            print(f"[WARN] Requested {size} > detected {detected_size}, using detected")
            size = detected_size
    else:
        print("[WARN] JEDEC ID not read, using default size")

    print(f"[DUMP] {size} bytes → {filename}")
    data = spi_read(dev, 0, size)
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    with open(filename, "wb") as f:
        f.write(data)
    print(f"[OK] Saved: {filename} ({len(data)} bytes)")

def main():
    print("═"*60)
    print("  ARGOS CH341A SPI Dumper v4.0")
    print("═"*60)
    dev = find_ch341a()
    if dev is None:
        print("[ERR] CH341A не найден. VID:PID = 1a86:5512")
        print("[HINT] su -c 'lsusb | grep 1a86'")
        sys.exit(1)
    print(f"[OK] CH341A на Bus {dev.bus} Dev {dev.address}")

    fname = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CAPTURE_DIR, f"ch341a_{int(time.time())}.bin")
    fsize = int(sys.argv[2]) if len(sys.argv) > 2 else 4194304
    dump_flash(dev, fname, fsize)
    usb.util.dispose_resources(dev)

if __name__ == '__main__':
    main()
PYEOF
chmod +x "$SCRIPTS/ch341a_dump.py"

# ====== J-LINK / ST-LINK BRIDGE — REAL SWD/JTAG ======
cat > "$SCRIPTS/debug_bridge.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""J-Link/ST-Link/CMSIS-DAP Bridge v4.0 — SWD/JTAG via openocd/pyocd"""
import subprocess, sys, os, time, json, signal

CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")
LOG_DIR = os.path.expanduser("~/argos-mobile/logs")

DEBUGGERS = {
    "J-Link V9":     {"vid": "1366", "pid": "0105", "type": "swd"},
    "J-Link V8":     {"vid": "1366", "pid": "0101", "type": "swd"},
    "ST-Link V2":    {"vid": "0483", "pid": "3748", "type": "swd"},
    "ST-Link V2-1":  {"vid": "0483", "pid": "374b", "type": "swd"},
    "ST-Link V3":    {"vid": "0483", "pid": "374f", "type": "swd"},
    "CMSIS-DAP":     {"vid": "0d28", "pid": "0204", "type": "swd"},
    "CMSIS-DAP v2":  {"vid": "0d28", "pid": "020c", "type": "swd"},
    "Raspberry Pi Debug Probe": {"vid": "2e8a", "pid": "000c", "type": "swd"},
}

def run_cmd(cmd, timeout=30):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, timeout=timeout, stderr=subprocess.STDOUT)
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERR] {e}"

def detect_probes():
    """Detect debug probes via lsusb"""
    out = run_cmd("su -c 'lsusb'", timeout=5)
    found = []
    for name, info in DEBUGGERS.items():
        key = f"{info['vid']}:{info['pid']}"
        if key in out:
            found.append({"name": name, "vidpid": key, "type": info["type"]})
    return found

def openocd_scan():
    """Scan for targets via openocd"""
    # Create minimal config
    cfg = os.path.join(LOG_DIR, "argos_scan.cfg")
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(cfg, 'w') as f:
        f.write("init\n")
        f.write("targets\n")
        f.write("exit\n")
    out = run_cmd(f"openocd -f interface/cmsis-dap.cfg -f target/cortex_m.cfg -c 'init; targets; exit' 2>&1 || true", timeout=15)
    return out

def pyocd_list():
    """List probes via pyocd"""
    out = run_cmd("pyocd list 2>&1 || true", timeout=10)
    return out

def read_memory(addr=0x08000000, size=256, probe="cmsis-dap"):
    """Read memory via openocd"""
    cfg = os.path.join(LOG_DIR, "argos_read.cfg")
    dump = os.path.join(CAPTURE_DIR, f"mem_{addr:#x}_{int(time.time())}.bin")
    os.makedirs(CAPTURE_DIR, exist_ok=True)
    with open(cfg, 'w') as f:
        f.write(f"source [find interface/{probe}.cfg]\n")
        f.write("source [find target/cortex_m.cfg]\n")
        f.write("init\n")
        f.write(f"dump_image {dump} 0x{addr:08X} 0x{size:X}\n")
        f.write("exit\n")
    out = run_cmd(f"openocd -f {cfg} 2>&1", timeout=20)
    if os.path.exists(dump):
        sz = os.path.getsize(dump)
        print(f"[OK] Memory dump: {dump} ({sz} bytes)")
        return dump
    print(f"[ERR] Dump failed:\n{out}")
    return None

def flash_firmware(fw_file, probe="cmsis-dap", target="stm32f1x"):
    """Flash firmware via openocd"""
    if not os.path.exists(fw_file):
        print(f"[ERR] File not found: {fw_file}")
        return False
    cfg = os.path.join(LOG_DIR, "argos_flash.cfg")
    with open(cfg, 'w') as f:
        f.write(f"source [find interface/{probe}.cfg]\n")
        f.write(f"source [find target/{target}.cfg]\n")
        f.write("init\n")
        f.write("reset halt\n")
        f.write(f"program {fw_file} verify reset exit 0x08000000\n")
    print(f"[FLASH] {fw_file} via {probe}")
    out = run_cmd(f"openocd -f {cfg} 2>&1", timeout=120)
    success = "Verified OK" in out or "success" in out.lower()
    if success:
        print(f"[OK] Flash successful!")
    else:
        print(f"[ERR] Flash failed:\n{out}")
    return success

def main():
    print("═"*60)
    print("  ARGOS Debug Bridge v4.0 — SWD/JTAG")
    print("═"*60)
    
    probes = detect_probes()
    if probes:
        for p in probes:
            print(f"  ✅ {p['name']} ({p['vidpid']}) [{p['type']}]")
    else:
        print("  ❌ Debug probes не обнаружены")
    
    if len(sys.argv) < 2:
        print("\nКоманды:")
        print("  debug_bridge.py scan       — поиск probes + targets")
        print("  debug_bridge.py list       — pyocd list")
        print("  debug_bridge.py read ADDR  — чтение памяти")
        print("  debug_bridge.py flash FILE — прошивка (.hex/.bin)")
        return
    
    cmd = sys.argv[1]
    if cmd == "scan":
        print("\n[SCAN] openocd targets...")
        print(openocd_scan())
    elif cmd == "list":
        print(pyocd_list())
    elif cmd == "read":
        addr = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x08000000
        read_memory(addr)
    elif cmd == "flash":
        if len(sys.argv) < 3:
            print("[ERR] Укажите файл: flash FILE [TARGET]")
        else:
            target = sys.argv[3] if len(sys.argv) > 3 else "stm32f1x"
            flash_firmware(sys.argv[2], target=target)

if __name__ == '__main__':
    main()
PYEOF
chmod +x "$SCRIPTS/debug_bridge.py"

# ====== XGECU T48 BRIDGE — REAL USB PROTOCOL ======
cat > "$SCRIPTS/xgecu_bridge.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""XGecu T48/T56 ISP Bridge v4.0 — USB protocol via minipro"""
import subprocess, sys, os, json, time

XGEcu_VID = "a466"
XGEcu_PID = "0a53"
CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")

def run_cmd(cmd, timeout=30):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, timeout=timeout, stderr=subprocess.STDOUT)
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERR] {e}"

def detect_xgecu():
    out = run_cmd("su -c 'lsusb'", timeout=5)
    if f"{XGEcu_VID}:{XGEcu_PID}" in out:
        return True
    # Also try minipro detection
    out = run_cmd("minipro -p AUTO -r 2>&1 || true", timeout=10)
    if "XGecu" in out or "T48" in out or "T56" in out:
        return True
    return False

def list_devices():
    """List supported devices from minipro database"""
    out = run_cmd("minipro -l 2>/dev/null | head -50")
    if out and "[ERR]" not in out:
        return out
    return None

def read_chip(chip_name="AUTO", size=None):
    """Read chip via minipro CLI"""
    fname = os.path.join(CAPTURE_DIR, f"xgecu_{chip_name}_{int(time.time())}.bin")
    os.makedirs(CAPTURE_DIR, exist_ok=True)
    cmd = f"minipro -p {chip_name} -r {fname}"
    if size:
        cmd += f" -s {size}"
    print(f"[READ] {cmd}")
    out = run_cmd(cmd, timeout=120)
    print(out)
    if os.path.exists(fname):
        sz = os.path.getsize(fname)
        print(f"[OK] Dumped: {fname} ({sz} bytes)")
        return fname
    print("[ERR] Dump failed")
    return None

def write_chip(chip_name, filename, verify=True):
    """Write chip via minipro CLI"""
    if not os.path.exists(filename):
        print(f"[ERR] File not found: {filename}")
        return False
    cmd = f"minipro -p {chip_name} -w {filename}"
    if verify:
        cmd += " -v"
    print(f"[WRITE] {cmd}")
    out = run_cmd(cmd, timeout=300)
    print(out)
    if "Verification OK" in out or "OK" in out:
        print(f"[OK] Written + verified: {filename}")
        return True
    print("[WARN] Verify result unclear")
    return False

def erase_chip(chip_name="AUTO"):
    cmd = f"minipro -p {chip_name} -e"
    print(f"[ERASE] {cmd}")
    out = run_cmd(cmd, timeout=60)
    print(out)
    return "OK" in out or "erase" in out.lower()

def detect_chip_auto():
    """Auto-detect chip"""
    cmd = "minipro -p AUTO -r /dev/null 2>&1 || true"
    out = run_cmd(cmd, timeout=15)
    # Parse chip name from output
    for line in out.split('\n'):
        if "Found" in line or "Device" in line or "Chip" in line:
            print(f"[DETECT] {line.strip()}")
    return out

def main():
    print("═"*60)
    print("  ARGOS XGecu Bridge v4.0 — minipro CLI")
    print("═"*60)
    
    if not detect_xgecu():
        print("[ERR] XGecu T48/T56 не найден.")
        print(f"[HINT] su -c 'lsusb | grep {XGEcu_VID}'")
        sys.exit(1)
    
    print("[OK] XGecu найден")
    
    if len(sys.argv) < 2:
        print("\nИспользование:")
        print("  xgecu_bridge.py detect       — автоопределение чипа")
        print("  xgecu_bridge.py list          — список поддерживаемых чипов")
        print("  xgecu_bridge.py read [CHIP]   — чтение (default: AUTO)")
        print("  xgecu_bridge.py write CHIP FILE — запись + верификация")
        print("  xgecu_bridge.py erase [CHIP]  — стирание")
        return
    
    cmd = sys.argv[1]
    if cmd == "detect":
        detect_chip_auto()
    elif cmd == "list":
        out = list_devices()
        if out:
            print(out)
        else:
            print("[INFO] minipro -l не доступен")
    elif cmd == "read":
        chip = sys.argv[2] if len(sys.argv) > 2 else "AUTO"
        read_chip(chip)
    elif cmd == "write":
        if len(sys.argv) < 4:
            print("[ERR] Укажите: write CHIP FILE")
        else:
            write_chip(sys.argv[2], sys.argv[3])
    elif cmd == "erase":
        chip = sys.argv[2] if len(sys.argv) > 2 else "AUTO"
        erase_chip(chip)
    else:
        print(f"[ERR] Unknown: {cmd}")

if __name__ == '__main__':
    main()
PYEOF
chmod +x "$SCRIPTS/xgecu_bridge.py"

# ====== FNIRSI SCOPE — USB CAPTURE ======
cat > "$SCRIPTS/fnirsi_scope.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""FNIRSI 2C23T / FZ-53 Scope Bridge v4.0"""
import sys, os, time, struct, csv
try:
    import usb.core, usb.util
    HAS_USB = True
except ImportError:
    HAS_USB = False

CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")

# Known FNIRSI VID:PID combos (varies by model)
FNIRSI_DEVICES = [
    (0x1D50, 0x6089),  # FNIRSI-1013D generic
    (0x1D50, 0x604B),  # Another FNIRSI
    (0x04B4, 0x8613),  # Cypress FX2 based
]

def find_fnirsi():
    if not HAS_USB:
        return None
    for vid, pid in FNIRSI_DEVICES:
        dev = usb.core.find(idVendor=vid, idProduct=pid)
        if dev:
            return dev
    # Fallback: try lsusb
    import subprocess
    out = subprocess.check_output("su -c 'lsusb'", shell=True, text=True, stderr=subprocess.DEVNULL)
    for line in out.split('\n'):
        if 'FNIRSI' in line.upper() or '1d50' in line.lower():
            return True  # signal found but can't open
    return None

def capture_via_usb(dev, n_samples=2048):
    """Capture waveform via USB bulk transfer"""
    if dev is True or not HAS_USB:
        return None
    try:
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)
        dev.set_configuration()
        # Try EP 1 IN (0x81) or EP 2 IN (0x82)
        for ep_in in [0x81, 0x82, 0x83]:
            try:
                data = dev.read(ep_in, n_samples * 2, timeout=3000)
                return data
            except: continue
    except Exception as e:
        print(f"[USB] {e}")
    return None

def parse_samples(raw_data, channels=1, resolution=8):
    """Parse raw bytes into sample values"""
    samples = []
    if resolution == 8:
        for b in raw_data:
            samples.append(b)
    else:  # 16-bit
        for i in range(0, len(raw_data), 2):
            val = struct.unpack('<h', raw_data[i:i+2])[0]
            samples.append(val)
    return samples

def save_csv(samples, ch_names=None, filename=None):
    if filename is None:
        filename = os.path.join(CAPTURE_DIR, f"fnirsi_{int(time.time())}.csv")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ch_names or ["sample"]
        writer.writerow(["idx"] + header)
        for i, v in enumerate(samples):
            writer.writerow([i, v])
    print(f"[OK] CSV: {filename} ({len(samples)} samples)")
    return filename

def print_ascii_plot(samples, width=60, height=12):
    """Simple ASCII waveform plot"""
    if not samples:
        return
    mn, mx = min(samples), max(samples)
    rng = mx - mn or 1
    lines = [[' '] * width for _ in range(height)]
    for i, v in enumerate(samples[:width]):
        y = int((1 - (v - mn) / rng) * (height - 1))
        y = max(0, min(height - 1, y))
        lines[y][i] = '█'
    for row in lines:
        print(''.join(row))

def main():
    print("═"*60)
    print("  ARGOS FNIRSI Scope Bridge v4.0")
    print("═"*60)
    
    dev = find_fnirsi()
    if dev is None:
        print("[ERR] FNIRSI не найден.")
        print("[HINT] Подключите FNIRSI scope через USB OTG")
        sys.exit(1)
    
    print("[OK] FNIRSI обнаружен")
    
    n_samples = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
    
    raw = capture_via_usb(dev, n_samples)
    if raw:
        samples = parse_samples(raw)
        print(f"[CAPTURED] {len(samples)} samples")
        print_ascii_plot(samples)
        save_csv(samples)
    else:
        print("[WARN] USB capture failed. Device may need vendor software.")
        print("[INFO] Для полной поддержки используйте sigrok/PulseView на ПК.")

if __name__ == '__main__':
    main()
PYEOF
chmod +x "$SCRIPTS/fnirsi_scope.py"

# ====== WIFI PENTEST (Andrax / aircrack) ======
cat > "$SCRIPTS/wifi_pentest.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""WiFi pentest wrapper — aircrack-ng via Andrax or Termux"""
import subprocess, sys, os

def check_tool(cmd):
    return os.system(f"which {cmd} > /dev/null 2>&1") == 0

def main():
    print("═"*70)
    print("  ARGOS WiFi Pentest")
    print("═"*70)
    tools = {
        "aircrack-ng": "WPA/WEP cracking",
        "airodump-ng": "AP/client sniffing",
        "aireplay-ng": "Packet injection",
        "mdk4": "Deauth / beacon flood",
        "iw": "Wireless config",
        "wpa_supplicant": "WPA client",
    }
    print("[STATUS] Tools:")
    for t, d in tools.items():
        ok = check_tool(t)
        print(f"  {'✅' if ok else '❌'} {t} — {d}")
    print("\n[INFO] Полный WiFi pentest требует:")
    print("  • USB WiFi adapter с monitor mode (RTL8812AU, AR9271)")
    print("  • Root для iwconfig + airmon-ng")
    print("  • Или запустите из Andrax chroot: ./andrax.sh")

if __name__ == '__main__':
    main()
PYEOF
chmod +x "$SCRIPTS/wifi_pentest.py"

# ====== ARGOS BRIDGE — MQTT + HEARTBEAT + COMMANDS ======
cat > "$SCRIPTS/argos_bridge.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/python3
"""ARGOS Agent Bridge v4.0 — MQTT + heartbeat + command dispatcher"""
import socket, json, time, subprocess, os, sys, threading, signal
import traceback

BRAIN_HOST = os.getenv('ARGOS_BRAIN_HOST', '192.168.1.53')
BRAIN_PORT = int(os.getenv('ARGOS_BRAIN_PORT', '5001'))
MQTT_HOST = os.getenv('ARGOS_MQTT_HOST', BRAIN_HOST)
MQTT_PORT = int(os.getenv('ARGOS_MQTT_PORT', '1883'))
AGENT_ID = os.getenv('ARGOS_AGENT_ID', 'agent-mobile-willow')
BEACON_INTERVAL = 30
COMMAND_PORT = int(os.getenv('ARGOS_MOBILE_PORT', '7779'))
SCRIPTS = os.path.expanduser("~/argos-mobile/scripts")
LOG_DIR = os.path.expanduser("~/argos-mobile/logs")

running = True

def get_ip():
    try:
        out = subprocess.check_output(['ip', 'addr', 'show', 'wlan0'], text=True)
        for line in out.split('\n'):
            if 'inet ' in line:
                return line.split()[1].split('/')[0]
    except: pass
    return 'unknown'

def get_battery():
    try:
        out = subprocess.check_output(['termux-battery-status'], text=True)
        data = json.loads(out)
        return f"{data.get('percentage', '?')}%"
    except: return 'unknown'

def get_usb_devices():
    try:
        out = subprocess.check_output(['su', '-c', 'lsusb'], text=True, stderr=subprocess.DEVNULL)
        return len([l for l in out.split('\n') if 'ID' in l])
    except: return 0

def get_status():
    return {
        'id': AGENT_ID,
        'type': 'mobile',
        'platform': 'android',
        'device': 'willow',
        'ip': get_ip(),
        'battery': get_battery(),
        'usb_devices': get_usb_devices(),
        'timestamp': time.time(),
        'services': ['ssh:8022', f'commands:{COMMAND_PORT}', 'argos-bridge'],
        'root': os.system('su -c "id -u" > /dev/null 2>&1') == 0
    }

def exec_command(cmd_str):
    """Execute a command and return result"""
    resp = {"status": "ok", "cmd": cmd_str}
    
    if cmd_str == "status":
        resp["result"] = get_status()
    elif cmd_str == "usb_scan":
        try:
            out = subprocess.check_output(
                [sys.executable, os.path.join(SCRIPTS, "usb_hub.py"), "--json"],
                text=True, timeout=15, stderr=subprocess.STDOUT)
            resp["result"] = json.loads(out)
        except Exception as e:
            resp["error"] = str(e)
    elif cmd_str.startswith("obd"):
        try:
            out = subprocess.check_output(
                [sys.executable, os.path.join(SCRIPTS, "obd_bridge.py")],
                text=True, timeout=15, stderr=subprocess.STDOUT)
            resp["result"] = out.split('\n')
        except Exception as e:
            resp["error"] = str(e)
    elif cmd_str.startswith("ble"):
        try:
            out = subprocess.check_output(
                [sys.executable, os.path.join(SCRIPTS, "ble_scan.py")],
                text=True, timeout=20, stderr=subprocess.STDOUT)
            resp["result"] = out.split('\n')
        except Exception as e:
            resp["error"] = str(e)
    elif cmd_str.startswith("shell:"):
        shell_cmd = cmd_str[6:]
        try:
            out = subprocess.check_output(['su', '-c', shell_cmd], text=True,
                                          stderr=subprocess.STDOUT, timeout=30)
            resp["result"] = out
        except Exception as e:
            resp["error"] = str(e)
    elif cmd_str.startswith("run:"):
        script = cmd_str[4:]
        path = os.path.join(SCRIPTS, script)
        if os.path.exists(path):
            try:
                out = subprocess.check_output(
                    [sys.executable, path], text=True, timeout=60,
                    stderr=subprocess.STDOUT)
                resp["result"] = out
            except Exception as e:
                resp["error"] = str(e)
        else:
            resp["error"] = f"Script not found: {script}"
    else:
        resp["error"] = f"Unknown command: {cmd_str}"
    
    return resp

def http_beacon():
    """Send status to Brain API"""
    while running:
        try:
            payload = json.dumps(get_status()).encode()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((BRAIN_HOST, BRAIN_PORT))
            s.sendall(payload + b'\n')
            s.close()
        except Exception as e:
            print(f"[BRIDGE] HTTP beacon fail: {e}")
        time.sleep(BEACON_INTERVAL)

def mqtt_beacon():
    """Send status via MQTT (if available)"""
    try:
        import paho.mqtt.client as mqtt
        client = mqtt.Client(client_id=AGENT_ID)
        client.on_connect = lambda c, u, f, rc: print(f"[MQTT] Connected ({rc})")
        client.on_disconnect = lambda c, u, f: print(f"[MQTT] Disconnected")
        try:
            client.connect(MQTT_HOST, MQTT_PORT, 60)
        except Exception as e:
            print(f"[MQTT] Connect failed: {e}, falling back to HTTP only")
            http_beacon()
            return
        
        client.loop_start()
        while running:
            status = json.dumps(get_status())
            client.publish(f"argos/agents/{AGENT_ID}/status", status)
            client.publish(f"argos/agents/{AGENT_ID}/heartbeat", str(int(time.time())))
            time.sleep(BEACON_INTERVAL)
        client.loop_stop()
    except ImportError:
        print("[MQTT] paho-mqtt not installed, using HTTP beacon")
        http_beacon()

def command_listener():
    """TCP command listener"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(1.0)
    s.bind(('0.0.0.0', COMMAND_PORT))
    s.listen(5)
    print(f"[BRIDGE] Commands on :{COMMAND_PORT}")
    
    while running:
        try:
            conn, addr = s.accept()
            conn.settimeout(10)
            data = conn.recv(4096).decode().strip()
            if not data:
                conn.close()
                continue
            print(f"[CMD] {addr[0]}: {data}")
            resp = exec_command(data)
            conn.sendall(json.dumps(resp, ensure_ascii=False).encode() + b'\n')
            conn.close()
        except socket.timeout:
            continue
        except Exception as e:
            print(f"[BRIDGE] Cmd error: {e}")
    s.close()

def signal_handler(sig, frame):
    global running
    running = False
    print("\n[BRIDGE] Shutting down...")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"[ARGOS Bridge v4.0] Agent: {AGENT_ID}")
    print(f"  Brain: {BRAIN_HOST}:{BRAIN_PORT}")
    print(f"  MQTT:  {MQTT_HOST}:{MQTT_PORT}")
    print(f"  Cmd:   :{COMMAND_PORT}")
    
    # Start beacon thread (tries MQTT first, falls back to HTTP)
    t1 = threading.Thread(target=mqtt_beacon, daemon=True)
    t1.start()
    
    # Start command listener in main thread
    command_listener()
    print("[BRIDGE] Stopped")
PYEOF
chmod +x "$SCRIPTS/argos_bridge.py"

# ====== OTG SETUP ======
cat > "$SCRIPTS/otg_setup.sh" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# ARGOS OTG Setup — через tsu
echo "[ARGOS] OTG Setup via tsu..."
if ! command -v tsu > /dev/null 2>&1; then
    echo "[ERR] tsu не установлен. pkg install tsu"
    exit 1
fi
tsu -c "chmod 666 /dev/ttyUSB* /dev/ttyACM* /dev/ttyCH340* /dev/hidraw* 2>/dev/null; chmod -R 666 /dev/bus/usb/*/* 2>/dev/null; echo '[OK] USB permissions set'"
EOF
chmod +x "$SCRIPTS/otg_setup.sh"

# ====== START / STOP SERVICES ======
cat > "$SCRIPTS/start_argos.sh" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
ARGOS_MOBILE="$HOME/argos-mobile"
LOG="$ARGOS_MOBILE/logs/services.log"
mkdir -p "$ARGOS_MOBILE/logs"
exec 1>>"$LOG" 2>&1
echo "[$(date)] Starting ARGOS services..."
sshd 2>/dev/null || true
echo "[$(date)] sshd started"
bash "$ARGOS_MOBILE/scripts/otg_setup.sh" || true
export ARGOS_BRAIN_HOST="${ARGOS_BRAIN_HOST:-192.168.1.53}"
nohup python "$ARGOS_MOBILE/scripts/argos_bridge.py" > /dev/null 2>&1 &
echo "[$(date)] bridge started PID: $!"
echo "[$(date)] All services started"
EOF
chmod +x "$SCRIPTS/start_argos.sh"

cat > "$SCRIPTS/stop_argos.sh" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
pkill -f argos_bridge.py 2>/dev/null || true
pkill -f can_sniff.py 2>/dev/null || true
pkill sshd 2>/dev/null || true
echo "[ARGOS] Services stopped"
EOF
chmod +x "$SCRIPTS/stop_argos.sh"

# ── 9. Environment ───────────────────────────────────────────────────────────
echo "[9/10] Окружение..."

cat > "$HOME/.termux/termux.properties" << 'EOF'
extra-keys = [
 ['ESC','|','/','HOME','UP','END','PGUP'],
 ['TAB','CTRL','ALT','LEFT','DOWN','RIGHT','PGDN']
]
EOF

cat > "$HOME/.bashrc_argos" << 'EOF'
# ═══════════════════════════════════════════════════════════════════════════════
#  ARGOS Mobile Multi-Tool v4.0 — FULL PROTOCOL ARSENAL
# ═══════════════════════════════════════════════════════════════════════════════
alias ll='ls -lah'
alias ..='cd ..'
alias ip='ip addr show wlan0 2>/dev/null || ifconfig wlan0'
alias root='tsu'
alias su='tsu'

# USB / Serial
alias obd='python ~/argos-mobile/scripts/obd_bridge.py'
alias uart='python ~/argos-mobile/scripts/uart_bridge.py'
alias scan='python ~/argos-mobile/scripts/usb_scan.py'
alias can='python ~/argos-mobile/scripts/can_sniff.py'
alias can500='python ~/argos-mobile/scripts/can_sniff.py can0 500000'
alias can250='python ~/argos-mobile/scripts/can_sniff.py can0 250000'
alias ble='python ~/argos-mobile/scripts/ble_scan.py'

# Programmers / Debug
alias ch341='python ~/argos-mobile/scripts/ch341a_dump.py'
alias debug='python ~/argos-mobile/scripts/debug_bridge.py'
alias xgecu='python ~/argos-mobile/scripts/xgecu_bridge.py'
alias fnirsi='python ~/argos-mobile/scripts/fnirsi_scope.py'

# WiFi / RF
alias wifi='python ~/argos-mobile/scripts/wifi_pentest.py'

# Network / Bridge
alias bridge='python ~/argos-mobile/scripts/argos_bridge.py'
alias flash='python ~/argos-mobile/scripts/ch341a_dump.py'
alias otg='bash ~/argos-mobile/scripts/otg_setup.sh'
alias hub='python ~/argos-mobile/scripts/usb_hub.py'
alias hub-auto='python ~/argos-mobile/scripts/usb_hub.py --auto'

# KolibriOS / Colibri
alias kolibri-os='bash ~/argos-kolibri/kolibri-os.sh'
alias kolibri-stop='bash ~/argos-kolibri/kolibri-stop.sh'
alias colibri='python ~/argos-kolibri/colibri/colibri_cli.py'

# Service control
alias start-argos='bash ~/argos-mobile/scripts/start_argos.sh'
alias stop-argos='bash ~/argos-mobile/scripts/stop_argos.sh'
alias logcat-save='logcat -d > /sdcard/Download/logcat_$(date +%Y%m%d_%H%M%S).txt'
alias argos-status='su -c /system/xbin/argos-status 2>/dev/null || echo "System module not loaded"'

# Environment
export ARGOS_MOBILE=1
export ARGOS_AGENT_ID="agent-mobile-willow"
export ARGOS_BRAIN_HOST="192.168.1.53"
export ARGOS_BRAIN_PORT="5001"
export PATH="$HOME/argos-mobile/bin:$HOME/argos-mobile/scripts:$PATH"
export PYTHONPATH="$HOME/argos-mobile:$PYTHONPATH"

echo -e "\e[32m╔════════════════════════════════════════════════════════════════╗\e[0m"
echo -e "\e[32m║     ARGOS Mobile Multi-Tool v4.0 — FULL ARSENAL              ║\e[0m"
echo -e "\e[32m╠════════════════════════════════════════════════════════════════╣\e[0m"
echo -e "\e[36m║  scan      \e[0m→ USB arsenal scanner (CH340/FTDI/ELM/J-Link)  \e[36m║\e[0m"
echo -e "\e[36m║  obd       \e[0m→ OBD-II bridge (ELM327)                      \e[36m║\e[0m"
echo -e "\e[36m║  uart      \e[0m→ USB-UART terminal                           \e[36m║\e[0m"
echo -e "\e[36m║  can       \e[0m→ CAN bus sniffer (root + adapter)            \e[36m║\e[0m"
echo -e "\e[36m║  ble       \e[0m→ BLE scanner (nRF/Flipper/custom)          \e[36m║\e[0m"
echo -e "\e[36m║  ch341     \e[0m→ CH341A EEPROM/Flash dumper                  \e[36m║\e[0m"
echo -e "\e[36m║  debug     \e[0m→ SWD/JTAG debugger detector                \e[36m║\e[0m"
echo -e "\e[36m║  xgecu     \e[0m→ XGecu T48 bridge                            \e[36m║\e[0m"
echo -e "\e[36m║  fnirsi    \e[0m→ FNIRSI scope/multimeter                   \e[36m║\e[0m"
echo -e "\e[36m║  wifi      \e[0m→ WiFi pentest status                         \e[36m║\e[0m"
echo -e "\e[36m║  hub       \e[0m→ USB auto-detect hub (menu/auto)   \e[36m║\e[0m"
echo -e "\e[36m║  hub-auto  \e[0m→ USB auto-launch scripts       \e[36m║\e[0m"
echo -e "\e[36m║  bridge    \e[0m→ ARGOS network bridge (MQTT)  \e[36m║\e[0m"
echo -e "\e[36m║  otg       \e[0m→ Fix USB permissions                         \e[36m║\e[0m"
echo -e "\e[36m║  root      \e[0m→ Root shell (tsu)                            \e[36m║\e[0m"
echo -e "\e[32m╚════════════════════════════════════════════════════════════════╝\e[0m"
EOF

if ! grep -q "source ~/.bashrc_argos" "$HOME/.bashrc" 2>/dev/null; then
    echo "source ~/.bashrc_argos" >> "$HOME/.bashrc"
fi

# ── 10. Andrax chroot link (if installed) ───────────────────────────────────
if [ -f "$HOME/andrax.sh" ]; then
    echo "[10/10] Andrax обнаружен — добавляю алиасы..."
    echo "alias andrax='cd ~ && ./andrax.sh'" >> "$HOME/.bashrc_argos"
fi

# ── Finish ─────────────────────────────────────────────────────────────────
echo ""
echo -e "\e[32m══════════════════════════════════════════════════════════\e[0m"
echo -e "\e[32m  ARGOS Mobile Multi-Tool v4.0 УСТАНОВЛЕН!            \e[0m"
echo -e "\e[32m══════════════════════════════════════════════════════════\e[0m"
echo ""
echo "Перезапустите Termux: source ~/.bashrc"
echo "SSH: ssh -p 8022 ${WHOAMI}@$(ip addr show wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)"
echo ""
echo "Все алиасы: scan, obd, uart, can, ble, ch341, debug, xgecu, fnirsi, wifi, bridge, otg, hub"
