"""Regression of recovered ARGOS host GTI/XDMA bridge, no hardware calls.

The original vendor GtiCreateModel trace must be validated BEFORE executing
ANY GTI ioctl on a genuine /dev/gti2800-N device. Fake device never claims
NPU inference, and generic xdma has no GTI command mapping.
"""
import importlib.util
from pathlib import Path
import struct
import sys
import unittest

SOURCE=Path(__file__).resolve().parents[1]/"src"/"gti_pcie_bridge.py"
spec=importlib.util.spec_from_file_location("spr2801_gti_bridge_recovered",SOURCE)
gti=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=gti
spec.loader.exec_module(gti)


def fake_capture(model_size=2056,extra_ioctl=None):
    payloads=[b"",bytes(8),bytes(8),bytes(64),gti.MODEL_STAGE4,bytes(8),
              bytes(model_size),bytes(32768)]
    data=bytearray(gti.MAGIC)
    for i,(opcode,payload) in enumerate(zip(gti.MODEL_OPCODES,payloads)):
        data.extend(gti.ENTRY.pack(b"I",4,gti.IOCTL_OPEN if i==0 else gti.IOCTL_COMMAND))
        data.extend(struct.pack("<I",opcode))
        for at in range(0,len(payload),2048):
            blob=payload[at:at+2048]
            data.extend(gti.ENTRY.pack(b"W",len(blob),0))
            data.extend(blob)
    if extra_ioctl is not None:
        data.extend(gti.ENTRY.pack(b"I",4,gti.IOCTL_COMMAND))
        data.extend(struct.pack("<I",extra_ioctl))
    return bytes(data)


class NativeSpy:
    real_npu_device=True
    def __init__(self):self.calls=[]
    def ioctl(self,*a):self.calls.append(("ioctl",a))
    def write(self,*a):self.calls.append(("write",a))
    def read(self,*a):self.calls.append(("read",a));return b""
    def close(self):pass


class FactoryBridgeSafetyTests(unittest.TestCase):
    def test_native_trailing_ninth_command_rejected_before_device(self):
        rec=gti.parse_trace(fake_capture(extra_ioctl=0xfeedcafe))
        with self.assertRaisesRegex(gti.ProtocolError,"Unverified extra"):
            gti.validate_model_load(rec)
        spy=NativeSpy()
        with self.assertRaises(gti.ProtocolError):
            gti.replay(rec,spy)
        self.assertEqual(spy.calls,[])

    def test_native_unverified_model_hash_rejected_before_device(self):
        rec=gti.parse_trace(fake_capture())
        spy=NativeSpy()
        with self.assertRaisesRegex(gti.FactoryABIMissing,"SHA256 not verified"):
            gti.replay(rec,spy)
        self.assertEqual(spy.calls,[])

    def test_valid_fake_model_load_baseline(self):
        rec=gti.parse_trace(fake_capture())
        summary=gti.validate_model_load(rec)
        self.assertEqual([r["bytes"] for r in summary],
                         [0,8,8,64,88,8,2056,32768])
        stub=gti.FakeGTIDevice()
        outcome=gti.replay(rec,stub)
        self.assertEqual(outcome.mode,"FAKE_TEST")
        self.assertEqual(outcome.ioctl_calls,8)
        self.assertEqual(outcome.writes,23)
        self.assertFalse(outcome.evidence()["physical_inference_verified"])

    def test_manufacturer_captures_whitelisted_exactly(self):
        self.assertEqual(len(gti.VERIFIED_MODEL_GTITXN_SHA256),2)
        self.assertEqual(gti.VERIFIED_MODEL_GTITXN_SHA256,{
          "9978890e0accc21e0a6e87f96f6fd38ae07604d26bd0835dae8104e91cbd51ec",
          "22fe1a77530f8f4ad9d51bf2149f024f18711b144158e0e3e839bd8396cc1f81",
        })

    def test_device_index_four_way_is_only_logical(self):
        for idx in (-1,4,True,None,"0"):
            with self.assertRaises(ValueError):
                gti.NativeGTIDevice(idx)
        for i in range(4):
            path=Path(f"/dev/gti2800-{i}")
            if not path.exists():
                with self.assertRaises(gti.FactoryABIMissing):
                    gti.NativeGTIDevice(i)

    def test_no_direct_xdma_gtifip_substitution(self):
        source=SOURCE.read_text()
        assert "os.pwrite(" not in source
        self.assertIn("xdma_to_GTIFIP_driver_map_verified",source)
        self.assertIn("FIP",source)


if __name__=="__main__":
    unittest.main()
