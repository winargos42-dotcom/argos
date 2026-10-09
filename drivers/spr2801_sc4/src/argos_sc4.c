#define _POSIX_C_SOURCE 200809L
#define _FILE_OFFSET_BITS 64
#include "argos_sc4.h"
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

static void sc4_err(char *out, size_t len, const char *fmt, ...) {
    if (!out || !len) return;
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(out, len, fmt, ap);
    va_end(ap);
}

static int path_join(char *out, size_t cap, const char *parent, const char *name) {
    if (!parent || !name) { errno = EINVAL; return -1; }
    int n = snprintf(out, cap, "%s/%s", parent, name);
    if (n < 0 || (size_t)n >= cap) { errno = ENAMETOOLONG; return -1; }
    return 0;
}

static int sysfs_is(const char *sysfs, const char *name, const char *expected,
                    char *err, size_t errlen) {
    char path[PATH_MAX], str[64];
    if (path_join(path, sizeof path, sysfs, name)) return -1;
    FILE *f = fopen(path, "r");
    if (!f) {
        sc4_err(err, errlen, "PCI identity %s: %s", name, strerror(errno));
        return -1;
    }
    if (!fgets(str, sizeof str, f)) {
        fclose(f);
        errno = EIO;
        sc4_err(err, errlen, "Cannot read PCI identity %s", name);
        return -1;
    }
    fclose(f);
    str[strcspn(str, "\r\n")] = '\0';
    if (strcmp(str, expected)) {
        sc4_err(err, errlen, "Wrong PCI %s: expected %s, found %s", name, expected, str);
        errno = ENODEV;
        return -1;
    }
    return 0;
}

static int read32(int fd, off_t address, uint32_t *out, char *err, size_t errlen) {
    /* The Xilinx XDMA user cdev deliberately returns at most 4 bytes
       per pread(), even when the count requested is larger. */
    unsigned char b[4];
    ssize_t n = pread(fd, b, sizeof b, address);
    if (n != 4) {
        if (n >= 0) errno = EIO;
        sc4_err(err, errlen, "PCI register 0x%llx: pread returned %zd: %s",
                (unsigned long long)address, n, strerror(errno));
        return -1;
    }
    *out = (uint32_t)b[0] | ((uint32_t)b[1] << 8) |
           ((uint32_t)b[2] << 16) | ((uint32_t)b[3] << 24);
    return 0;
}

void sc4_close(sc4_device *d) {
    if (!d) return;
    if (d->user_fd >= 0) { close(d->user_fd); d->user_fd = -1; }
    if (d->control_fd >= 0) { close(d->control_fd); d->control_fd = -1; }
}

int sc4_open(sc4_device *d, const char *sysfs_path, const char *devdir,
             char *err, size_t errlen) {
    char path[PATH_MAX];
    if (!d || !sysfs_path || !devdir) {
        errno = EINVAL;
        sc4_err(err, errlen, "Invalid device parameters");
        return -1;
    }
    memset(d, 0, sizeof *d);
    d->user_fd = d->control_fd = -1;
    if (snprintf(d->sysfs_path, sizeof d->sysfs_path, "%s", sysfs_path) >=
        (int)sizeof d->sysfs_path ||
        snprintf(d->devdir, sizeof d->devdir, "%s", devdir) >=
        (int)sizeof d->devdir) {
        errno = ENAMETOOLONG;
        sc4_err(err, errlen, "Device path too long");
        return -1;
    }
    if (sysfs_is(sysfs_path, "vendor", "0x10ee", err, errlen) ||
        sysfs_is(sysfs_path, "device", "0x7022", err, errlen) ||
        sysfs_is(sysfs_path, "subsystem_device", "0x2801", err, errlen))
        return -1;
    if (path_join(path, sizeof path, devdir, "xdma0_user")) return -1;
    d->user_fd = open(path, O_RDONLY | O_CLOEXEC | O_NOFOLLOW);
    if (d->user_fd < 0) {
        sc4_err(err, errlen, "Cannot open %s: %s", path, strerror(errno));
        return -1;
    }
    if (path_join(path, sizeof path, devdir, "xdma0_control")) {
        sc4_close(d);
        return -1;
    }
    d->control_fd = open(path, O_RDONLY | O_CLOEXEC | O_NOFOLLOW);
    if (d->control_fd < 0) {
        sc4_err(err, errlen, "Cannot open %s: %s", path, strerror(errno));
        sc4_close(d);
        return -1;
    }
    return 0;
}

int sc4_snapshot(sc4_device *d, sc4_status *s, char *err, size_t errlen) {
    if (!d || !s || d->control_fd < 0 || d->user_fd < 0) {
        errno = EINVAL;
        sc4_err(err, errlen, "SC4 device is not open");
        return -1;
    }
    memset(s, 0, sizeof *s);
    uint32_t id0, id1;
    if (read32(d->user_fd, 0, &id0, err, errlen) ||
        read32(d->user_fd, 4, &id1, err, errlen) ||
        read32(d->user_fd, 8, &s->fingerprint, err, errlen))
        return -1;
    if (id0 != UINT32_C(0x5f346373) ||
        id1 != UINT32_C(0x616d6478) ||
        s->fingerprint != SC4_FINGERPRINT) {
        errno = ENODEV;
        sc4_err(err, errlen, "Factory SC4 BAR0 signature/fingerprint mismatch");
        return -1;
    }
    if (read32(d->control_fd, 0, &s->h2c_id, err, errlen) ||
        read32(d->control_fd, 0x1000, &s->c2h_id, err, errlen) ||
        read32(d->control_fd, 0x40, &s->h2c_status, err, errlen) ||
        read32(d->control_fd, 0x1040, &s->c2h_status, err, errlen))
        return -1;
    if (s->h2c_id != SC4_H2C_ID || s->c2h_id != SC4_C2H_ID) {
        errno = ENODEV;
        sc4_err(err, errlen, "Unexpected H2C/C2H hardware engine IDs");
        return -1;
    }
    s->h2c_memory_mapped = (s->h2c_id & UINT32_C(0x8000)) == 0;
    s->c2h_memory_mapped = (s->c2h_id & UINT32_C(0x8000)) == 0;
    if (!s->h2c_memory_mapped || !s->c2h_memory_mapped) {
        errno = ENOTSUP;
        sc4_err(err, errlen, "Not the proven XDMA AXI Memory-Mapped configuration");
        return -1;
    }
    for (unsigned slot = 0; slot < SC4_NPU_COUNT; slot++) {
        for (unsigned word = 0; word < 4; word++) {
            off_t address = (off_t)(0x10 + slot * 0x10 + word * 4);
            if (read32(d->user_fd, address, &s->slots[slot][word], err, errlen))
                return -1;
        }
    }
    /* Four 16-byte logical banks do NOT prove U4/U5/U9/U10 ASIC routing. */
    s->factory_four_way_routing_verified = 0;
    s->native_npu_response_verified = 0;
    return 0;
}

static double elapsed_milliseconds(const struct timespec *before,
                                   const struct timespec *after) {
    return (double)(after->tv_sec - before->tv_sec) * 1000.0 +
           (double)(after->tv_nsec - before->tv_nsec) / 1000000.0;
}

int sc4_diag_h2c(sc4_device *d, const char *kind, const char *proof_file,
                 sc4_dma_result *r, char *err, size_t errlen) {
    if (!d || !r || !kind || !proof_file) {
        errno = EINVAL;
        sc4_err(err, errlen, "Missing diagnostic parameters");
        return -1;
    }
    const char *allow = getenv("ARGOS_SC4_H2C_DIAGNOSTIC");
    if (!allow || strcmp(allow, "I_AUTHORIZE_SINGLE_DMA")) {
        errno = EPERM;
        sc4_err(err, errlen, "Hardware DMA requires explicit one-shot authorization");
        return -1;
    }
    if (proof_file[0] != '/' || strstr(proof_file, "/dev/") ||
        strstr(proof_file, "/sys/") || strstr(proof_file, "/proc/")) {
        errno = EINVAL;
        sc4_err(err, errlen, "Proof marker must be an ordinary absolute file path");
        return -1;
    }
    unsigned char payload[SC4_H2C_DIAGNOSTIC_MAX] = {0};
    size_t length = 0;
    if (!strcmp(kind, "zero256")) length = 256;
    else if (!strcmp(kind, "stage4")) {
        length = 88;
        payload[1] = 2;
    } else {
        errno = EINVAL;
        sc4_err(err, errlen, "Only previously tested zero256/stage4 payloads supported");
        return -1;
    }

    sc4_status status;
    if (sc4_snapshot(d, &status, err, errlen)) return -1;
    memset(r, 0, sizeof *r);
    r->requested = (unsigned)length;
    r->address = SC4_H2C_KNOWN_AXI_ADDR;

    /* Atomic marker prevents automatic retries even after process crash. */
    int marker = open(proof_file, O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC | O_NOFOLLOW, 0600);
    if (marker < 0) {
        sc4_err(err, errlen, "One-shot marker already exists/unwritable: %s", strerror(errno));
        return -1;
    }
    const char *reason = "ARGOS: ONE H2C DMA attempted; NOT NPU inference.\n";
    (void)write(marker, reason, strlen(reason));
    close(marker);

    char path[PATH_MAX];
    if (path_join(path, sizeof path, d->devdir, "xdma0_h2c_0")) return -1;
    int fd = open(path, O_WRONLY | O_CLOEXEC | O_NOFOLLOW);
    if (fd < 0) {
        sc4_err(err, errlen, "H2C open failed: %s", strerror(errno));
        return -1;
    }
    struct timespec t0, t1;
    (void)clock_gettime(CLOCK_MONOTONIC, &t0);
    ssize_t written = pwrite(fd, payload, length, (off_t)SC4_H2C_KNOWN_AXI_ADDR);
    (void)clock_gettime(CLOCK_MONOTONIC, &t1);
    int saved_errno = errno;
    close(fd);
    r->elapsed_ms = elapsed_milliseconds(&t0, &t1);
    if (written != (ssize_t)length) {
        if (written >= 0) saved_errno = EIO;
        errno = saved_errno;
        sc4_err(err, errlen, "H2C returned %zd/%zu: %s",
                written, length, strerror(errno));
        return -1;
    }
    r->completed = (unsigned)written;
    r->npu_acknowledged = 0;
    return 0;
}

int sc4_select_asic(sc4_device *d, unsigned index, char *err, size_t errlen) {
    (void)d;
    if (index >= SC4_NPU_COUNT) {
        errno = EINVAL;
        sc4_err(err, errlen, "Logical ASIC index is not 0..3");
        return -1;
    }
    errno = ENOTSUP;
    sc4_err(err, errlen, "Factory FIP ASIC-select AXI register map unavailable; no guessed writes");
    return -1;
}

int sc4_load_npu_model(sc4_device *d, const char *model_path,
                       unsigned index, char *err, size_t errlen) {
    (void)model_path;
    return sc4_select_asic(d, index, err, errlen);
}
