#ifndef __ALLOCATOR_H__
#define __ALLOCATOR_H__

#include "src/model/system/core.h"
#include "src/model/kernel/mmu.h"
#include "src/utils/memory/mmu.h"

#include <stdlib.h>

struct Allocator_t {
    char type;
    union {
        struct System_t* sys;
        struct {
            void* curr;
            void *limit;
        } fixed;
        struct MemoryManagementUnit_t* mmu;
    };
};

const char SYS_ALLOCATOR  = 0x1;
const char GLOBAL_ALLOCATOR = 0x2;
const char FIXED_ALLOCATOR = 0x3;
const char MMU_ALLOCATOR = 0x4;

struct Allocator_t created_global_allocator(void *base, size_t capacity)
{
    struct Allocator_t allocator;
    allocator.type = GLOBAL_ALLOCATOR;
    return allocator;
}

struct Allocator_t created_fixed_allocator(void *base, size_t capacity)
{
    struct Allocator_t allocator;
    allocator.type = FIXED_ALLOCATOR;
    allocator.fixed.curr = base;
    allocator.fixed.limit = base + capacity - 1;
    return allocator;
}

struct Allocator_t create_sys_allocator(struct System_t* sys) 
{
    struct Allocator_t allocator;
    allocator.type = SYS_ALLOCATOR;
    allocator.sys = sys;
    return allocator;
}

struct Allocator_t create_mmu_allocator(struct MemoryManagementUnit_t* mmu)
{
    struct Allocator_t allocator;
    allocator.type = MMU_ALLOCATOR;
    allocator.mmu = mmu;
    return allocator;   
}

void allocator_free(struct Allocator_t* allocator, void* block) 
{
    if (allocator->type == SYS_ALLOCATOR) 
        return sys_free(allocator->sys, block);
    else if (allocator->type == MMU_ALLOCATOR) {
        mmu_free(allocator->mmu, block);
    }
    else
        return free(block);  
}

void* allocator_alloc(struct Allocator_t* allocator, size_t len) 
{
    if (allocator->type == SYS_ALLOCATOR) 
        return sys_alloc(allocator->sys, len);
    else if (allocator->type == MMU_ALLOCATOR) {
       return mmu_alloc(allocator->mmu, len);
    }
    else if (allocator->type == FIXED_ALLOCATOR) 
    {
        if(allocator->fixed.curr + len > allocator->fixed.limit)
            return NULL;
        
        void* block = allocator->fixed.curr;
        allocator->fixed.curr += len;
        return block;
    }
    else
        return malloc(len);
}

#endif