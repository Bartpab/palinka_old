#include "src/model/common/device/phy/accessor.h"

int phy_dev_open(struct PhysicalDeviceAccessor_t* pdev_acc, struct PhysicalDevice_t** pdev)
{
    int retcode;

    if(pdev_acc->type == PHY_DEV_ACCESSOR_DIRECT) {
        *pdev = pdev_acc->dev;
        return 1;
    } else if (pdev_acc->type == PHY_DEV_ACESSOR_BY_PLAN) {
        struct SystemAccessor_t sys_acc;
        
        retcode = plant_get_system(pdev_acc->by_plant.plant, pdev_acc->by_plant.sys_id, &sys_acc);

        if(!retcode)
            return 0;
        
        pdev_acc->type = PHY_DEV_ACESSOR_BY_SYS;
        pdev_acc->by_system.dev_id = pdev_acc->by_plant.dev_id;

        return phy_dev_open(pdev_acc, pdev);
    } else if (pdev_acc->type == PHY_DEV_ACESSOR_BY_SYS) {
        struct System_t* sys;
        
        retcode = sys_open(&pdev_acc->by_system.acc, &sys);

        if(!retcode)
            return 0;
        
        return phy_dev_list_get(&sys->devices, pdev_acc->by_system.dev_id, pdev);
    }

    return 0;
}

void phy_dev_close(struct PhysicalDeviceAccessor_t* pdev_acc)
{
    if(pdev_acc->type == PHY_DEV_ACESSOR_BY_SYS) 
    {
        sys_close(&pdev_acc->by_system.acc);
    }
}
