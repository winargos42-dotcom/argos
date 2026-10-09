#!/usr/bin/env python3
"""Read-only Xilinx XDMA transport inspection for ARGOS SPR2801S.

Grounded in https://github.com/Xilinx/dma_ip_drivers:
  XDMA/linux-kernel/xdma/cdev_ctrl.c  (each pread is exactly 4 bytes)
  XDMA/linux-kernel/xdma/cdev_sgdma.c (pread/pwrite offset is AXI address)
  XDMA/linux-kernel/xdma/cdev_sgdma.h (SGDMA ioctl magic is 'q')
  XDMA/linux-kernel/xdma/cdev_ctrl.h  (control ioctl magic is 'x')
  XDMA/linux-kernel/xdma/libxdma.c   (engine ID bit 15 means AXI-ST)

Only inspects known registers of an existing factory SC4 device; it never
uses DMA engines, writes BAR or activates any NPU. Read-only capabilities
do NOT establish FPGA FIP, chip selector or command acknowledgement.
"""
from __future__ import annotations
import json
import os
from pathlib import Path

PCI_BDF = "0000:04:00.0"
EXPECTED = {"vendor": "0x10ee", "device": "0x7022", "subsystem_device": "0x2801"}
SC4_SIGNATURE = b"sc4_xdma"
SC4_FINGERPRINT = 0x61A7330D
XDMA_H2C_ID = 0x1FC00006
XDMA_C2H_ID = 0x1FC10006
SLOT_BASES = (0x10, 0x20, 0x30, 0x40)
# Only historical verified factory SC4 user offsets; no 0x90/0x94.
USER_OFFSETS = (0, 4, 8) + tuple(base + i for base in SLOT_BASES for i in (0, 4, 8, 12))
CONTROL_OFFSETS = (0, 0x40, 0x1000, 0x1040)
GTI_IOCTL_TYPE = 0x47  # 'G': user-space manufacturer's proprietary ABI
XDMA_CTRL_IOCTL_TYPE = ord("x")
XDMA_SGDMA_IOCTL_TYPE = ord("q")


def ioctl_type(request: int) -> int:
    """Linux _IOC_TYPE() = bits 8..15, no actual ioctl performed."""
    if not isinstance(request, int) or request < 0 or request > 0xFFFFFFFF:
        raise ValueError("Invalid ioctl request")
    return (request >> 8) & 255


def read_u32(fd: int, offset: int, *, allowed: tuple[int, ...]) -> int:
    """Official cdev_ctrl.c char_ctrl_read(): one aligned LE32 per pread."""
    if not isinstance(offset, int) or offset not in allowed or offset % 4:
        raise ValueError("Unverified BAR offset forbidden")
    block = os.pread(fd, 4, offset)
    if len(block) != 4:
        raise OSError("Short XDMA BAR read")
    return int.from_bytes(block, "little")


class XDMAFactorySC4:
    """Existing official-driver hardware preflight; zero writes, zero DMA."""

    def __init__(
        self,
        *,
        sysfs: Path = Path("/sys/bus/pci/devices") / PCI_BDF,
        user_node: Path = Path("/dev/xdma0_user"),
        control_node: Path = Path("/dev/xdma0_control"),
    ):
        self.sysfs = Path(sysfs)
        self.user_node = Path(user_node)
        self.control_node = Path(control_node)

    def probe(self) -> dict:
        ids: dict[str, str] = {}
        for item, expected in EXPECTED.items():
            ids[item] = (self.sysfs / item).read_text(encoding="ascii").strip().lower()
            if ids[item] != expected:
                raise RuntimeError(f"Wrong PCI identity {item}: {ids[item]}")
        if (self.sysfs / "driver").exists():
            actual = (self.sysfs / "driver").resolve().name
            if actual != "xdma":
                raise RuntimeError(f"Wrong kernel driver: {actual}")
        u = os.open(str(self.user_node), os.O_RDONLY | os.O_CLOEXEC)
        try:
            user = {off: read_u32(u, off, allowed=USER_OFFSETS) for off in USER_OFFSETS}
        finally:
            os.close(u)
        c = os.open(str(self.control_node), os.O_RDONLY | os.O_CLOEXEC)
        try:
            ctrl = {off: read_u32(c, off, allowed=CONTROL_OFFSETS) for off in CONTROL_OFFSETS}
        finally:
            os.close(c)

        identity = user[0].to_bytes(4, "little") + user[4].to_bytes(4, "little")
        if identity != SC4_SIGNATURE or user[8] != SC4_FINGERPRINT:
            raise RuntimeError("Factory SC4 signature or ID mismatch")
        if ctrl[0] != XDMA_H2C_ID or ctrl[0x1000] != XDMA_C2H_ID:
            raise RuntimeError("Unexpected XDMA engine identity")
        # libxdma.c checks engine identifier's 0x8000U bit.
        if ctrl[0] & 0x8000 or ctrl[0x1000] & 0x8000:
            raise RuntimeError("AXI-ST rather than expected memory-mapped engine")
        slots = [
            {
                "logical_bank": i,
                "offset": hex(base),
                "readback_words": [
                    hex(user[base + rel]) for rel in (0, 4, 8, 12)
                ],
                "SPR2801S_physical_package": None,
                "NPU_command_registers_known": False,
            }
            for i, base in enumerate(SLOT_BASES)
        ]
        return {
            "pci": PCI_BDF,
            "ids": ids,
            "factory_signature": identity.decode("ascii"),
            "factory_fingerprint": hex(user[8]),
            "h2c_engine_id": hex(ctrl[0]),
            "c2h_engine_id": hex(ctrl[0x1000]),
            "h2c_engine_mode": "AXI-MM",
            "c2h_engine_mode": "AXI-MM",
            "logical_register_banks": slots,
            "control_status_words": {"h2c": hex(ctrl[0x40]), "c2h": hex(ctrl[0x1040])},
            "all_nodes_opened_read_only": True,
            "mmio_writes": 0,
            "h2c_writes": 0,
            "c2h_requests": 0,
            "GTI2800_ioctl_to_SC4_AXI_verified": False,
            "NPU_load_or_inference_verified": False,
        }

    def load_model(self, *args, **kwargs):
        raise RuntimeError(
            "No factory GTI2800 ioctl-to-SC4 AXI/FIP mapping or NPU ACK. "
            "Generic Xilinx XDMA does not translate GTI commands."
        )


def main():
    print(json.dumps(XDMAFactorySC4().probe(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
