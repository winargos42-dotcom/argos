#ifndef ARGOS_SC4_DRIVER_H
#define ARGOS_SC4_DRIVER_H

#include <stddef.h>
#include <stdint.h>
#include <limits.h>

#define SC4_NPU_COUNT 4
#define SC4_H2C_KNOWN_AXI_ADDR ((uint64_t)0x10000U)
#define SC4_H2C_DIAGNOSTIC_MAX 256
#define SC4_H2C_ID UINT32_C(0x1fc00006)
#define SC4_C2H_ID UINT32_C(0x1fc10006)
#define SC4_FINGERPRINT UINT32_C(0x61a7330d)

typedef struct {
    int user_fd;
    int control_fd;
    char sysfs_path[PATH_MAX];
    char devdir[PATH_MAX];
} sc4_device;

typedef struct {
    uint32_t fingerprint, h2c_id, c2h_id, h2c_status, c2h_status;
    uint32_t slots[SC4_NPU_COUNT][4];
    int h2c_memory_mapped, c2h_memory_mapped;
    int factory_four_way_routing_verified;
    int native_npu_response_verified;
} sc4_status;

typedef struct {
    unsigned int requested;
    unsigned int completed;
    double elapsed_ms;
    uint64_t address;
    int npu_acknowledged;
} sc4_dma_result;

/* Coexists with existing Xilinx xdma kernel module. It does NOT bind PCI. */
int sc4_open(sc4_device *d, const char *sysfs_path, const char *devdir,
             char *err, size_t errlen);
void sc4_close(sc4_device *d);

/* Read-only, bounded 32-bit PCIe MMIO via XDMA's existing char devices. */
int sc4_snapshot(sc4_device *d, sc4_status *s, char *err, size_t errlen);

/* Proven host DMA-only diagnostic, NOT factory NPU model upload.
 * Call only under explicit on-device consent and one-shot proof path.
 * 'stage4' sends exactly 88 manufacturer's initialization bytes.
 * 'zero256' sends exactly 256 zero bytes.
 */
int sc4_diag_h2c(sc4_device *d, const char *kind, const char *proof_file,
                 sc4_dma_result *r, char *err, size_t errlen);

/* Fail closed: factory ASIC select/ACK/AXI map has NOT been recovered. */
int sc4_select_asic(sc4_device *d, unsigned index, char *err, size_t errlen);
int sc4_load_npu_model(sc4_device *d, const char *model_path,
                       unsigned index, char *err, size_t errlen);

#endif
