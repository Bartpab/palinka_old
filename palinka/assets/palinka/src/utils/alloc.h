#ifndef __ALLOCATOR_H__
#define __ALLOCATOR_H__

#include "src/model/system/api.h"
#include "src/model/common/mmu.h"

#include <stdlib.h>

struct Allocator_t {
    char type;
    union {
        struct System_t* sys;
        struct {
            void* curr;
            void *limit;
        } stic;
    };
};

const char SYS_ALLOCATOR  = 0x1;
const char GLOBAL_ALLOCATOR = 0x2;
const char STATIC_ALLOCATOR = 0x3;

struct Allocator_t create_static_allocator(void *base, size_t capacity)
{
    struct Allocator_t allocator;
    allocator.type = STATIC_ALLOCATOR;
    allocator.stic.curr = base;
    allocator.stic.limit = base + capacity - 1;
}

struct Allocator_t create_sys_allocator(struct System_t* sys) 
{
    struct Allocator_t allocator;
    allocator.type = SYS_ALLOCATOR;
    allocator.sys = sys;
    return allocator;
}

void allocator_free(struct Allocator_t* allocator, void* block) 
{
    if (allocator->type == SYS_ALLOCATOR) 
        return sys_free(allocator->sys, block);
    else
        return free(block);  
}

void* allocator_alloc(struct Allocator_t* allocator, size_t len) 
{
    if (allocator->type == SYS_ALLOCATOR) 
        return sys_alloc(allocator->sys, len);
    else if (allocator->type == STATIC_ALLOCATOR) 
    {
        if(allocator->stic.curr + len > allocator->stic.limit)
            return NULL;
        
        void* block = allocator->stic.curr;
        allocator->stic.curr += len;
        return block;
    }
    else
        return malloc(len);
}

#endif