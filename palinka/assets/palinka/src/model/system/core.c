#include "src/model/system/core.h"
#include "src/model/kernel/core.h"
#include "src/model/kernel/irq.h"
#include "src/model/system/accessor.h"
#include "src/model/error.h"

#include <stdlib.h>

int sys_init(struct System_t* sys, struct SystemCfg_t* cfg, struct Allocator_t* allocator)
{    
    struct PhysicalDeviceCfgListIterator_t it;
    struct PhysicalDeviceCfg_t* dev_cfg;

    // Initialise the error
    error_init(&sys->err);

    void* base = allocator_alloc(allocator, cfg->base_cfg->memory_size);

    if(base == NULL) {
        sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, "Cannot allocate enough system memory.");
        return ERR_NOT_ENOUGH_MEMORY_SPACE;
    }

    struct Allocator_t allocator = created_fixed_allocator(base, cfg->memory_size);

    // Set the base memory of the system.
    sys->base = base;
    
    // Set the memory size
    sys->memory_size = cfg->base_cfg->memory_size;

    // We set the step callback function of the system.
    sys->step = cfg->step;

    // We copy the name of the system
    snprintf(sys->name, SYSTEM_NAME_MAX_LENGTH, cfg->name);

    //
    phy_dev_cfg_list_it_init(&it, &cfg->pdevices);
    while(it.next(&it)) 
    {
        if(it.get(&it, &dev_cfg)) 
        {

        }
    }    

    // Initialise the system based on its configuration
    return cfg->init(&sys);
}

void sys_push_error(struct System_t* sys, const int code, const char* msg) 
{
    write_error(&sys->err, code, msg);
}

int sys_pop_error(struct System_t* sys, struct Error_t* output)
{
    if(sys->err.code > 0) {
        *output = sys->err;
        // erase the error.
        write_error(&sys->err, 0, "");
        return 1;
    }

    return 0;
}

int sys_step(struct System_t* sys)
{
    return sys->step(sys);
}

int sys_interrupt(struct System_t* sys, unsigned char irq)
{
    struct KernelHeader_t* kernel;

    if(sys->base == NULL)
        return ERR_SYSTEM_UNAVAILABLE;
    
    kernel = get_kernel_header(sys);

    return irq_interrupt(sys, &kernel->irq, irq);
}

int sys_write_device(struct System_t* sys, size_t dev_id, unsigned char data)
{
    struct PhysicalDevice_t* dev;

    if(phy_dev_list_get(&sys->devices, dev_id, &dev))
    {
        dev->write(dev, data);
    }
}