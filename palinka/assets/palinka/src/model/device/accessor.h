#ifndef __DEV_PHY_ACCESSOR_H__
#define __DEV_PHY_ACCESSOR_H__

#include "src/model/plant/core.h"
#include "src/model/system/core.h"
#include "src/model/device/core.h"

/**
 * \brief An accessor to a physical device.
 */
struct PhysicalDeviceAccessor_t
{
    char type;
    union {
        struct {
            unsigned char sys_id;
            unsigned char dev_id;
            struct Plant_t* plant;
        } by_plant;

        struct {
            unsigned char dev_id;
            struct SystemAccessor_t acc;
        } by_system;

        struct PhysicalDevice_t* dev;
    };
};

const char PHY_DEV_ACESSOR_BY_PLAN = 0x1;
const char PHY_DEV_ACESSOR_BY_SYS  = 0x2;
const char PHY_DEV_ACCESSOR_DIRECT = 0x3;

int phy_dev_open(struct PhysicalDeviceAccessor_t* pdev_acc, struct PhysicalDevice_t** pdev);
void phy_dev_close(struct PhysicalDeviceAccessor_t* pdev_acc);

#endif