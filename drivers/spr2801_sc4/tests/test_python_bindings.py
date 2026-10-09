#!/usr/bin/env python3
"""Production libargos_sc4.so accessed from Python via actual compiled C."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from driver_bindings import status,LIB
from test_driver import SimulatedSC4,put32

class BindingsWorkWithNativeCDriver(SimulatedSC4):
    def test_real_compiled_library_loaded(self):
        self.assertTrue(LIB.is_file())
        actual=status(sysfs=self.pci,devdir=self.dev)
        self.assertEqual(actual["backend"],"compiled_libargos_sc4.so")
        self.assertEqual(actual["sc4_signature"],"sc4_xdma")
        self.assertEqual(actual["fingerprint"],"0x61a7330d")
        self.assertEqual(actual["h2c_engine_id"],"0x1fc00006")
        self.assertEqual(actual["c2h_engine_id"],"0x1fc10006")
        self.assertEqual([s["words"][2] for s in actual["logical_slots"]],
                         ["0x00000010"]*4)
        self.assertFalse(actual["physical_inference_verified"])
        self.assertFalse(actual["factory_npu_routing_verified"])

    def test_binding_rejects_wrong_hardware(self):
        (self.pci/"vendor").write_text("0x1234\n")
        with self.assertRaises(OSError):
            status(sysfs=self.pci,devdir=self.dev)

    def test_binding_has_no_side_effects(self):
        before=(self.dev/"xdma0_user").read_bytes()
        result=status(sysfs=self.pci,devdir=self.dev)
        self.assertEqual((self.dev/"xdma0_user").read_bytes(),before)
        self.assertFalse(result["factory_npu_routing_verified"])

if __name__=="__main__":
    unittest.main()
