#include <stddef.h>

#include "src/model/kernel/mmu.h"
#include "src/model/kernel/core.h"

void sys_free(struct System_t* sys, void* block)
{
    struct KernelHeader_t* kernel = _get_kernel(sys);
    mmu_free(&kernel->mmu, block);
}

void* sys_alloc(struct System_t* sys, size_t len)
{
    struct KernelHeader_t* kernel = _get_kernel(sys);
    return mmu_alloc(&kernel->mmu, len);
}
