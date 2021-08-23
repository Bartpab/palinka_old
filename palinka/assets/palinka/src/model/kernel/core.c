#include "src/model/kernel/core.h"
#include "src/model/kernel/cfg.h"
#include "src/model/kernel/mmu.h"
#include "src/model/error.h"

#include "src/utils/memory/alloc.h"

#include <cstdio>

int kernel_init(struct System_t* sys, struct KernelCfg_t* kernel) 
{
    char err_msg[256]; int code;

    struct KernelHeader_t* header;
    struct Allocator_t allocator;

    size_t total_reserved = sizeof(struct KernelHeader_t) + kernel->reserved;
    
    // Not enough memory size...
    if (total_reserved >= sys->memory_size) 
    {
        snprintf(err_msg, 256, "Not enough system memory to initialise system kernel, required: %d and got only %d", total_reserved, sys->memory_size);
        sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, err_msg);
        return ERR_NOT_ENOUGH_MEMORY_SPACE;
    }
    
    header = (struct KernelHeader_t*) sys->base;
    char* heap_base = sys->base + total_reserved;
    size_t heap_max_size = sys->memory_size - total_reserved;

    // We need to init the MMU firstly so we can have the allocator functions.
    mmu_init(&header->mmu, heap_base, heap_max_size);

    // Now we can use the allocator functions
    allocator = create_sys_allocator(sys);

    // We need to initialise the IRQ table
    if (!irq_init(&header->irq, &allocator, kernel->irq_size)) 
    {
        snprintf(err_msg, 256, "Not enough system memory to initialise the IRQ table.");
        sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, err_msg);
        return ERR_NOT_ENOUGH_MEMORY_SPACE;
    }

    // Now we can register drivers

    return 0;
}

void kernel_delete(struct System_t* sys)
{
    struct Allocator_t allocator;
    struct KernelHeader_t* header;
    
    header = get_kernel_header(sys);
    allocator = create_sys_allocator(sys);

    irq_delete(&header->irq, &allocator);
}