#include "src/model/common/api.h"

#include "src/model/common/cfg.h"
#include "src/model/common/data.h"
#include "src/model/common/mmu.h"
#include "src/model/error.h"

#include "src/utils/alloc.h"

#include <cstdio>

int common_init(struct System_t* sys, struct CommonCfg_t* common, size_t reserved) 
{
    char err_msg[256]; int code;

    struct CommonHeader_t* header;
    struct Allocator_t allocator;

    size_t total_header_size = sizeof(struct CommonHeader_t) + reserved;
    
    // Not enough memory size...
    if (total_header_size >= sys->memory_size) 
    {
        snprintf(err_msg, 256, "Not enough system memory to initialise system common, required: %d and got only %d", total_header_size, sys->memory_size);
        sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, err_msg);
        return ERR_NOT_ENOUGH_MEMORY_SPACE;
    }
    
    header = (struct CommonHeader_t*) sys->base;
    char* heap_base = sys->base + total_header_size;
    size_t heap_max_size = sys->memory_size - total_header_size;

    // We need to init the MMU firstly so we can have the allocator functions.
    mmu_init(&header->mmu, heap_base, heap_max_size);

    // Now we can use the allocator functions
    allocator = create_sys_allocator(sys);

    // We need to initialise the IRQ table
    if (!irq_init(&header->irq, &allocator, common->irq_size)) 
    {
        snprintf(err_msg, 256, "Not enough system memory to initialise the IRQ table.");
        sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, err_msg);
        return ERR_NOT_ENOUGH_MEMORY_SPACE;
    }

    // Now we can register devices

    return 0;
}

void common_delete(struct System_t* sys)
{
    struct Allocator_t allocator;
    struct CommonHeader_t* header;
    
    header = get_common_header(sys);
    allocator = create_sys_allocator(sys);

    irq_delete(&header->irq, &allocator);
}