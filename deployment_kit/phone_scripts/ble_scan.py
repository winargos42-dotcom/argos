#!/usr/bin/env python3
"""
BLE Scanner v4.0 for ARGOS Multi-Tool
Enhanced with service identification, RSSI bar, JSON output
"""
import asyncio, sys, os, json, time
try:
    from bleak import BleakScanner
except ImportError:
    print("[ERR] bleak not installed. pip install bleak")
    sys.exit(1)
from rich.console import Console
from rich.table import Table

console = Console()
LOG_DIR = os.path.expanduser("~/argos-mobile/logs")

BLE_SERVICES = {
    "1800": "Generic Access", "1801": "Generic Attribute", "180A": "Device Info",
    "180F": "Battery", "1812": "HID over GATT", "FE59": "Nordic DFU",
    "8EC90001": "Flipper Zero", "6E400001": "Nordic UART", "F000FFC0": "TI CC2652",
    "0000FFE0": "HM-10/11", "0000FFF0": "JDY-xx",
}


def service_name(uuid):
    uid = uuid.replace("-", "").upper()
    for k, v in BLE_SERVICES.items():
        if uid.startswith(k) or uid.endswith(k): return v
    return None


async def scan(timeout=10, output_json=False):
    console.print(f"[bold blue]ARGOS BLE Scanner v4.0[/bold blue] (timeout={timeout}s)")
    devices = await BleakScanner.discover(timeout=timeout, return_adv=True)
    
    table = Table(title=f"BLE Devices ({len(devices)})", show_lines=True)
    table.add_column("Name", style="cyan")
    table.add_column("MAC", style="magenta")
    table.add_column("RSSI", style="green")
    table.add_column("Services")
    
    results = []
    for addr, (d, adv) in devices.items():
        name = d.name or "(Unknown)"
        rssi = adv.rssi if hasattr(adv, 'rssi') else "?"
        uuids = adv.service_uuids if hasattr(adv, 'service_uuids') else []
        svc_names = [service_name(str(u)) or str(u)[:12] for u in uuids]
        
        table.add_row(name, d.address, str(rssi), ", ".join(svc_names) or "-")
        results.append({"name": name, "address": d.address, "rssi": rssi,
                        "services": svc_names, "time": time.strftime("%H:%M:%S")})
    
    console.print(table)
    
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"ble_scan_{int(time.time())}.json")
    with open(log_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    console.print(f"[green]✓ Log: {log_path}[/green]")
    
    if output_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    timeout = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
    json_out = "--json" in sys.argv
    try: asyncio.run(scan(timeout, json_out))
    except KeyboardInterrupt: console.print("[red]Stopped[/red]")
