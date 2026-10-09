"""ARGOS GTI SPR2801 bridge regression tests. No PCIe/MMIO/DMA operations.

Factory reference: original Gyrfalcon 4.5.1 host model-load captures:
GNet3 stage6 2779448 bytes / 1379 write calls total;
GNet18 stage6 4601864 bytes / 2269 write calls total.
These are synthetic payloads with exact factory packet framing.
"""
import hashlib
import struct
from unittest import mock
from pathlib import Path
import pytest

from src.connectivity.gti_pcie_bridge import (
    MAGIC,ENTRY,IOCTL_OPEN,IOCTL_COMMAND,MAX_CHUNK,MODEL_STAGE4,
    ProtocolError,FactoryABIMissing,NativeGTIDevice,FakeGTIDevice,
    Record,parse_trace,validate_model_load,replay,sc4_status_read_only,
)

def r(kind,payload=b"",request=0,read_count=0):
    n=read_count if kind==b"R" else len(payload)
    return ENTRY.pack(kind,n,request)+(b"" if kind==b"R" else payload)

def factory_trace(model_size=2779448,readback=False):
    assert model_size in (2779448,4601864)
    payloads=[b"",bytes(8),bytes(8),bytes(64),MODEL_STAGE4,
              bytes(8),bytes(model_size),bytes(32768)]
    data=bytearray(MAGIC)
    for stage,(opcode,payload) in enumerate(zip((0,0,1,0,5,0,3,3),payloads)):
        data.extend(r(b"I",struct.pack("<I",opcode),
                      IOCTL_OPEN if stage==0 else IOCTL_COMMAND))
        for i in range(0,len(payload),2048):
            data.extend(r(b"W",payload[i:i+2048]))
    if readback:
        data.extend(r(b"I",struct.pack("<I",5),IOCTL_COMMAND))
        for i in range(16):data.extend(r(b"R",read_count=2048))
    return bytes(data)

@pytest.mark.parametrize("size,expected_writes",[(2779448,1379),(4601864,2269)])
def test_exact_full_native_host_model_load(size,expected_writes):
    records=parse_trace(factory_trace(model_size=size))
    stages=validate_model_load(records)
    assert [x["bytes"] for x in stages]==[0,8,8,64,88,8,size,32768]
    assert [x["opcode"] for x in stages]==[0,0,1,0,5,0,3,3]
    assert stages[4]["sha256"]==hashlib.sha256(MODEL_STAGE4).hexdigest()
    assert stages[7]["writes"]==16
    fake=FakeGTIDevice()
    outcome=replay(records,fake,logical_index=2)
    assert outcome.ioctl_calls==8
    assert outcome.writes==expected_writes
    assert outcome.sent_bytes==size+32944
    assert outcome.read_calls==0
    assert outcome.evidence()["physical_inference_verified"] is False
    assert outcome.evidence()["asic_package_mapping_verified"] is False
    assert fake.ioctls[0]==(IOCTL_OPEN,0)
    assert fake.ioctls[4]==(IOCTL_COMMAND,5)

def test_fake_result_cannot_be_called_npu_inference():
    fake=FakeGTIDevice()
    out=replay(parse_trace(factory_trace(readback=True)),fake)
    assert out.read_calls==16
    assert len(out.read_bytes)==32768
    assert fake.read_requests==[2048]*16
    assert out.evidence()["physical_inference_verified"] is False
    assert out.evidence()["read_from_native_gti_driver"] is False

@pytest.mark.parametrize("bad",[
    b"not gti", MAGIC+b"?",MAGIC+ENTRY.pack(b"Q",0,0),
    MAGIC+ENTRY.pack(b"I",4,0x40044703)+bytes(4),
    MAGIC+ENTRY.pack(b"I",4,IOCTL_OPEN)+bytes(3),
    MAGIC+ENTRY.pack(b"W",5,0)+bytes(5),
    MAGIC+ENTRY.pack(b"R",0,0),
])
def test_unknown_or_corrupt_record_rejected(bad):
    with pytest.raises(ProtocolError):parse_trace(bad)

def test_corrupted_opcode_is_rejected_before_hardware():
    records=parse_trace(factory_trace())
    records[0]=Record(b"I",IOCTL_OPEN,struct.pack("<I",93))
    with pytest.raises(ProtocolError):validate_model_load(records)

def test_native_device_indices_are_strictly_0_through_3():
    for v in (True,False,-1,4,"0",None):
        with pytest.raises(ValueError):NativeGTIDevice(v)

def test_vendor_missing_fails_closed_no_xdma_fallback(monkeypatch):
    monkeypatch.setattr(Path,"exists",lambda self:False)
    with pytest.raises(FactoryABIMissing):
        NativeGTIDevice(0)

def test_real_vendor_backend_exact_native_ioctl_and_read_write(monkeypatch):
    calls=[]
    monkeypatch.setattr(Path,"exists",lambda self:True)
    monkeypatch.setattr("os.open",lambda path,flags: calls.append(("open",path)) or 18)
    monkeypatch.setattr("fcntl.ioctl",lambda fd,cmd,arg: calls.append(("ioctl",fd,cmd,arg)))
    monkeypatch.setattr("os.write",lambda fd,buf: calls.append(("write",fd,buf)) or len(buf))
    monkeypatch.setattr("os.read",lambda fd,n: calls.append(("read",fd,n)) or bytes([0xAB])*n)
    monkeypatch.setattr("os.close",lambda fd: calls.append(("close",fd)))
    with NativeGTIDevice(3) as dev:
        dev.ioctl(IOCTL_OPEN,0)
        dev.ioctl(IOCTL_COMMAND,5)
        dev.write(b"\x00\x02\x00\x00")
        assert dev.read(4)==b"\xab"*4
    assert calls[0]==("open","/dev/gti2800-3")
    assert ("ioctl",18,IOCTL_OPEN,bytes(4)) in calls
    assert ("ioctl",18,IOCTL_COMMAND,struct.pack("<I",5)) in calls
    assert ("write",18,b"\x00\x02\x00\x00") in calls
    assert ("read",18,4) in calls
    assert calls[-1]==("close",18)

def test_native_interface_never_promises_xdma_to_npu_mapping():
    code=(Path(__file__).resolve().parents[1]/"src/connectivity/gti_pcie_bridge.py").read_text()
    native_backend=code.split("class NativeGTIDevice:",1)[1].split("class FakeGTIDevice:",1)[0]
    # Global device-inventory only mentions /dev/xdma*; NativeGTIDevice
    # must never secretly use that generic transport to replay GTI ioctls.
    assert "/dev/xdma0_h2c_0" not in native_backend
    assert "os.pwrite(" not in code
    assert "xdma_model_upload_enabled" in code
    assert "FIP" in code

def test_readonly_sc4_gate_reports_no_inference():
    info=sc4_status_read_only()
    assert info["xdma_to_GTIFIP_driver_map_verified"] is False
    assert info["U4_U5_U9_U10_selection_verified"] is False
    assert info["xdma_model_upload_enabled"] is False
