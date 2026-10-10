# QtStudy / SPR2801S — complete Git tree inventory

Source: https://github.com/ZhengPengqiao/QtStudy/tree/master/%E8%8A%AF%E7%89%87%E5%B9%B3%E5%8F%B0/SPR2801S

2026-10-10: all 4 recursive subtree listings completed with truncated=false.
346 files inventoried by Git blob SHA and byte size. A full path/size/SHA
manifest was saved on physical X230 through ARGOS MCP as
SPR2801_QTSTUDY_MASTER_ALL_FILES_20261010.json.

| Directory | Files |
| --- | ---: |
| 1_0_Demo | 13 |
| doc | 100 |
| include | 2 |
| libs | 231 |

Technical findings:
- 1_0_Demo/spr2801s.cpp calls proprietary GtiCreateModel() and
  GtiEvaluate(). It converts images to 224x224x3 BGR planar data,
  uses GtiTensor and parses returned JSON. It does not implement
  PCIe, XDMA, FPGA MMIO, chip-select, FIP or IRQ.
- include/GTILib.h exposes USB_FTDI, USB_EUSB, PCIE, VIRTUAL,
  USB_NATIVE device types and an API for models and inference;
  it does not describe SC4's factory AXI-MM address map.
- doc/rules/70-gti.rules creates symlinks gti0-0..3 -> gti2800-0..3.
  No kernel driver is included in those rules.
- Other rules are for USB/FTDI, not PCIe 10ee:7022.
- libs contains libGTILibrary.so.4.5.1 and static SDK
  libGTILibrary-static.a.4.5.1, but no source code for the actual
  gti0/gti2800 kernel transport or FPGA FIP switch.
- doc/Modules holds two original GTI .model files, GNet3 FC20
  and GNet18 Dog40, whose native GtiCreateModel host transactions
  ARGOS previously reconstructed byte for byte.
- doc/Data/Image_lite contains five 150528-byte BGR/RGB sample
  frames (224*224*3), ideal for next original GtiEvaluate
  host-side differential test.
- 1_0_Demo/1_0_Demo.pro references -lftd3xx-static but this subtree
  contains the dynamic libftd3xx.so.0.5.21, not a matching
  libftd3xx-static.a; the example build may need adjustment.
- libs/OpenCV is bundled OpenCV x86_64 library and headers.
- Application source and SDK API were inspected; images, videos,
  binary libraries and OpenCV internals were inventoried, not all
  disassembled or viewed frame-by-frame.

The complete tree contains NO source for factory SC4/XC7A35T
FPGA image, four SPR2801S ASIC FIP selector, proprietary
gti2800 kernel module, or GTI ioctl-to-XDMA register mapping.
Do not infer U4/U5/U9/U10 selections from gti2800 device indices.

This audit is evidence for the ongoing ARGOS SC4 C userspace driver,
not evidence of real NPU model inference.
