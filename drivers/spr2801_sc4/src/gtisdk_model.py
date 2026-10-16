#!/usr/bin/env python3
"""Factory GTI2801 host model loader for ARGOS SC4 driver-adapter.

Reconstructed against original Gyrfalcon GTI SDK v4.5.1 for GNet3/GNet18.
This bridge talks ONLY to a genuine manufacturer's /dev/gti2800-{0..3}
CHARACTER driver; the existing Xilinx /dev/xdma* is INCOMPATIBLE with
manufacturer's ioctls and is deliberately NEVER opened here.

The entire native GtiCreateModel host sequence (8 ioctl stages and
2,048-byte write framing) is known. Only SHA-approved, exact manufacturer
model files are accepted. Selecting a logical index is not proof which
physical U4/U5/U9/U10 ASIC is selected by the factory SC4.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import struct

IOCTL_OPEN = 0x40044701
IOCTL_COMMAND = 0x40044702
MAGIC = b"GTITXN01"
CAPTURE_ENTRY = struct.Struct("<cIQ")
OPCODES = (0, 0, 1, 0, 5, 0, 3, 3)
CHUNK = 2048
GTICNN_DATA_HEADER = 88

PROFILES = {
    "gti_gnet3_fc20_2801": {
        "model_sha256": "ecb2a45465d133bd7187502f002d2958cc7b5615f4bd34d911df8bcca33957d1",
        "stage6_sha256": "f8996a47f05bdbc8f7631977d91a8d6db07a2d95a5ac871209d9b37df627d203",
        "model_bytes": 9282331,
        "data_offset": 3166,
        "data_size": 2779532,
        "payload_bytes": 2779448,
    },
    "gti_gnet18_dog40_2801": {
        "model_sha256": "dd15298ae4dae9beaf4aa95dbf4c33152162374419da1b7f59d0f638d2315d6c",
        "stage6_sha256": "84d3ba34481cde505366e1cd42eeac38cd39486e98b61f84cbe610e856928649",
        "model_bytes": 4689239,
        "data_offset": 2070,
        "data_size": 4601948,
        "payload_bytes": 4601864,
    },
}

class UnverifiedFactoryModel(ValueError):
    pass

class MissingNativeGTIDriver(RuntimeError):
    pass

def inspect_model_metadata(model: bytes) -> dict:
    if not isinstance(model, bytes) or len(model) < 200 or len(model) > 32 * 1024 * 1024:
        raise ValueError("Expected regular factory model bytes")
    # The original manufacturer stores an ASCII JSON prefix followed by
    # arbitrary binary. latin1 is reversible, allowing byte-exact offsets.
    header = model[:min(len(model), 1024 * 1024)].decode("latin1")
    document, chars_consumed = json.JSONDecoder().raw_decode(header)
    layers = document.get("layer") if isinstance(document, dict) else None
    if not isinstance(layers, list):
        raise ValueError("Manufacturer model has no layer list")
    gticnn = next(
        (l for l in layers if isinstance(l, dict) and l.get("operation") == "GTICNN"),
        None,
    )
    if gticnn is None:
        raise ValueError("Model contains no GTICNN layer")
    offset, size = gticnn.get("data offset"), gticnn.get("data size")
    if type(offset) is not int or type(size) is not int:
        raise ValueError("GTICNN offsets must be integers")
    if (not chars_consumed <= offset < len(model)
        or size <= GTICNN_DATA_HEADER or offset + size > len(model)):
        raise ValueError("GTICNN declares invalid payload boundaries")
    return {
        "data_offset": offset, "data_size": size,
        "gticnn_name": gticnn.get("name"), "json_header_bytes": chars_consumed,
    }

def stage6_unverified_for_test(model: bytes) -> bytes:
    """Structure-only transform, WITHOUT approval to send to live NPU."""
    meta = inspect_model_metadata(model)
    begin = meta["data_offset"] + GTICNN_DATA_HEADER
    end = meta["data_offset"] + meta["data_size"]
    data = bytearray(model[begin:end])
    data[:2] = b"\x00\x00"
    data += b"\x00\x00\x00\x00"
    return bytes(data)

def verified_stage6(model: bytes) -> tuple[str, bytes]:
    digest = hashlib.sha256(model).hexdigest()
    for profile, manifest in PROFILES.items():
        if digest != manifest["model_sha256"] or len(model) != manifest["model_bytes"]:
            continue
        metadata = inspect_model_metadata(model)
        if (metadata["data_offset"] != manifest["data_offset"] or
            metadata["data_size"] != manifest["data_size"]):
            raise UnverifiedFactoryModel("Manufacturer model GTICNN metadata mismatch")
        data = stage6_unverified_for_test(model)
        if len(data) != manifest["payload_bytes"] or hashlib.sha256(data).hexdigest() != manifest["stage6_sha256"]:
            raise UnverifiedFactoryModel("Model payload differs from native vendor SDK capture")
        return profile, data
    raise UnverifiedFactoryModel(
        "Unknown model SHA256. Nothing sent to hardware. "
        "Capture original GTI SDK sequence for this exact model first."
    )

def gticreate_stages(stage6: bytes):
    # These exact bytes were independently observed for two OEM profiles.
    return (
        b"",
        bytes(8),
        bytes(8),
        bytes(64),
        b"\x00\x02" + bytes(86),
        bytes(8),
        stage6,
        bytes(32768),
    )

def gticreate_events(stage6: bytes):
    for index, payload in enumerate(gticreate_stages(stage6)):
        req = IOCTL_OPEN if index == 0 else IOCTL_COMMAND
        yield b"I", req, struct.pack("<I", OPCODES[index])
        for pos in range(0, len(payload), CHUNK):
            yield b"W", 0, payload[pos:pos+CHUNK]

def encode_trace(stage6: bytes) -> bytes:
    records=[MAGIC]
    for kind,req,data in gticreate_events(stage6):
        if kind == b"W" and not 1 <= len(data) <= CHUNK:
            raise ValueError("GTI SDK chunk size invalid")
        records.append(CAPTURE_ENTRY.pack(kind, len(data), req))
        records.append(data)
    return b"".join(records)

class GTICharDevice:
    """The OEM driver only, never the generic Xilinx XDMA interface."""
    def __init__(self, index: int):
        if type(index) is not int or index not in range(4):
            raise ValueError("Device index must be 0..3")
        self.index = index
        self.path = Path(f"/dev/gti2800-{index}")
        try:
            st = self.path.stat()
        except FileNotFoundError as exc:
            raise MissingNativeGTIDriver(
                f"{self.path} not installed; unable to perform physical NPU load"
            ) from exc
        if not stat.S_ISCHR(st.st_mode):
            raise MissingNativeGTIDriver(
                f"{self.path} is not a character device — refusing emulation"
            )
        self.fd = os.open(self.path, os.O_RDWR | os.O_CLOEXEC)
    def ioctl(self, request: int, opcode: int):
        if request not in (IOCTL_OPEN, IOCTL_COMMAND) or not 0 <= opcode <= 5:
            raise ValueError("Unexpected GTI SDK ioctl command")
        fcntl.ioctl(self.fd, request, struct.pack("<I", opcode))
    def write(self, data: bytes):
        n = os.write(self.fd, data)
        if n != len(data):
            raise IOError(f"GTI SDK hardware short write: {n}/{len(data)}")
    def close(self):
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1
    def __enter__(self):
        return self
    def __exit__(self, *_):
        self.close()

def transmit_verified_model(stage6: bytes, backend) -> dict:
    """Call only with an independently genuine OEM GTI device backend."""
    if not isinstance(backend, GTICharDevice):
        # Test helper can call gticreate_events without using hardware.
        raise MissingNativeGTIDriver("Native manufacturer char driver required")
    count = 0
    total = 0
    for kind,req,payload in gticreate_events(stage6):
        if kind == b"I":
            backend.ioctl(req, int.from_bytes(payload,"little"))
        else:
            backend.write(payload)
            count += 1
            total += len(payload)
    return {
        "native_char_device": str(backend.path),
        "sdk_ioctl_count": 8,
        "sdk_write_count": count,
        "sdk_payload_bytes": total,
        "completion_verified": False,
        "physical_npu_result_verified": False,
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("action",choices=["status","build","load-native"])
    p.add_argument("--model",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--index",type=int,default=0)
    p.add_argument("--execute",action="store_true")
    args=p.parse_args()
    if args.action=="status":
        result={
            "logical_gtidevices":{
                str(i):{"path":f"/dev/gti2800-{i}",
                        "present":Path(f"/dev/gti2800-{i}").exists()}
                for i in range(4)
            },
            "xdma_is_not_native_gti_ioctl":True,
            "four_asic_mapping_proven":False,
        }
        print(json.dumps(result,indent=2))
        return
    if args.model is None:
        p.error("--model required for build and load-native")
    raw=args.model.read_bytes()
    profile,stage6=verified_stage6(raw)
    if args.action=="build":
        if args.output is None:
            p.error("--output required")
        if args.output.is_symlink() or str(args.output.resolve()).startswith(("/dev/","/sys/","/proc/")):
            p.error("Output destination must be a regular local file, not a device")
        data=encode_trace(stage6)
        args.output.write_bytes(data)
        print(json.dumps({
            "profile":profile,"capture_sha256":hashlib.sha256(data).hexdigest(),
            "trace_bytes":len(data),"stage6_bytes":len(stage6),
            "physical_npu_inference_verified":False
        }))
        return
    if not args.execute: p.error("load-native requires --execute")
    with GTICharDevice(args.index) as gti:
        receipt=transmit_verified_model(stage6,gti)
    print(json.dumps({"profile":profile,**receipt},indent=2))

if __name__=="__main__":
    main()
