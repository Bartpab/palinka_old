#ifndef __PHY_H__
#define __PHY_H__

#include "src/model/common/skb.h"
#include "src/model/system/api.h"
#include "src/model/common/mmu.h"
#include "src/utils/alloc.h"
#include "src/utils/math.h"

#include <stdlib.h>
#include <string.h> 

struct PhysicalDevice_t 
{
    void* base;
    void* limit;

    /*! Address to the firmware data of the device */
    const char family;
    void* firmware;
};

const char NETWORK_DEVICE = 0x1;

struct PhysicalDeviceCfg_t
{
    void* cfg;
    int (*init_cbk)(struct PhysicalDevice_t*, struct PhysicalDeviceCfg_t* cfg, struct Allocator_t* firmware_allocator, struct Allocator_t* dev_allocator);
};

/**
 * \brief List of physical devices
 */
struct PhysicalDeviceList_t 
{
    struct PhysicalDevice_t* tail;
    struct PhysicalDevice_t* head;
    struct PhysicalDevice_t* limit;
};

/**
 * \brief Get the physical device based on its id.
 * 
 * \return 1 if it exists, 0 if not.
 */
int phy_dev_list_get(struct PhysicalDeviceList_t* list, unsigned char id, struct PhysicalDevice_t** out);

/**
 * \brief Add a physical device to the list
 * 
 * \return 1 if succeeded, 0 else (no more space)
 */ 
int phy_dev_list_add(struct PhysicalDeviceList_t* list, struct PhysicalDevice_t dev);

/**
 * \brief Initialise the list.
 */
int phy_dev_list_init(struct PhysicalDeviceList_t* list, size_t capacity);

/**
 * \brief Delete the list.
 */ 
void phy_dev_list_delete(struct PhysicalDeviceList_t* list);

#endif