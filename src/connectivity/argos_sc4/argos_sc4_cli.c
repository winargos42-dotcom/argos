#define _POSIX_C_SOURCE 200809L
#include "argos_sc4.h"
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void usage(const char *name) {
    fprintf(stderr,
        "ARGOS SC4 XDMA driver-adapter for factory XC7A35T / 4 SPR2801S\n"
        "Usage: %s [--sysfs DIR] [--devdir DIR] status\n"
        "       %s [--sysfs DIR] [--devdir DIR] select-asic N\n"
        "       %s [--sysfs DIR] [--devdir DIR] diag-stage4 --execute --proof /ABS/ONE-SHOT\n"
        "       %s [--sysfs DIR] [--devdir DIR] diag-zero256 --execute --proof /ABS/ONE-SHOT\n"
        "\nWARNING: diagnostic DMA only! Requires ARGOS_SC4_H2C_DIAGNOSTIC="
        "I_AUTHORIZE_SINGLE_DMA in the environment.\n"
        "The hardware ASIC routing command ABI remains UNKNOWN; the driver never "
        "invents NPU ACK or model execution.\n",
        name, name, name, name);
}

static void status_json(const sc4_status *s) {
    printf("{\n"
           "  \"driver\": \"argos-sc4-xdma-bridge-v1\",\n"
           "  \"hardware_identity\": \"sc4_xdma\",\n"
           "  \"fingerprint\": \"0x%08x\",\n"
           "  \"h2c\": {\"id\": \"0x%08x\", \"status\": \"0x%08x\", \"axi_mm\": %s},\n"
           "  \"c2h\": {\"id\": \"0x%08x\", \"status\": \"0x%08x\", \"axi_mm\": %s},\n"
           "  \"logical_banks\": [\n",
           s->fingerprint,s->h2c_id,s->h2c_status,
           s->h2c_memory_mapped ? "true":"false",
           s->c2h_id,s->c2h_status,
           s->c2h_memory_mapped ? "true":"false");
    for (unsigned i=0;i<SC4_NPU_COUNT;i++) {
        printf("    {\"index\":%u,\"BAR0_base\":\"0x%02x\","
               "\"words\":[\"0x%08x\",\"0x%08x\",\"0x%08x\",\"0x%08x\"],"
               "\"physical_asic_mapping_verified\":false}%s\n",
               i,0x10+i*0x10,s->slots[i][0],s->slots[i][1],
               s->slots[i][2],s->slots[i][3],
               i==SC4_NPU_COUNT-1 ? "" : ",");
    }
    printf("  ],\n"
           "  \"factory_NPU_command_route_verified\":false,\n"
           "  \"factory_model_loaded\":false,\n"
           "  \"real_NPU_inference_verified\":false\n"
           "}\n");
}

int main(int argc,char **argv) {
    const char *sysfs="/sys/bus/pci/devices/0000:04:00.0";
    const char *devdir="/dev";
    const char *mode=NULL;
    const char *proof=NULL;
    int do_execute=0;
    unsigned slot=0;
    for (int i=1;i<argc;i++) {
        if (!strcmp(argv[i],"--sysfs") && i+1<argc)sysfs=argv[++i];
        else if (!strcmp(argv[i],"--devdir") && i+1<argc)devdir=argv[++i];
        else if (!strcmp(argv[i],"--proof") && i+1<argc)proof=argv[++i];
        else if (!strcmp(argv[i],"--execute"))do_execute=1;
        else if (!strcmp(argv[i],"status") || !strcmp(argv[i],"diag-stage4") ||
                 !strcmp(argv[i],"diag-zero256")) {
            if (mode) {usage(argv[0]);return 64;}
            mode=argv[i];
        } else if (!strcmp(argv[i],"select-asic") && i+1<argc) {
            if (mode) {usage(argv[0]);return 64;}
            mode="select-asic";
            char *end=NULL;
            unsigned long n=strtoul(argv[++i],&end,10);
            if (!end || *end || n>=SC4_NPU_COUNT) {usage(argv[0]);return 64;}
            slot=(unsigned)n;
        } else { usage(argv[0]);return 64; }
    }
    if (!mode) {usage(argv[0]);return 64;}
    char err[320]="";
    sc4_device device;
    if (sc4_open(&device,sysfs,devdir,err,sizeof err)) {
        fprintf(stderr,"SC4 OPEN FAILED: %s\n",err);
        return 2;
    }
    sc4_status snapshot;
    if (sc4_snapshot(&device,&snapshot,err,sizeof err)) {
        fprintf(stderr,"SC4 IDENTITY FAILED: %s\n",err);
        sc4_close(&device);
        return 3;
    }
    int rc=0;
    if (!strcmp(mode,"status")) status_json(&snapshot);
    else if (!strcmp(mode,"select-asic")) {
        if (sc4_select_asic(&device,slot,err,sizeof err)) {
            fprintf(stderr,"FACTORY ASIC COMMAND ABI UNVERIFIED: %s\n",err);
            rc=4;
        }
    } else {
        if (!do_execute || !proof) {
            fprintf(stderr,"REFUSED DMA: explicit --execute and --proof required.\n");
            rc=64;
        } else {
            sc4_dma_result result;
            const char *kind = !strcmp(mode,"diag-stage4") ? "stage4":"zero256";
            if (sc4_diag_h2c(&device,kind,proof,&result,err,sizeof err)) {
                fprintf(stderr,"DMA FAILED/REFUSED: %s\n",err);
                rc=5;
            } else {
                printf("{\"operation\":\"physical_H2C_host_diagnostic\","
                       "\"kind\":\"%s\",\"axi\":\"0x%llx\","
                       "\"attempted_bytes\":%u,\"dma_completed_bytes\":%u,"
                       "\"elapsed_ms\":%.3f,"
                       "\"npu_acknowledged\":false,\"model_loaded\":false}\n",
                       kind,(unsigned long long)result.address,
                       result.requested,result.completed,result.elapsed_ms);
            }
        }
    }
    sc4_close(&device);
    return rc;
}
