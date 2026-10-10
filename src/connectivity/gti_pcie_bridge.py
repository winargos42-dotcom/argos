#!/usr/bin/env python3
"""ARGOS SPR2801 GTI host protocol bridge reconstructed from SDK 4.5.1 traces.

GTITXN01 captures contain actual host ioctl/write operations but synthetic
READ requests. No original GTI kernel driver /dev/gti2800-* is installed
on the X230; XDMA is a DIFFERENT interface. This code deliberately cannot
redirect the proprietary ioctl stream into unverified SC4 FPGA registers.

Supported: strict host transactions, native GTI char-device backend if
genuine device exists, fake backend for tests, indices 0..3 (NOT proven
to correspond to U4/U5/U9/U10), read-only XDMA/PCI preflight.
No BAR write, no DMA upload, no JTAG, no flash, no fabricated inference.
"""
from __future__ import annotations
from dataclasses import dataclass,field
from pathlib import Path
from typing import Protocol
import argparse,fcntl,hashlib,json,os,struct

MAGIC=b"GTITXN01"
ENTRY=struct.Struct("<cIQ")
IOCTL_OPEN=0x40044701
IOCTL_COMMAND=0x40044702
IOCTL_OTHER=0x40044704
ALLOWED_IOCTL={IOCTL_OPEN,IOCTL_COMMAND,IOCTL_OTHER}
MAX_CHUNK=2048
MAX_EVENTS=12000
MAX_TOTAL=24*1024*1024
MODEL_OPCODES=(0,0,1,0,5,0,3,3)
MODEL_STAGE4=bytes.fromhex("00 02 00 00")+bytes(84)
# Byte-exact original GTI SDK v4.5.1 GtiCreateModel captures.
# Only these two known factory model loads may run on a genuine GTI
# kernel char device. Never authorize an unknown custom model by shape.
VERIFIED_MODEL_GTITXN_SHA256=frozenset({
    "9978890e0accc21e0a6e87f96f6fd38ae07604d26bd0835dae8104e91cbd51ec",  # GNet3
    "22fe1a77530f8f4ad9d51bf2149f024f18711b144158e0e3e839bd8396cc1f81",  # GNet18
})

class ProtocolError(ValueError):
    pass

class FactoryABIMissing(RuntimeError):
    pass

@dataclass(frozen=True)
class Record:
    kind:bytes
    request:int
    payload:bytes=b""
    requested_length:int=0

    @property
    def length(self):
        return self.requested_length if self.kind==b"R" else len(self.payload)

def parse_trace(raw:bytes)->list[Record]:
    if not isinstance(raw,bytes) or not raw.startswith(MAGIC):
        raise ProtocolError("Not original GTI SDK GTITXN01 capture format")
    if len(raw)>MAX_TOTAL:
        raise ProtocolError("Trace too large")
    output=[];pos=len(MAGIC);size_sum=0
    while pos<len(raw):
        if len(raw)-pos<ENTRY.size:raise ProtocolError("Truncated record")
        kind,size,req=ENTRY.unpack_from(raw,pos)
        pos+=ENTRY.size
        if kind==b"I":
            if size!=4 or req not in ALLOWED_IOCTL:
                raise ProtocolError("Unexpected ioctl request/length")
        elif kind in (b"W",b"R"):
            if req!=0 or not 0<size<=MAX_CHUNK:
                raise ProtocolError("Unexpected GTI read/write header")
        else:raise ProtocolError("Unknown record type")
        if kind==b"R":
            output.append(Record(kind,0,b"",size))
        else:
            if size>len(raw)-pos:raise ProtocolError("Truncated ioctl/write data")
            output.append(Record(kind,req,raw[pos:pos+size],0))
            pos+=size
        size_sum+=size
        if len(output)>MAX_EVENTS or size_sum>MAX_TOTAL:
            raise ProtocolError("Transaction safety limit exceeded")
    if not output or output[0].kind!=b"I":
        raise ProtocolError("No GTI opening ioctl")
    return output

def validate_model_load(records:list[Record],*,allow_postload:bool=False)->list[dict]:
    """Validate exactly 8 load stages for hardware; fake tests may have a tail.

    Do NOT approve a real GTI ioctl replay based on a valid eight-stage
    prefix followed by arbitrary extra commands. The old prefix-only
    validator could allow a ninth unchecked ioctl through replay().
    """
    stages=[]
    for r in records:
        if r.kind==b"I":
            if len(stages)>=8:
                if allow_postload:
                    break  # test-only synthetic result, never native replay
                raise ProtocolError("Unverified extra GTI command after model load")
            stages.append({"ioctl":r.request,"opcode":int.from_bytes(r.payload,"little"),
                           "data":bytearray(),"writes":[]})
        elif r.kind==b"W" and 0<len(stages)<=8:
            stages[-1]["data"].extend(r.payload)
            stages[-1]["writes"].append(len(r.payload))
        elif r.kind==b"R":
            raise ProtocolError("Unexpected read during model load")
        else:
            raise ProtocolError("Unexpected event outside GTI model stages")
    if len(stages)!=8 or tuple(x["opcode"] for x in stages)!=MODEL_OPCODES:
        raise ProtocolError("Unexpected model-load command order")
    if stages[0]["ioctl"]!=IOCTL_OPEN or any(x["ioctl"]!=IOCTL_COMMAND for x in stages[1:]):
        raise ProtocolError("Wrong host ioctl framing")
    constants={0:b"",1:bytes(8),2:bytes(8),3:bytes(64),4:MODEL_STAGE4,5:bytes(8),7:bytes(32768)}
    for i,body in constants.items():
        if bytes(stages[i]["data"])!=body:
            raise ProtocolError(f"Unexpected stage {i} payload")
    blob=stages[6]["data"]
    if not 2048<len(blob)<=16*1024*1024 or blob[:2]!=bytes(2) or blob[-4:]!=bytes(4):
        raise ProtocolError("Unknown GTICNN model block layout")
    for st in stages:
        lens=st["writes"]
        if lens and (lens[:-1]!=[2048]*(len(lens)-1) or not 0<lens[-1]<=2048):
            raise ProtocolError("Wrong original GTI 2048-byte write framing")
    return [{"stage":i,"opcode":s["opcode"],"ioctl":hex(s["ioctl"]),
             "bytes":len(s["data"]),"writes":len(s["writes"]),
             "sha256":hashlib.sha256(s["data"]).hexdigest()} for i,s in enumerate(stages)]

class Backend(Protocol):
    real_npu_device:bool
    def ioctl(self,req:int,opcode:int)->None: ...
    def write(self,body:bytes)->None: ...
    def read(self,size:int)->bytes: ...
    def close(self)->None: ...

class NativeGTIDevice:
    """A REAL manufacturer's GTI char device only, NOT /dev/xdma0*."""
    real_npu_device=True
    def __init__(self,index:int):
        if type(index)!=int or index not in range(4):
            raise ValueError("GTI logical index must be 0..3")
        self.index=index
        self.path=Path(f"/dev/gti2800-{index}")
        if not self.path.exists():
            raise FactoryABIMissing(
                f"{self.path} absent: GTI2800 kernel driver unavailable. "
                "Generic XDMA cannot emulate vendor ioctl/FIP.")
        self.fd=os.open(str(self.path),os.O_RDWR|os.O_CLOEXEC)
        self.closed=False
    def ioctl(self,req,opcode):
        if self.closed:raise RuntimeError("Device already closed")
        if req not in ALLOWED_IOCTL or type(opcode)!=int or not 0<=opcode<=0xffffffff:
            raise ProtocolError("Unrecognized GTI ioctl")
        fcntl.ioctl(self.fd,req,struct.pack("<I",opcode))
    def write(self,body):
        if self.closed:raise RuntimeError("Device already closed")
        if type(body)!=bytes or not 0<len(body)<=MAX_CHUNK:
            raise ProtocolError("GTI write length invalid")
        n=os.write(self.fd,body)
        if n!=len(body):raise IOError(f"GTI short write {n}/{len(body)}")
    def read(self,size):
        if self.closed:raise RuntimeError("Device already closed")
        if type(size)!=int or not 0<size<=MAX_CHUNK:
            raise ProtocolError("GTI read length invalid")
        data=os.read(self.fd,size)
        if len(data)!=size:raise IOError(f"GTI short read {len(data)}/{size}")
        return data
    def close(self):
        if not self.closed:os.close(self.fd);self.closed=True
    def __enter__(self):return self
    def __exit__(self,*_):self.close()

class FakeGTIDevice:
    """Tests only; fake output must NEVER be counted as NPU inference."""
    real_npu_device=False
    def __init__(self):
        self.ioctls=[];self.writes=[];self.read_requests=[]
    def ioctl(self,req,opcode):self.ioctls.append((req,opcode))
    def write(self,body):self.writes.append(bytes(body))
    def read(self,size):
        self.read_requests.append(size)
        return bytes(size)
    def close(self):pass

@dataclass
class ReplayResult:
    mode:str
    logical_device:int|None
    events:int
    ioctl_calls:int
    writes:int
    sent_bytes:int
    read_calls:int
    read_bytes:bytes=field(repr=False)
    def evidence(self):
        return {"mode":self.mode,"logical_device":self.logical_device,
                "events":self.events,"ioctls":self.ioctl_calls,
                "writes":self.writes,"sent_bytes":self.sent_bytes,
                "read_calls":self.read_calls,"received_bytes":len(self.read_bytes),
                "read_sha256":hashlib.sha256(self.read_bytes).hexdigest() if self.read_bytes else None,
                "read_from_native_gti_driver":self.mode=="NATIVE_GTI" and bool(self.read_bytes),
                "physical_inference_verified":False,
                "asic_package_mapping_verified":False}

def replay(records:list[Record],backend:Backend,*,logical_index:int|None=None)->ReplayResult:
    native=backend.real_npu_device
    validate_model_load(records,allow_postload=not native)
    if native:
        # The genuine vendor driver can move physical NPU commands. Require
        # a byte-exact capture of a factory model and refuse any extended
        # evaluation/read stages until independently reviewed.
        canonical=bytearray(MAGIC)
        for r in records:
            if r.kind not in (b"I",b"W") or not isinstance(r.payload,bytes):
                raise ProtocolError("Native device accepts model load records only")
            canonical.extend(ENTRY.pack(r.kind,len(r.payload),r.request))
            canonical.extend(r.payload)
        if hashlib.sha256(canonical).hexdigest() not in VERIFIED_MODEL_GTITXN_SHA256:
            raise FactoryABIMissing("Original factory GTI SDK model-load SHA256 not verified")
    n_io=n_w=n_r=total=0;out=bytearray()
    for r in records:
        if r.kind==b"I":
            backend.ioctl(r.request,int.from_bytes(r.payload,"little"))
            n_io+=1
        elif r.kind==b"W":
            backend.write(r.payload)
            n_w+=1;total+=len(r.payload)
        else:
            val=backend.read(r.length)
            if len(val)!=r.length:raise IOError("Short GTI result")
            n_r+=1;out.extend(val)
    return ReplayResult("NATIVE_GTI" if backend.real_npu_device else "FAKE_TEST",
                        logical_index,len(records),n_io,n_w,total,n_r,bytes(out))

def sc4_status_read_only():
    dev=Path("/sys/bus/pci/devices/0000:04:00.0")
    ids={}
    for field in ("vendor","device","subsystem_device"):
        try:ids[field]=(dev/field).read_text().strip()
        except OSError:ids[field]=None
    ids["pci_identity_verified"]=(ids["vendor"],ids["device"],ids["subsystem_device"])==("0x10ee","0x7022","0x2801")
    ids["native_gti_devices"]={str(i):Path(f"/dev/gti2800-{i}").exists() for i in range(4)}
    ids["xdma_present"]=all(Path(p).exists() for p in ("/dev/xdma0_user","/dev/xdma0_control","/dev/xdma0_h2c_0","/dev/xdma0_c2h_0"))
    ids["xdma_to_GTIFIP_driver_map_verified"]=False
    ids["U4_U5_U9_U10_selection_verified"]=False
    ids["xdma_model_upload_enabled"]=False
    return ids

if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--status",action="store_true")
    cli.add_argument("--trace",type=Path)
    cli.add_argument("--index",type=int,default=0)
    cli.add_argument("--native-driver",action="store_true",help="Requires genuine GTI driver; does NOT work via xdma")
    x=cli.parse_args()
    if x.status or x.trace is None:print(json.dumps(sc4_status_read_only(),indent=2))
    else:
        rec=parse_trace(x.trace.read_bytes())
        print(json.dumps({"model_stages":validate_model_load(rec)},indent=2))
        if x.native_driver:
            with NativeGTIDevice(x.index) as device:out=replay(rec,device,logical_index=x.index)
        else:out=replay(rec,FakeGTIDevice(),logical_index=x.index)
        print(json.dumps(out.evidence(),indent=2))
