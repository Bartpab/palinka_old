#include <stdlib.h>

#include "src/model/system/api.h"
#include "src/model/common/data.h"
#include "src/model/common/irq.h"
#include "src/model/system/accessor.h"
#include "src/model/error.h"

int sys_init(struct System_t* sys, struct SystemCfg_t* cfg, struct Allocator_t* allocator)
{    
    // Initialise the error
    error_init(&sys->err);

    void* base = allocator_alloc(allocator, cfg->base_cfg->memory_size);

    if(base == NULL) {
        sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, "Cannot allocate enough system memory.");
        return ERR_NOT_ENOUGH_MEMORY_SPACE;
    }

    // Set the base memory of the system.
    sys->base = base;
    
    // Set the memory size
    sys->memory_size = cfg->base_cfg->memory_size;

    // We set the step callback function of the system.
    sys->step = cfg->step_cbk;

    // We copy the name of the system
    snprintf(sys->name, SYSTEM_NAME_MAX_LENGTH, cfg->name);

    // Initialise the system based on its configuration
    return cfg->init_cbk(&sys, cfg->base_cfg);
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
    struct CommonHeader_t* common;

    if(sys->base == NULL)
        return ERR_SYSTEM_UNAVAILABLE;
    
    common = get_common_header(sys);

    return irq_interrupt(sys, &common->irq, irq);
}
