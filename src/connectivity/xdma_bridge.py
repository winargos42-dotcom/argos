#!/usr/bin/env python3
"""ARGOS factory SC4/Xilinx XDMA transport inspector (read-only).

Grounded in Xilinx/dma_ip_drivers, XDMA/linux-kernel/xdma:
- cdev_ctrl.c:char_ctrl_read() performs exactly one ioread32(), returns 4.
- cdev_sgdma.c:char_sgdma_read_write() uses *pos as AXI endpoint address.
- libxdma.c:probe_one_engine() detects AXI-ST via identifier bit 15.
- libxdma.c:identify_bars() distinguishes user BAR and config BAR.

THIS IS NOT THE PROPRIETARY GTI2800 KERNEL DRIVER.
There is NO invented ioctl->FPGA mapping, per-NPU selector, model-upload
or inference facility. Any write or C2H DMA would be an unsupported and
potentially dangerous physical action, so this adapter implements neither.

Verified history on the physical card (2026-10-10):
10ee:7022/1e00:2801, user BAR "sc4_xdma" and 0x61a7330d;
H2C at AXI 0x10000 completed 256B and separately 88B, but did NOT
prove NPU ACK. C2H at AXI 0x10000 timed out once. Do not repeat.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping
import os

PCI_DEVICE = "0000:04:00.0"
PCI_VENDOR = "0x10ee"
PCI_ID = "0x7022"
PCI_SUBSYSTEM_DEVICE = "0x2801"
USER_BAR = "/dev/xdma0_user"
CONTROL_BAR = "/dev/xdma0_control"
H2C_ENGINE_ID = 0x1FC00006
C2H_ENGINE_ID = 0x1FC10006
SC4_FINGERPRINT = 0x61A7330D
STREAMING_FLAG = 1 << 15
# Only offsets already verified read-only on this particular firmware.
USER_OFFSETS = frozenset({0, 4, 8, 12} | {
    base + word for base in (0x10, 0x20, 0x30, 0x40)
    for word in (0, 4, 8, 12)
})
CONTROL_OFFSETS = frozenset({
    0x0, 0x40, 0x1000, 0x1040, 0x2004, 0x2010
})
STATUS_OFFSETS = (0x18, 0x28, 0x38, 0x48)


class XDMAProbeError(RuntimeError):
    """Hardware identity differs, or a safe read returned invalid data."""


class FactoryGTIMappingMissing(RuntimeError):
    """Generic XDMA cannot infer which FPGA register targets an NPU."""


@dataclass(frozen=True)
class Engine:
    identifier: int
    status: int
    memory_mapped: bool


@dataclass(frozen=True)
class SC4Snapshot:
    identity: str
    fingerprint: int
    h2c: Engine
    c2h: Engine
    logical_slot_values: tuple[int, int, int, int]

    def as_dict(self) -> dict:
        return {
            "identity": self.identity,
            "fingerprint": hex(self.fingerprint),
            "h2c": {
                "id": hex(self.h2c.identifier), "status": hex(self.h2c.status),
                "memory_mapped": self.h2c.memory_mapped,
            },
            "c2h": {
                "id": hex(self.c2h.identifier), "status": hex(self.c2h.status),
                "memory_mapped": self.c2h.memory_mapped,
            },
            "logical_slot_status": [hex(v) for v in self.logical_slot_values],
            "four_physical_chip_selects_verified": False,
            "factory_gt2801_command_abi_recovered": False,
            "dma_weight_upload_allowed": False,
            "physical_inference_verified": False,
        }


def _read32(fd: int, offset: int, reader: Callable[[int, int, int], bytes]) -> int:
    if offset < 0 or offset % 4:
        raise XDMAProbeError("Only aligned known uint32 offsets are supported")
    chunk = reader(fd, 4, offset)
    if len(chunk) != 4:
        raise XDMAProbeError(f"Expected exactly four bytes at {offset:#x}")
    return int.from_bytes(chunk, "little")


def read_snapshot(
    *,
    opener: Callable[[str, int], int] = os.open,
    reader: Callable[[int, int, int], bytes] = os.pread,
    closer: Callable[[int], None] = os.close,
    user_path: str = USER_BAR,
    control_path: str = CONTROL_BAR,
) -> SC4Snapshot:
    """Bounded hardware read. No device writes, reset, C2H or DMA submit.

    Dependency-injectable opener/reader/closer permits purely offline tests.
    """
    u = opener(user_path, os.O_RDONLY | os.O_CLOEXEC)
    try:
        c = opener(control_path, os.O_RDONLY | os.O_CLOEXEC)
        try:
            def r_user(offset: int) -> int:
                if offset not in USER_OFFSETS:
                    raise XDMAProbeError("Unknown SC4 BAR register")
                return _read32(u, offset, reader)

            def r_control(offset: int) -> int:
                if offset not in CONTROL_OFFSETS:
                    raise XDMAProbeError("Unknown XDMA control offset")
                return _read32(c, offset, reader)

            signature = (
                r_user(0).to_bytes(4, "little") +
                r_user(4).to_bytes(4, "little")
            )
            if signature != b"sc4_xdma" or r_user(8) != SC4_FINGERPRINT:
                raise XDMAProbeError("Unexpected factory SC4 identity")
            h2c_id = r_control(0)
            c2h_id = r_control(0x1000)
            if h2c_id != H2C_ENGINE_ID or c2h_id != C2H_ENGINE_ID:
                raise XDMAProbeError("Unexpected XDMA engine identifiers")
            h2c = Engine(h2c_id, r_control(0x40), not bool(h2c_id & STREAMING_FLAG))
            c2h = Engine(c2h_id, r_control(0x1040), not bool(c2h_id & STREAMING_FLAG))
            return SC4Snapshot(
                "sc4_xdma", SC4_FINGERPRINT, h2c, c2h,
                tuple(r_user(offset) for offset in STATUS_OFFSETS),
            )
        finally:
            closer(c)
    finally:
        closer(u)


def verify_pci_identity(sysfs_root: Path = Path("/sys/bus/pci/devices")) -> bool:
    dev = sysfs_root / PCI_DEVICE
    try:
        return (
            (dev / "vendor").read_text().strip() == PCI_VENDOR
            and (dev / "device").read_text().strip() == PCI_ID
            and (dev / "subsystem_device").read_text().strip() == PCI_SUBSYSTEM_DEVICE
        )
    except OSError:
        return False


def require_verified_npu_route(*_args, **_kwargs) -> None:
    """Intentionally fail closed until genuine factory NPU ABI is recovered."""
    raise FactoryGTIMappingMissing(
        "Xilinx XDMA provides AXI memory-mapped DMA, not the GTI2800 "
        "command protocol. A successful pwrite to 0x10000 is not NPU ACK. "
        "No chip-select mapping, model/weight upload, or NPU readout is "
        "authorized based on currently available evidence."
    )


if __name__ == "__main__":
    if not verify_pci_identity():
        raise SystemExit("PCI SC4 identity not verified; no device opened")
    print(read_snapshot().as_dict())
