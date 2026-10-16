#!/usr/bin/env python3
"""Reconstructed manufacturer GTI 4.5 host protocol regressions (NO NPU writes)."""
from pathlib import Path
import hashlib
import importlib
import json
import os
import struct
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from gtisdk_model import (
    IOCTL_OPEN, IOCTL_COMMAND, OPCODES, CHUNK,
    GTICharDevice, MissingNativeGTIDriver, UnverifiedFactoryModel,
    inspect_model_metadata, stage6_unverified_for_test, verified_stage6,
    gticreate_stages, gticreate_events, encode_trace,transmit_verified_model
)

class NativeGTIModelTests(unittest.TestCase):
    def setUp(self):
        meta={
            "layer":[
                {"name":"image","operation":"IMAGEREADER"},
                {"name":"cnn","operation":"GTICNN","data offset":300,
                 "data size":88+4096}
            ]
        }
        prefix=json.dumps(meta,separators=(",",":")).encode("ascii")
        self.assertLess(len(prefix),300)
        self.raw=(prefix+bytes(300-len(prefix))+b"\xaa\xaa"+bytes(86)+
                  bytes((i*29+1)&255 for i in range(4096))+
                  b"\x02\x00\x01\x00"+bytes(512))
        self.expected=bytes(2)+bytes((i*29+1)&255 for i in range(4096))[2:]+bytes(4)

    def test_gticnn_metadata_has_exact_declared_start(self):
        meta=inspect_model_metadata(self.raw)
        self.assertEqual(meta["data_offset"],300)
        self.assertEqual(meta["data_size"],4184)
        self.assertEqual(meta["gticnn_name"],"cnn")

    def test_byte_accurate_payload_transform_without_native_approval(self):
        stage6=stage6_unverified_for_test(self.raw)
        self.assertEqual(stage6,self.expected)
        self.assertEqual(len(stage6),4100)
        self.assertEqual(stage6[:2],bytes(2))
        self.assertEqual(stage6[-4:],bytes(4))

    def test_unknown_model_never_allowed_on_native_device(self):
        with self.assertRaises(UnverifiedFactoryModel):
            verified_stage6(self.raw)
        self.assertEqual(len(self.raw),300+4184+4+512)

    def test_host_model_eight_ioctl_stage_codes(self):
        events=list(gticreate_events(self.expected))
        ioctls=[(req,int.from_bytes(data,"little")) for kind,req,data in events if kind==b"I"]
        self.assertEqual(ioctls,[
            (IOCTL_OPEN,0),(IOCTL_COMMAND,0),(IOCTL_COMMAND,1),
            (IOCTL_COMMAND,0),(IOCTL_COMMAND,5),(IOCTL_COMMAND,0),
            (IOCTL_COMMAND,3),(IOCTL_COMMAND,3)
        ])
        self.assertEqual(tuple(op for _,op in ioctls),OPCODES)
        self.assertEqual(len(ioctls),8)
        self.assertEqual(sum(len(d) for k,req,d in events if k==b"W"),
                         0+8+8+64+88+8+4100+32768)

    def test_stage6_transfers_in_original_2048B_chunks(self):
        stages=list(gticreate_stages(self.expected))
        self.assertEqual(stages[4],bytes.fromhex("00 02")+bytes(86))
        self.assertEqual(stages[7],bytes(32768))
        current=-1; per_stage={}
        for kind,req,data in gticreate_events(self.expected):
            if kind==b"I":
                current+=1;per_stage[current]=[]
            else:
                per_stage[current].append(len(data))
                self.assertGreaterEqual(len(data),1)
                self.assertLessEqual(len(data),CHUNK)
        self.assertEqual(per_stage[6],[2048,2048,4])
        self.assertEqual(per_stage[7],[2048]*16)
        self.assertEqual(per_stage[0],[])

    def test_original_gtitxn_v1_serialization(self):
        raw=encode_trace(self.expected)
        self.assertTrue(raw.startswith(b"GTITXN01"))
        parsed=[]
        at=8
        while at<len(raw):
            kind,n,req=struct.unpack_from("<cIQ",raw,at)
            at+=13
            body=raw[at:at+n]
            self.assertEqual(len(body),n)
            parsed.append((kind,n,req))
            at+=n
        self.assertEqual(at,len(raw))
        self.assertEqual(sum(k==b"I" for k,_,_ in parsed),8)
        self.assertEqual(parsed[0],(b"I",4,IOCTL_OPEN))
        self.assertEqual(sum(k==b"W" for k,_,_ in parsed),1+1+1+1+1+3+16)

    def test_refuse_unknown_physical_device(self):
        with self.assertRaises(MissingNativeGTIDriver):
            transmit_verified_model(self.expected,object())

    def test_gtisdk_status_reports_logical_indices_without_claim(self):
        import subprocess
        r=subprocess.run(
            [sys.executable,str(ROOT/"src/gtisdk_model.py"),"status"],
            capture_output=True,text=True,timeout=3)
        self.assertEqual(r.returncode,0,r.stderr)
        j=json.loads(r.stdout)
        self.assertEqual(set(j["logical_gtidevices"]),{"0","1","2","3"})
        self.assertFalse(j["four_asic_mapping_proven"])
        self.assertTrue(j["xdma_is_not_native_gti_ioctl"])

    def test_invalid_model_rejection(self):
        for invalid in [b"",b"123",b'{"layer":[]}' + bytes(300)]:
            with self.assertRaises((ValueError,StopIteration)):
                inspect_model_metadata(invalid)

if __name__=="__main__":
    unittest.main()
