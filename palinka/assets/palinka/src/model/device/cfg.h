#ifndef __DEV_PHY_CFG_H__
#define __DEV_PHY_CFG_H__

#include "src/utils/memory/alloc.h"

struct PhysicalDeviceCfg_t
{
    /*! The size of memory to reserve for DMA*/
    size_t dma_size;
    size_t offset;

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

struct PhysicalDeviceCfgList_t
{
    struct PhysicalDeviceCfg_t* tail;
    struct PhysicalDeviceCfg_t* head;
    struct PhysicalDeviceCfg_t* limit;
};

int phy_dev_cfg_list_init(struct PhysicalDeviceCfgList_t *list, size_t capacity);
int phy_dev_cfg_list_add(struct PhysicalDeviceCfgList_t *list, struct PhysicalDeviceCfg_t cfg);
void phy_dev_cfg_list_delete(struct PhysicalDeviceCfgList_t *list);

struct PhysicalDeviceCfgListIterator_t
{
    struct PhysicalDeviceCfg_t* curr;
    struct PhysicalDeviceCfgList_t* list;

    int (*next)(struct PhysicalDeviceCfgListIterator_t* it);
    int (*get)(struct PhysicalDeviceCfgListIterator_t* it, struct PhysicalDeviceCfg_t** out);
};

void phy_dev_cfg_list_it_init(struct PhysicalDeviceCfgListIterator_t* it, struct PhysicalDeviceCfgList_t *list);
int phy_dev_cfg_list_it_next(struct PhysicalDeviceCfgListIterator_t* it);
int phy_dev_cfg_list_it_get(struct PhysicalDeviceCfgListIterator_t* it, struct PhysicalDeviceCfg_t** out);

#endif