#!/usr/bin/env python3
"""ARGOS Python binding for compiled libargos_sc4.so on Linux X230.

This layer is a real ctypes call to compiled C; physical MMIO reads are
done by XDMA's /dev/xdma0_user and /dev/xdma0_control on an authorized host.
The default ARGOS MCP service namespace cannot see those device nodes;
running the binding there cannot claim it read hardware. Tests use fake
binary BAR files to exercise the exact production C implementation.
"""
from __future__ import annotations
from contextlib import contextmanager
import ctypes
from pathlib import Path

LIB=Path(__file__).resolve().parents[1]/"bin/libargos_sc4.so"
PATH_MAX=4096

class CDevice(ctypes.Structure):
    _fields_=[("user_fd",ctypes.c_int),("control_fd",ctypes.c_int),
              ("sysfs_path",ctypes.c_char*PATH_MAX),
              ("devdir",ctypes.c_char*PATH_MAX)]

class CStatus(ctypes.Structure):
    _fields_=[
        ("fingerprint",ctypes.c_uint32),
        ("h2c_id",ctypes.c_uint32),("c2h_id",ctypes.c_uint32),
        ("h2c_status",ctypes.c_uint32),("c2h_status",ctypes.c_uint32),
        ("slots",(ctypes.c_uint32*4)*4),
        ("h2c_memory_mapped",ctypes.c_int),
        ("c2h_memory_mapped",ctypes.c_int),
        ("factory_four_way_routing_verified",ctypes.c_int),
        ("native_npu_response_verified",ctypes.c_int),
    ]

def library():
    lib=ctypes.CDLL(str(LIB),use_errno=True)
    lib.sc4_open.argtypes=[ctypes.POINTER(CDevice),ctypes.c_char_p,
                           ctypes.c_char_p,ctypes.c_char_p,ctypes.c_size_t]
    lib.sc4_open.restype=ctypes.c_int
    lib.sc4_snapshot.argtypes=[ctypes.POINTER(CDevice),ctypes.POINTER(CStatus),
                               ctypes.c_char_p,ctypes.c_size_t]
    lib.sc4_snapshot.restype=ctypes.c_int
    lib.sc4_close.argtypes=[ctypes.POINTER(CDevice)]
    lib.sc4_close.restype=None
    return lib

def status(*,sysfs="/sys/bus/pci/devices/0000:04:00.0",devdir="/dev"):
    lib=library()
    dev=CDevice()
    out=CStatus()
    err=ctypes.create_string_buffer(512)
    result=lib.sc4_open(ctypes.byref(dev),str(sysfs).encode(),
                        str(devdir).encode(),err,len(err))
    if result:
        raise OSError(f"X230 PCIe SC4 open: {err.value.decode(errors='replace')}")
    try:
        result=lib.sc4_snapshot(ctypes.byref(dev),ctypes.byref(out),err,len(err))
        if result:
            raise OSError(f"X230 PCIe SC4 inspect: {err.value.decode(errors='replace')}")
    finally:
        lib.sc4_close(ctypes.byref(dev))
    return {
        "backend":"compiled_libargos_sc4.so",
        "sc4_signature":"sc4_xdma",
        "fingerprint":f"0x{out.fingerprint:08x}",
        "h2c_engine_id":f"0x{out.h2c_id:08x}",
        "c2h_engine_id":f"0x{out.c2h_id:08x}",
        "h2c_memory_mapped":bool(out.h2c_memory_mapped),
        "c2h_memory_mapped":bool(out.c2h_memory_mapped),
        "logical_slots":[
            {"index":i,"bar0":hex(0x10+i*0x10),
             "words":[f"0x{out.slots[i][j]:08x}" for j in range(4)],
             "physical_asic_verified":False} for i in range(4)
        ],
        "factory_npu_routing_verified":bool(out.factory_four_way_routing_verified),
        "physical_inference_verified":bool(out.native_npu_response_verified),
    }

if __name__=="__main__":
    import json
    print(json.dumps(status(),indent=2))
