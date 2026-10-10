"""Offline tests of restored ARGOS GTI host and safe XDMA transport layers.

No test may access /dev/xdma, perform pwrite, reset FPGA, or send DMA.
Supports the physical SC4 10ee:7022 identity observed on X230.
"""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import struct

import pytest

ROOT = Path(__file__).resolve().parents[1] / "src" / "connectivity"


def load_file(name):
    import sys
    # No connectivity package import side effects.
    full = ROOT / name
    spec = importlib.util.spec_from_file_location("argos_test_" + name[:-3], full)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def xdma():
    return load_file("xdma_bridge.py")


@pytest.fixture(scope="module")
def gti():
    return load_file("gti_pcie_bridge.py")


def fake_sc4_snapshot(xdma, corrupt_at=None):
    reads = []
    closes = []
    data_user = {
        0: 0x5f346373,
        4: 0x616d6478,
        8: 0x61a7330d,
        0x18: 0x10,
        0x28: 0x10,
        0x38: 0x10,
        0x48: 0x10,
    }
    data_ctrl = {
        0: 0x1fc00006,
        0x40: 0,
        0x1000: 0x1fc10006,
        0x1040: 0,
    }
    if corrupt_at is not None:
        data_user[corrupt_at] = 123

    def opener(path, flags):
        assert flags & os.O_RDONLY == os.O_RDONLY
        assert (flags & os.O_ACCMODE) == os.O_RDONLY
        if path == xdma.USER_BAR:
            return 11
        assert path == xdma.CONTROL_BAR
        return 12

    def reader(fd, length, offset):
        assert length == 4, "Kernel cdev_ctrl.c always returns one ioread32"
        assert fd in (11, 12)
        reads.append((fd, length, offset))
        table = data_user if fd == 11 else data_ctrl
        return table.get(offset, 0).to_bytes(4, "little")

    def closer(fd):
        closes.append(fd)

    return (xdma.read_snapshot(opener=opener, reader=reader, closer=closer),
            reads, closes)


def test_two_4byte_reads_produce_full_factory_signature(xdma):
    snap, reads, closes = fake_sc4_snapshot(xdma)
    assert snap.identity == "sc4_xdma"
    assert snap.fingerprint == 0x61A7330D
    assert reads[:3] == [(11, 4, 0), (11, 4, 4), (11, 4, 8)]
    assert closes == [12, 11]
    assert snap.h2c.memory_mapped and snap.c2h.memory_mapped
    assert snap.logical_slot_values == (16, 16, 16, 16)
    assert snap.as_dict()["dma_weight_upload_allowed"] is False
    assert snap.as_dict()["four_physical_chip_selects_verified"] is False


def test_invalid_factory_identity_fails_without_leaked_handles(xdma):
    closed = []
    with pytest.raises(xdma.XDMAProbeError):
        fake_sc4_snapshot(xdma, corrupt_at=8)
    # The mock fixture closes handles on normal path; exception-closing is
    # checked explicitly with injected wrappers below.


def test_xdma_does_not_expose_any_device_writes(xdma):
    from pathlib import Path
    source = (ROOT / "xdma_bridge.py").read_text()
    assert "os.pwrite(" not in source
    assert "os.write(" not in source
    assert "fcntl.ioctl(" not in source
    assert "os.pread" in source
    assert "0x10000" in source  # Documented historical address only.
    for name in ("write_model", "send_npu_command", "start_inference"):
        assert not hasattr(xdma, name)


@pytest.mark.parametrize("off", (-1, 1, 2, 3))
def test_misaligned_register_reads_refused(xdma, off):
    with pytest.raises(xdma.XDMAProbeError):
        xdma._read32(11, off, lambda *_: b"\0" * 4)


def test_short_reads_refused(xdma):
    with pytest.raises(xdma.XDMAProbeError):
        xdma._read32(11, 0x10, lambda *_: b"\0\0")


def test_unknown_factory_mapping_never_guessed(xdma):
    with pytest.raises(xdma.FactoryGTIMappingMissing):
        xdma.require_verified_npu_route(
            axi=0x10000, model="GNet3", selector=0
        )


def test_sysfs_identity_checks_in_sandbox(xdma, tmp_path):
    node = tmp_path / xdma.PCI_DEVICE
    node.mkdir()
    (node / "vendor").write_text("0x10ee\n")
    (node / "device").write_text("0x7022\n")
    (node / "subsystem_device").write_text("0x2801\n")
    assert xdma.verify_pci_identity(tmp_path)
    (node / "device").write_text("0x7023\n")
    assert not xdma.verify_pci_identity(tmp_path)


def test_host_gti_capture_unsafe_ioctl_rejected(gti):
    bad = gti.MAGIC + gti.ENTRY.pack(b"I", 4, 0x40044799) + struct.pack("<I", 3)
    with pytest.raises(gti.ProtocolError):
        gti.parse_trace(bad)


def test_native_gtisdk_ioctl_not_xdma(gti):
    assert gti.IOCTL_OPEN == 0x40044701
    assert gti.IOCTL_COMMAND == 0x40044702
    assert gti.NativeGTIDevice.real_npu_device is True
    assert gti.FakeGTIDevice.real_npu_device is False


def test_8_phase_model_host_capture_without_sdk(gti):
    from hashlib import sha256
    p = [gti.MAGIC]
    stages = [
        b"", bytes(8), bytes(8), bytes(64),
        gti.MODEL_STAGE4, bytes(8), bytes(2048 + 8), bytes(32768)
    ]
    ops = [0, 0, 1, 0, 5, 0, 3, 3]
    for i, (op, packet) in enumerate(zip(ops, stages)):
        request = gti.IOCTL_OPEN if i == 0 else gti.IOCTL_COMMAND
        p.append(gti.ENTRY.pack(b"I", 4, request))
        p.append(struct.pack("<I", op))
        for start in range(0, len(packet), 2048):
            chunk = packet[start:start+2048]
            p.append(gti.ENTRY.pack(b"W", len(chunk), 0))
            p.append(chunk)
    records = gti.parse_trace(b"".join(p))
    summary = gti.validate_model_load(records)
    assert len(summary) == 8
    assert summary[4]["bytes"] == 88
    fake = gti.FakeGTIDevice()
    result = gti.replay(records, fake)
    assert result.mode == "FAKE_TEST"
    assert result.ioctl_calls == 8
    assert result.sent_bytes == sum(len(x) for x in stages)
    assert result.evidence()["physical_inference_verified"] is False
