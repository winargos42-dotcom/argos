"""Offline unit tests for reconstructed ARGOS GTI/Xilinx XDMA bridge.

All I/O in tests targets regular temporary files or FakeGTIDevice.
Never access real /dev/xdma, no FPGA/NPU DMA, BAR writes or firmware change.
Run: python -m unittest discover -s tests -p 'test_spr2801_gti_xdma.py' -v
"""
from __future__ import annotations
import os
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

CONNECTIVITY = Path(__file__).resolve().parents[1] / "src" / "connectivity"
sys.path.insert(0, str(CONNECTIVITY))

import gti_pcie_bridge as gti
import xdma_transport as xdma


def original_host_model_trace():
    """Minimal stage6 test payload: correct host framing, fake data, no hardware."""
    chunks = []
    lengths = {
        0: b"",
        1: bytes(8),
        2: bytes(8),
        3: bytes(64),
        4: bytes.fromhex("00 02") + bytes(86),
        5: bytes(8),
        6: bytes(2112),
        7: bytes(32768),
    }
    for idx, opcode in enumerate(gti.MODEL_OPCODES):
        request = gti.IOCTL_OPEN if idx == 0 else gti.IOCTL_COMMAND
        data = struct.pack("<I", opcode)
        chunks.append(gti.ENTRY.pack(b"I", 4, request) + data)
        body = lengths[idx]
        for off in range(0, len(body), gti.MAX_CHUNK):
            part = body[off:off + gti.MAX_CHUNK]
            chunks.append(gti.ENTRY.pack(b"W", len(part), 0) + part)
    return gti.MAGIC + b"".join(chunks)


class VendorIOCTLTests(unittest.TestCase):
    def test_xilinx_ioctl_magics_distinct_from_manufacturer(self):
        self.assertEqual(xdma.ioctl_type(0x40044701), ord("G"))
        self.assertEqual(xdma.ioctl_type(0x40044702), ord("G"))
        self.assertEqual(xdma.XDMA_CTRL_IOCTL_TYPE, ord("x"))
        self.assertEqual(xdma.XDMA_SGDMA_IOCTL_TYPE, ord("q"))
        self.assertNotEqual(xdma.GTI_IOCTL_TYPE, xdma.XDMA_CTRL_IOCTL_TYPE)
        self.assertNotEqual(xdma.GTI_IOCTL_TYPE, xdma.XDMA_SGDMA_IOCTL_TYPE)

    def test_unknown_ioctl_rejected(self):
        raw = original_host_model_trace()
        with self.assertRaises(gti.ProtocolError):
            gti.parse_trace(raw.replace(
                gti.ENTRY.pack(b"I", 4, gti.IOCTL_OPEN),
                gti.ENTRY.pack(b"I", 4, 0x40047101), 1))
        with self.assertRaises(ValueError):
            xdma.ioctl_type(-1)
        with self.assertRaises(ValueError):
            xdma.ioctl_type(0x100000000)

    def test_offline_model_load_reconstructs_all_eight_stages(self):
        records = gti.parse_trace(original_host_model_trace())
        stages = gti.validate_model_load(records)
        self.assertEqual(len(stages), 8)
        self.assertEqual([x["opcode"] for x in stages], list(gti.MODEL_OPCODES))
        self.assertEqual([x["bytes"] for x in stages],
                         [0, 8, 8, 64, 88, 8, 2112, 32768])
        device = gti.FakeGTIDevice()
        result = gti.replay(records, device, logical_index=0)
        self.assertEqual(result.mode, "FAKE_TEST")
        self.assertEqual(result.ioctl_calls, 8)
        self.assertEqual(result.sent_bytes, 0 + 8 + 8 + 64 + 88 + 8 + 2112 + 32768)
        self.assertEqual(result.read_calls, 0)
        self.assertFalse(result.evidence()["physical_inference_verified"])
        self.assertFalse(result.evidence()["asic_package_mapping_verified"])

    def test_native_driver_absence_is_error_not_fake_XDMA_upload(self):
        with patch.object(Path, "exists", return_value=False):
            with self.assertRaisesRegex(gti.FactoryABIMissing, "kernel driver unavailable"):
                gti.NativeGTIDevice(0)
        with self.assertRaises(ValueError):
            gti.NativeGTIDevice(4)
        with self.assertRaises(ValueError):
            gti.NativeGTIDevice(-1)


class XDMAFactoryReadOnlyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.pci = root / "pci"
        self.pci.mkdir()
        for name, value in xdma.EXPECTED.items():
            (self.pci / name).write_text(value)
        self.user = root / "xdma0_user"
        user = bytearray(0x50)
        user[0:8] = b"sc4_xdma"
        user[8:12] = xdma.SC4_FINGERPRINT.to_bytes(4, "little")
        for slot in xdma.SLOT_BASES:
            user[slot + 8:slot + 12] = (0x10).to_bytes(4, "little")
        self.user.write_bytes(user)
        self.control = root / "xdma0_control"
        ctrl = bytearray(0x1050)
        ctrl[0:4] = xdma.XDMA_H2C_ID.to_bytes(4, "little")
        ctrl[0x1000:0x1004] = xdma.XDMA_C2H_ID.to_bytes(4, "little")
        self.control.write_bytes(ctrl)
        self.transport = xdma.XDMAFactorySC4(
            sysfs=self.pci, user_node=self.user, control_node=self.control)

    def test_reads_only_aligned_known_xilinx_registers(self):
        buf = self.user.read_bytes()
        fd = os.open(self.user, os.O_RDONLY)
        try:
            self.assertEqual(xdma.read_u32(fd, 0x18, allowed=xdma.USER_OFFSETS), 0x10)
            for off in (0x90, 0x94, 0x19, 0x50, 0x10000):
                with self.assertRaises(ValueError):
                    xdma.read_u32(fd, off, allowed=xdma.USER_OFFSETS)
        finally:
            os.close(fd)
        self.assertEqual(buf, self.user.read_bytes())
        self.assertLessEqual(max(xdma.USER_OFFSETS), 0x4c)

    def test_four_logical_banks_without_invented_chip_assignment(self):
        u0 = self.user.read_bytes()
        c0 = self.control.read_bytes()
        data = self.transport.probe()
        self.assertEqual(data["factory_signature"], "sc4_xdma")
        self.assertEqual(data["h2c_engine_mode"], "AXI-MM")
        self.assertEqual(data["c2h_engine_mode"], "AXI-MM")
        self.assertEqual(len(data["logical_register_banks"]), 4)
        for i, block in enumerate(data["logical_register_banks"]):
            self.assertEqual(block["logical_bank"], i)
            self.assertEqual(block["readback_words"], ["0x0", "0x0", "0x10", "0x0"])
            self.assertIsNone(block["SPR2801S_physical_package"])
        self.assertFalse(data["GTI2800_ioctl_to_SC4_AXI_verified"])
        self.assertFalse(data["NPU_load_or_inference_verified"])
        self.assertEqual(data["mmio_writes"], 0)
        self.assertEqual(data["h2c_writes"], 0)
        self.assertEqual(data["c2h_requests"], 0)
        self.assertEqual(self.user.read_bytes(), u0)
        self.assertEqual(self.control.read_bytes(), c0)

    def test_wrong_bus_identity_fails_closed(self):
        (self.pci / "device").write_text("0x9999")
        with self.assertRaisesRegex(RuntimeError, "Wrong PCI identity"):
            self.transport.probe()

    def test_streaming_engine_instead_of_memory_mapped_fails_closed(self):
        ctrl = bytearray(self.control.read_bytes())
        ctrl[0:4] = (xdma.XDMA_H2C_ID | 0x8000).to_bytes(4, "little")
        self.control.write_bytes(ctrl)
        with self.assertRaises(RuntimeError):
            self.transport.probe()

    def test_unknown_GTIFIP_mapping_disallows_real_model_upload(self):
        with self.assertRaisesRegex(RuntimeError, "Generic Xilinx XDMA"):
            self.transport.load_model(bytes(88))


if __name__ == "__main__":
    unittest.main()
