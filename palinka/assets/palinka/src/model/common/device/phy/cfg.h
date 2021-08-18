#ifndef __DEV_PHY_CFG_H__
#define __DEV_PHY_CFG_H__

#include "src/utils/alloc.h"

struct PhysicalDeviceCfg_t
{
    void* data;
    int (*init)(
        struct PhysicalDevice_t* pdev, 
        struct PhysicalDeviceCfg_t* pcfg, 
        struct Allocator_t* firmware_allocator, 
        struct Allocator_t* dev_allocator
    );
};

void phy_dev_cfg_delete(struct PhysicalDeviceCfg_t* pcfg) 
{
    free(pcfg->data);
    pcfg->data = NULL;
}

#endif