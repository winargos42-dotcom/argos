# ARGOS SC4 / SPR2801S — native Xilinx XDMA interface

Hardware-facing userspace driver and shared C library for the owner's original
SC4 PCIe FPGA, built on top of the official Xilinx XDMA Linux kernel driver.

This is **production C code**, not a Python fake. Its
`argos_sc4.c` calls `open`/`pread` on real `/dev/xdma0_user` and
`/dev/xdma0_control`; `diag-stage4` can issue **one explicitly authorized**
`pwrite` to `/dev/xdma0_h2c_0` at the proven AXI-MM address `0x10000`.
No MMIO writes, no PCI reset, no JTAG/Flash. The hardware driver keeps
factory FPGA configuration unchanged.

## Build and test

```bash
make -C src/connectivity/argos_sc4 all
make -C src/connectivity/argos_sc4 test
src/connectivity/argos_sc4/bin/argos-sc4 status
```

On the owner's ThinkPad X230, the same C sources compiled and **the binary
was executed on the physical 10ee:7022 PCIe card through RootGuard**:
`status` exited 0 and reported `sc4_xdma`, fingerprint
`0x61a7330d`, XDMA H2C ID `0x1fc00006`, C2H ID
`0x1fc10006`, and four 16-byte BAR0 banks (0x10/20/30/40).

**Native PCIe C driver status is confirmed.** This does not mean NPU
ASIC select/inference is available: the original SC4 FPGA chip-routing
ABI and valid per-NPU acknowledgment remain unrecovered.

### API
- `argos_sc4.h`: `sc4_open`, `sc4_snapshot`, `sc4_diag_h2c`,
  `sc4_select_asic`, `sc4_load_npu_model`.
- `bin/libargos_sc4.so`: linkable library for ARGOS agents.
- `driver_bindings.py`: Python `ctypes` wrapper for **the same C hardware functions**.

Unknown hardware select/load operations fail with `ENOTSUP`,
rather than guessing FPGA registers. Only factory SC4 identity and
engine types are accepted. Four logical banks should **not** be
mistaken for verified physical U4/U5/U9/U10 selectors.

H2C diagnostics require BOTH environment
`ARGOS_SC4_H2C_DIAGNOSTIC=I_AUTHORIZE_SINGLE_DMA` and the
`--execute --proof /absolute/path/never-before-used` flags. A
one-shot marker is created atomically **before** DMA. This is
only for an authorized physical host with the exact pre-verified SC4 FPGA
and AXI address `0x10000` — it cannot load neural weights or
produce a model output on its own.

This code uses no legacy `/dev/gti2800-*` ioctl on XDMA.
`gti_pcie_bridge.py` separately supports only a **genuine
manufacturer GTI char driver**; the custom board's factory FIP
control ABI remains a separate research task.

Reference: [Xilinx/dma_ip_drivers](https://github.com/Xilinx/dma_ip_drivers).
