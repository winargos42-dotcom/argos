# ARGOS SC4 / SPR2801S — new Linux driver-adapter (2026-10-10)

**Implemented and compiled on ThinkPad X230 (Arch Linux, kernel 7.2.8).**

This project is a working **userspace driver and shared C library** for the SC4 factory PCIe endpoint, built **on top of Xilinx's already-installed `xdma.ko` (v2025.2.0)**. It does not unload, rebind, flash, replace or reset that kernel driver or the FPGA. This is the correct division: Xilinx XDMA already owns PCIe and implements scatter/gather DMA; ARGOS adds board-specific identity/logic and the separately reconstructed GTI host protocol.

## Hardware backends

1. **SC4/XDMA:** `bin/argos-sc4 status` and `libargos_sc4.so` read the real PCIe user/control BARs through `/dev/xdma0_user` and `/dev/xdma0_control`. Hardware identity: `10ee:7022 / 1e00:2801`, `sc4_xdma`, fingerprint `0x61a7330d`, H2C `0x1fc00006`, C2H `0x1fc10006`. All four logical BAR0 blocks (0x10, 0x20, 0x30, 0x40) are exposed as **read-only, unassigned logical banks**. There is no claim that these are proved physical chip selectors for U4/U5/U9/U10.
2. **H2C:** The new C driver has a real `pwrite` capability, limited to the **previously tested** 256-byte zero diagnostic or 88-byte manufacturer stage4 command at AXI-MM `0x10000`. A deliberate one-shot proof marker and explicit `--execute` plus environment authorization are required. These tests have already succeeded previously on this physical board via Python; **the new C binary's LIVE DMA path itself has not yet run**. The program does **not** read C2H or claim NPU inference.
3. **GTI native loader:** `src/gtisdk_model.py` recreates every manufacturer `GtiCreateModel` host `ioctl/write` stage for **SHA-256-whitelisted** GNet3/GNet18 factory models (eight stages, 2048-byte chunks, byte-perfect according to earlier captures). Actual `load-native` requires a genuine OEM `/dev/gti2800-N` character device, which is **not installed on the X230**. The code never substitutes XDMA for the OEM ioctl.
4. **Strict native GTI bridge:** `src/gti_pcie_bridge.py` replays native `GTITXN01` records only through a real `/dev/gti2800-0..3`, never XDMA. Native mode now refuses an extra ninth command or any model-loading transcript whose *complete capture SHA-256* is not one of the two independently verified factory SDK recordings (GNet3/GNet18). Validated by `tests/test_gti_pcie_bridge.py`. In the absence of vendor GTI kernel nodes this remains in explicit fail-closed mode; this is not a four-chip factory FIP implementation.

## Build on X230

```sh
cd /home/argos-data/mcp-workspace/projects/spr2801-sc4-driver
make all
make test
bin/argos-sc4 status
python3 src/gtisdk_model.py status
```

Build outputs:
- `bin/argos-sc4` — native C11 executable, no Python runtime required for PCIe status.
- `bin/libargos_sc4.so` — dynamically linkable C driver library.
- `src/driver_bindings.py` — Python ctypes integration for ARGOS processes.
- `src/gtisdk_model.py` — reconstructed factory GTI ioctl/write host model loader.
- `tests/test_*.py` — fake PCIe BAR/control and sparse H2C filesystem regressions.

Compile flags `-O2 -g -std=c11 -Wall -Wextra -Werror -Wconversion -Wshadow -pedantic`; no compiler diagnostics. The build and tests on X230 passed.

### RootGuard live read-only status

ARGOS MCP service user `argos-mcp` lives inside a restricted device namespace without `/dev/xdma*`. The **physical host** has `/dev/xdma0_user`, `/dev/xdma0_control`, `/dev/xdma0_h2c_0`, `/dev/xdma0_c2h_0`, confirmed through `workstation_admin dev_nodes`. To run our new binary **against the actual card**, owner confirmation is required for a RootGuard call executing:

```sh
/home/argos-data/mcp-workspace/projects/spr2801-sc4-driver/bin/argos-sc4 status
```

This command is **read-only** and does NOT install a kernel module, write DMA or change the firmware. Owner confirmation was requested via ARGOS X230 RootGuard under request `1af1e0131f42`; it may expire if not approved within its TTL.

### Important: limitations of today's driver

The underlying vendor factory SC4 mapping from AXI-MM words to proprietary 4-chip SPR2801S FIP `CMD/RDY/CLK/select` remains unknown. Old ARGOS PCIe tests confirmed H2C completion but **no valid per-NPU ACK or output tensor**. No trustworthy inference execution should be reported until actual OEM FIP command routing/ASIC selection is recovered and measured. This user-space driver is a working **SC4/XDMA hardware/GTI host transport component**, not yet a verified end-to-end 4-NPU inference driver.

The factory bitstream remains in nonvolatile memory; nothing here changes it. Kernel hangs, DMA timeout, or PCIe errors are still possible if unknown addresses are used: hence only verified read offsets and one-shot diagnostic payloads are enabled.

## Original references

Xilinx `dma_ip_drivers`, `XDMA/linux-kernel/xdma/{cdev_ctrl.c,cdev_sgdma.c,libxdma.c}`. The Xilinx control device limits each `pread()` to one 32-bit register. Its SGDMA device treats file offset as a physical AXI-MM target address. XDMA does not implement the GTI proprietary `ioctl 0x40044701/02`. Original GTI model host capture data and hardware audit reports are in the owner's X230 recovery tree.
