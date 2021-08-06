#ifndef __SYSTEM_H__
#define __SYSTEM_H__

#include "src/model/data_block.h"
#include "src/model/system/mmu.h"

#include <stddef.h>

#define MEMORY_SIZE 64000 // 64ko of memory
#define FREE_SIZE 32000 // 32ko of heap size

struct System_t {
    char* base;
    char* app_base;
    char* sys_base;
};

/*
    <lower>
    [APP MEMORY]
    [SYS MEMORY]
    [...]
    [HEAP]
    [...]
    <higher>

*/

struct SystemData_t
{
    struct MemoryManagementUnit_t mmu;
};

size_t get_sys_memory_size()
{
    return sizeof(struct SystemData_t) + FREE_SIZE;
}

void sys_init(struct System_t* sys, size_t sys_base_offset)
{
    sys->sys_base = sys->base[sys_base_offset];
    
    *get_system_data(sys)->mmu = mmu_init(
        sys->sys_base[sizeof(struct SystemData_t)], 
        FREE_SIZE
    );
}

struct SystemData_t* get_system_data(struct System_t* sys)
{
    return (struct SystemData_t*) sys->sys_base;
}

struct DataBlock_t open_data_block(struct System_t* sys, unsigned int offset);

#endif