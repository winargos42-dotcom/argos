#!/usr/bin/env python3
"""
FNIRSI Scope Bridge v4.0 for ARGOS Multi-Tool
USB capture + ASCII waveform plot + CSV export
"""
import sys, os, time, struct, csv
try:
    import usb.core, usb.util
    HAS_USB = True
except ImportError:
    HAS_USB = False
from rich.console import Console

console = Console()
CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")
FNIRSI_DEVICES = [(0x1D50, 0x6089), (0x1D50, 0x604B)]


def find_fnirsi():
    if not HAS_USB: return None
    for vid, pid in FNIRSI_DEVICES:
        dev = usb.core.find(idVendor=vid, idProduct=pid)
        if dev: return dev
    return None


def capture_via_usb(dev, n_samples=2048):
    try:
        if dev.is_kernel_driver_active(0): dev.detach_kernel_driver(0)
        dev.set_configuration()
        for ep_in in [0x81, 0x82, 0x83]:
            try:
                return dev.read(ep_in, n_samples * 2, timeout=3000)
            except: continue
    except Exception as e:
        console.print(f"[yellow]USB: {e}[/yellow]")
    return None


def save_csv(samples, filename=None):
    if filename is None:
        filename = os.path.join(CAPTURE_DIR, f"fnirsi_{int(time.time())}.csv")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["idx", "value"])
        for i, v in enumerate(samples): w.writerow([i, v])
    console.print(f"[green]✓ CSV: {filename} ({len(samples)} samples)[/green]")
    return filename


def ascii_plot(samples, width=60, height=12):
    if not samples: return
    mn, mx = min(samples), max(samples)
    rng = mx - mn or 1
    lines = [[' '] * width for _ in range(height)]
    step = max(1, len(samples) // width)
    for i in range(min(width, len(samples) // step)):
        v = samples[i * step]
        y = int((1 - (v - mn) / rng) * (height - 1))
        y = max(0, min(height - 1, y))
        lines[y][i] = '█'
    for row in lines:
        print(''.join(row))


if __name__ == "__main__":
    console.print("[bold blue]ARGOS FNIRSI Scope v4.0[/bold blue]")
    dev = find_fnirsi()
    if dev is None:
        console.print("[red]FNIRSI not found. Connect via USB OTG.[/red]")
        sys.exit(1)
    console.print("[green]FNIRSI found[/green]")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
    raw = capture_via_usb(dev, n)
    if raw:
        samples = [b for b in raw] if len(raw) == n else [struct.unpack('<h', raw[i:i+2])[0] for i in range(0, len(raw), 2)]
        console.print(f"[green]Captured {len(samples)} samples[/green]")
        ascii_plot(samples)
        save_csv(samples)
    else:
        console.print("[yellow]USB capture failed. Use sigrok/PulseView on PC.[/yellow]")
