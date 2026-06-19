#!/data/data/com.termux/files/usr/bin/python3
"""
CH341A Flash/EEPROM Dumper for ARGOS Multi-Tool v4.0
Real SPI protocol via pyusb
"""
import sys, os, time, struct
try:
    import usb.core, usb.util
    HAS_USB = True
except ImportError:
    HAS_USB = False
from rich.console import Console

console = Console()
CH341_VID = 0x1A86
CH341_PID = 0x5512

CAPTURE_DIR = os.path.expanduser("~/argos-mobile/captures")

CHIP_DB = {
    "W25Q32":  {"size": 4194304,  "page": 256},
    "W25Q64":  {"size": 8388608,  "page": 256},
    "W25Q128": {"size": 16777216, "page": 256},
    "MX25L3206":{"size": 4194304, "page": 256},
    "GD25Q32": {"size": 4194304, "page": 256},
    "SST25VF016B":{"size": 2097152, "page": 256},
}


def find_ch341a():
    if not HAS_USB:
        console.print("[red]pyusb not installed[/red]")
        return None
    dev = usb.core.find(idVendor=CH341_VID, idProduct=CH341_PID)
    if dev is None:
        dev = usb.core.find(idVendor=CH341_VID, idProduct=0x7523)
    if dev and dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    if dev:
        dev.set_configuration()
    return dev


def read_jedec_id(dev):
    """Read JEDEC ID: cmd 0x9F"""
    try:
        dev.write(0x02, b'\x9F\x00\x00\x00\x00')
        resp = dev.read(0x82, 5, timeout=1000)
        if len(resp) >= 5:
            return resp[2], resp[3], resp[4]
    except: pass
    return None


def identify_chip(mfr, typ, cap):
    size = 1 << cap
    mfr_names = {0xEF: "Winbond", 0xC2: "Macronix", 0x1C: "EON",
                 0xC8: "GigaDevice", 0xBF: "SST", 0x20: "Micron"}
    name = mfr_names.get(mfr, f"MFR:0x{mfr:02X}")
    return f"{name} 0x{typ:02X}0x{cap:02X} ({size//1024}KB)"


def dump_flash(dev, filename=None, size=None):
    jedec = read_jedec_id(dev)
    chip_name = "Unknown"
    if jedec:
        mfr, typ, cap = jedec
        chip_name = identify_chip(mfr, typ, cap)
        if size is None:
            size = 1 << cap
        console.print(f"[cyan]Chip: {chip_name}[/cyan]")

    if size is None:
        size = 4194304  # Default 4MB
    if filename is None:
        filename = os.path.join(CAPTURE_DIR, f"ch341a_{int(time.time())}.bin")

    console.print(f"[green]Reading {size} bytes into {filename}...[/green]")
    data = bytearray()
    for addr in range(0, size, 256):
        cmd = b'\x03' + struct.pack('>I', addr)[1:] + b'\x00' * 256
        try:
            dev.write(0x02, cmd)
            resp = dev.read(0x82, 260, timeout=2000)
            if len(resp) > 4:
                data.extend(resp[4:260])
            pct = (addr + 256) * 100 // size
            console.print(f"[dim]Read {addr+256}/{size} ({pct}%)[/dim]", end="\r")
        except Exception as e:
            console.print(f"[red]Read error at {addr}: {e}[/red]")
            break

    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    with open(filename, "wb") as f:
        f.write(data)
    console.print(f"\n[bold green]✓ Dump saved: {filename} ({len(data)} bytes)[/bold green]")
    return 0


if __name__ == "__main__":
    dev = find_ch341a()
    if not dev:
        console.print("[red]CH341A not found. Connect via USB OTG + check permissions.[/red]")
        sys.exit(1)
    console.print(f"[green]CH341A found: Bus {dev.bus} Dev {dev.address}[/green]")
    fname = sys.argv[1] if len(sys.argv) > 1 else None
    fsize = int(sys.argv[2]) if len(sys.argv) > 2 else None
    sys.exit(dump_flash(dev, fname, fsize) or 0)
