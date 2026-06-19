#!/usr/bin/env python3
"""
J-Link/ST-Link/CMSIS-DAP Debug Bridge v4.0 for ARGOS Multi-Tool
SWD/JTAG via openocd + pyocd
"""
import subprocess, sys, os, time, json
from rich.console import Console
from rich.table import Table

console = Console()
CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")
LOG_DIR = os.path.expanduser("~/argos-mobile/logs")

DEBUGGERS = {
    "J-Link V9":    {"vid": "1366", "pid": "0105"},
    "J-Link V8":    {"vid": "1366", "pid": "0101"},
    "ST-Link V2":   {"vid": "0483", "pid": "3748"},
    "ST-Link V2-1": {"vid": "0483", "pid": "374b"},
    "ST-Link V3":   {"vid": "0483", "pid": "374f"},
    "CMSIS-DAP":    {"vid": "0d28", "pid": "0204"},
    "CMSIS-DAP v2": {"vid": "0d28", "pid": "020c"},
    "RP Debug Probe":{"vid": "2e8a", "pid": "000c"},
}


def run_cmd(cmd, timeout=30):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, timeout=timeout, stderr=subprocess.STDOUT)
    except subprocess.TimeoutExpired: return "[TIMEOUT]"
    except Exception as e: return f"[ERR] {e}"


def detect_probes():
    out = run_cmd("su -c 'lsusb' 2>/dev/null", timeout=5)
    found = []
    for name, info in DEBUGGERS.items():
        key = f"{info['vid']}:{info['pid']}"
        if key in out:
            found.append({"name": name, "vidpid": key})
    return found


def scan_targets():
    return run_cmd("openocd -f interface/cmsis-dap.cfg -f target/cortex_m.cfg -c 'init; targets; exit' 2>&1 || true", timeout=15)


def pyocd_list():
    return run_cmd("pyocd list 2>&1 || true", timeout=10)


def read_memory(addr=0x08000000, size=256):
    dump = os.path.join(CAPTURE_DIR, f"mem_{addr:#x}_{int(time.time())}.bin")
    os.makedirs(CAPTURE_DIR, exist_ok=True)
    cfg = os.path.join(LOG_DIR, "argos_read.cfg")
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(cfg, 'w') as f:
        f.write("source [find interface/cmsis-dap.cfg]\nsource [find target/cortex_m.cfg]\n")
        f.write("init\n")
        f.write(f"dump_image {dump} 0x{addr:08X} 0x{size:X}\nexit\n")
    out = run_cmd(f"openocd -f {cfg} 2>&1", timeout=20)
    if os.path.exists(dump):
        console.print(f"[green]✓ Memory dump: {dump} ({os.path.getsize(dump)} bytes)[/green]")
        return dump
    console.print(f"[red]Dump failed[/red]")
    return None


def flash_firmware(fw_file, target="stm32f1x"):
    if not os.path.exists(fw_file):
        console.print(f"[red]File not found: {fw_file}[/red]")
        return False
    cfg = os.path.join(LOG_DIR, "argos_flash.cfg")
    with open(cfg, 'w') as f:
        f.write("source [find interface/cmsis-dap.cfg]\n")
        f.write(f"source [find target/{target}.cfg]\n")
        f.write("init\nreset halt\n")
        f.write(f"program {fw_file} verify reset exit 0x08000000\n")
    console.print(f"[blue]Flashing {fw_file}...[/blue]")
    out = run_cmd(f"openocd -f {cfg} 2>&1", timeout=120)
    ok = "Verified OK" in out or "success" in out.lower()
    if ok: console.print("[bold green]✓ Flash successful[/bold green]")
    else: console.print(f"[red]Flash failed:\n{out[:500]}[/red]")
    return ok


if __name__ == "__main__":
    console.print("[bold blue]ARGOS Debug Bridge v4.0 — SWD/JTAG[/bold blue]")
    probes = detect_probes()
    table = Table(title="Debug Probes")
    table.add_column("Status", width=6)
    table.add_column("Name")
    table.add_column("VID:PID")
    for name, info in DEBUGGERS.items():
        key = f"{info['vid']}:{info['pid']}"
        found = any(p["vidpid"] == key for p in probes)
        table.add_row("✅" if found else "❌", name, key)
    console.print(table)

    if len(sys.argv) < 2:
        console.print("\n[dim]Commands: scan | list | read [ADDR] | flash FILE [TARGET][/dim]")
    else:
        cmd = sys.argv[1]
        if cmd == "scan": console.print(scan_targets())
        elif cmd == "list": console.print(pyocd_list())
        elif cmd == "read": read_memory(int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x08000000)
        elif cmd == "flash":
            if len(sys.argv) >= 3: flash_firmware(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "stm32f1x")
            else: console.print("[red]Usage: flash FILE [TARGET][/red]")
        else: console.print(f"[red]Unknown: {cmd}[/red]")
