#!/usr/bin/env python3
"""Noninteractive regression tests for ARGOS/XDMA host driver.

A fake BAR0, standard XDMA control BAR, H2C sparse file and PCI sysfs
files let the real compiled C driver run without accessing actual FPGA.
The program tests ABI parsing, safety guards and one-shot DMA semantics.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
BIN=ROOT/"bin/argos-sc4"

def put32(block,pos,value):
    struct.pack_into("<I",block,pos,value)

class SimulatedSC4(unittest.TestCase):
    def setUp(self):
        self.dir=tempfile.TemporaryDirectory(prefix="argos-sc4-fixture-")
        self.addCleanup(self.dir.cleanup)
        self.base=Path(self.dir.name)
        self.pci=self.base/"pci"
        self.dev=self.base/"dev"
        self.pci.mkdir();self.dev.mkdir()
        for field,value in (
            ("vendor","0x10ee\n"),
            ("device","0x7022\n"),
            ("subsystem_device","0x2801\n"),
        ):
            (self.pci/field).write_text(value)
        self.bar=bytearray(0x100)
        self.bar[:8]=b"sc4_xdma"
        put32(self.bar,0x08,0x61a7330d)
        for i in range(4):
            put32(self.bar,0x18+0x10*i,0x10)
        (self.dev/"xdma0_user").write_bytes(self.bar)
        self.control=bytearray(0x2100)
        put32(self.control,0x0,0x1fc00006)
        put32(self.control,0x1000,0x1fc10006)
        (self.dev/"xdma0_control").write_bytes(self.control)
        (self.dev/"xdma0_h2c_0").write_bytes(bytes(0x10100))
        self.env=os.environ.copy()

    def cli(self,*args,with_env=None):
        env=self.env.copy()
        if with_env:env.update(with_env)
        return subprocess.run(
            [str(BIN),"--sysfs",str(self.pci),"--devdir",str(self.dev),*args],
            capture_output=True,text=True,timeout=5,env=env,
        )

    def test_successfully_opens_and_identifies_factory_pci(self):
        x=self.cli("status")
        self.assertEqual(x.returncode,0,x.stderr)
        j=json.loads(x.stdout)
        self.assertEqual(j["hardware_identity"],"sc4_xdma")
        self.assertEqual(j["fingerprint"],"0x61a7330d")
        self.assertTrue(j["h2c"]["axi_mm"])
        self.assertEqual([a["BAR0_base"] for a in j["logical_banks"]],
                         ["0x10","0x20","0x30","0x40"])
        self.assertEqual([a["words"][2] for a in j["logical_banks"]],["0x00000010"]*4)
        self.assertFalse(j["factory_NPU_command_route_verified"])

    def test_rejects_wrong_subsystem(self):
        (self.pci/"subsystem_device").write_text("0xffff\n")
        x=self.cli("status")
        self.assertNotEqual(x.returncode,0)
        self.assertIn("Wrong PCI",x.stderr)

    def test_rejects_wrong_fingerprint(self):
        put32(self.bar,0x08,0xbadc0ffe)
        (self.dev/"xdma0_user").write_bytes(self.bar)
        x=self.cli("status")
        self.assertNotEqual(x.returncode,0)
        self.assertIn("signature/fingerprint mismatch",x.stderr)

    def test_rejects_streaming_engine(self):
        put32(self.control,0x00,0x1fc08006)
        (self.dev/"xdma0_control").write_bytes(self.control)
        x=self.cli("status")
        self.assertNotEqual(x.returncode,0)

    def test_rejects_short_control_bar(self):
        (self.dev/"xdma0_control").write_bytes(b"abcd")
        x=self.cli("status")
        self.assertNotEqual(x.returncode,0)
        self.assertIn("pread returned",x.stderr)

    def test_does_not_write_bar_during_status(self):
        before=(self.dev/"xdma0_user").read_bytes()
        before2=(self.dev/"xdma0_control").read_bytes()
        x=self.cli("status")
        self.assertEqual(x.returncode,0,x.stderr)
        self.assertEqual((self.dev/"xdma0_user").read_bytes(),before)
        self.assertEqual((self.dev/"xdma0_control").read_bytes(),before2)

    def test_chip_selector_explicitly_not_guessed(self):
        x=self.cli("select-asic","0")
        self.assertEqual(x.returncode,4)
        self.assertIn("ABI UNVERIFIED",x.stderr)
        self.assertEqual(self.cli("select-asic","4").returncode,64)

    def test_write_requires_two_explicit_authorizations(self):
        proof=self.base/"proof"
        first=self.cli("diag-zero256","--execute","--proof",str(proof))
        self.assertNotEqual(first.returncode,0)
        self.assertIn("authorization",first.stderr)
        self.assertFalse(proof.exists())
        second=self.cli("diag-stage4","--proof",str(proof),
                        with_env={"ARGOS_SC4_H2C_DIAGNOSTIC":"I_AUTHORIZE_SINGLE_DMA"})
        self.assertNotEqual(second.returncode,0)
        self.assertFalse(proof.exists())

    def test_one_shot_diagnostic_zero256_only(self):
        proof=self.base/"zero256_once"
        env={"ARGOS_SC4_H2C_DIAGNOSTIC":"I_AUTHORIZE_SINGLE_DMA"}
        x=self.cli("diag-zero256","--execute","--proof",str(proof),with_env=env)
        self.assertEqual(x.returncode,0,x.stderr)
        r=json.loads(x.stdout)
        self.assertEqual(r["dma_completed_bytes"],256)
        self.assertEqual(r["axi"],"0x10000")
        self.assertFalse(r["npu_acknowledged"])
        self.assertEqual((self.dev/"xdma0_h2c_0").read_bytes()[0x10000:0x10100],bytes(256))
        self.assertTrue(proof.exists())
        second=self.cli("diag-zero256","--execute","--proof",str(proof),with_env=env)
        self.assertNotEqual(second.returncode,0)
        self.assertIn("One-shot marker",second.stderr)

    def test_valid_vendor_88byte_command_only(self):
        # The original GTI host stage4 command is 00 02 00 00 followed by zeros.
        proof=self.base/"stage4_once"
        x=self.cli("diag-stage4","--execute","--proof",str(proof),
                   with_env={"ARGOS_SC4_H2C_DIAGNOSTIC":"I_AUTHORIZE_SINGLE_DMA"})
        self.assertEqual(x.returncode,0,x.stderr)
        sent=(self.dev/"xdma0_h2c_0").read_bytes()[0x10000:0x10058]
        self.assertEqual(sent,b"\x00\x02"+bytes(86))
        self.assertEqual(len(sent),88)

    def test_diag_is_not_physical_asic_inference(self):
        self.assertIn("NPU",BIN.read_bytes().decode("latin1"))
        snapshot=json.loads(self.cli("status").stdout)
        self.assertFalse(snapshot["real_NPU_inference_verified"])

    def test_does_not_access_any_c2h_nodes(self):
        # The driver never opens C2H (prior physical C2H returned ETIMEDOUT).
        self.assertFalse((self.dev/"xdma0_c2h_0").exists())
        x=self.cli("status")
        self.assertEqual(x.returncode,0)

if __name__=="__main__":
    unittest.main()
