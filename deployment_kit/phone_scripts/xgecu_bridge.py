#!/usr/bin/env python3
"""
XGecu T48/T56 ISP Bridge v4.0 for ARGOS Multi-Tool
Uses minipro CLI for real chip read/write/erase operations
"""
import subprocess, sys, os, time
from rich.console import Console

console = Console()
CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")


def run_cmd(cmd, timeout=30):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, timeout=timeout, stderr=subprocess.STDOUT)
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERR] {e}"


def detect_xgecu():
    out = run_cmd("minipro -p AUTO -r /dev/null 2>&1 || true", timeout=10)
    if any(x in out for x in ["XGecu", "T48", "T56", "TL866"]):
        return True
    out2 = run_cmd("su -c 'lsusb' 2>/dev/null", timeout=5)
    return "a466:0a53" in out2


def read_chip(chip_name="AUTO"):
    fname = os.path.join(CAPTURE_DIR, f"xgecu_{chip_name}_{int(time.time())}.bin")
    os.makedirs(CAPTURE_DIR, exist_ok=True)
    console.print(f"[blue]Reading chip '{chip_name}' via minipro...[/blue]")
    out = run_cmd(f"minipro -p {chip_name} -r {fname}", timeout=120)
    console.print(out)
    if os.path.exists(fname):
        console.print(f"[bold green]✓ Dumped: {fname} ({os.path.getsize(fname)} bytes)[/bold green]")
        return fname
    console.print("[red]Dump failed[/red]")
    return None


def write_chip(chip_name, filename, verify=True):
    if not os.path.exists(filename):
        console.print(f"[red]File not found: {filename}[/red]")
        return False
    cmd = f"minipro -p {chip_name} -w {filename}" + (" -v" if verify else "")
    console.print(f"[blue]Writing {filename} to {chip_name}...[/blue]")
    out = run_cmd(cmd, timeout=300)
    console.print(out)
    if "Verification OK" in out or "OK" in out:
        console.print(f"[bold green]✓ Written + verified[/bold green]")
        return True
    return False


def erase_chip(chip_name="AUTO"):
    out = run_cmd(f"minipro -p {chip_name} -e", timeout=60)
    console.print(out)
    return "OK" in out


def detect_chip():
    out = run_cmd("minipro -p AUTO -r /dev/null 2>&1 || true", timeout=15)
    for line in out.split('\n'):
        if any(x in line for x in ["Found", "Device", "Chip"]):
            console.print(f"[cyan]{line.strip()}[/cyan]")
    return out


if __name__ == "__main__":
    if not detect_xgecu():
        console.print("[red]XGecu programmer not found. Connect via USB OTG.[/red]")
        sys.exit(1)
    console.print("[green]XGecu found[/green]")
    if len(sys.argv) < 2:
        console.print("[bold]Commands:[/bold] detect | list | read [CHIP] | write CHIP FILE | erase [CHIP]")
    else:
        cmd = sys.argv[1]
        if cmd == "detect": detect_chip()
        elif cmd == "list": console.print(run_cmd("minipro -l 2>/dev/null | head -50"))
        elif cmd == "read": read_chip(sys.argv[2] if len(sys.argv) > 2 else "AUTO")
        elif cmd == "write":
            if len(sys.argv) >= 4: write_chip(sys.argv[2], sys.argv[3])
            else: console.print("[red]Usage: write CHIP FILE[/red]")
        elif cmd == "erase": erase_chip(sys.argv[2] if len(sys.argv) > 2 else "AUTO")
        else: console.print(f"[red]Unknown: {cmd}[/red]")
