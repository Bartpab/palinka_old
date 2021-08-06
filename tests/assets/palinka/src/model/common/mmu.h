#ifndef __MMU_H__
#define __MMU_H__

#include <stddef.h>

/*
* Memory Management Unit
*
* Each system has a MMU to manage dynamic allocation of memory.
*/


struct MemoryManagementUnit_t
{
    char* raw_tail;
    char* raw_head;
    char* raw_end;

    struct HeapHeader_t* head;
    struct HeapHeader_t* tail;
}

void mmu_init(struct MemoryManagementUnit_t* mmu, char* base_heap, size_t free_space_size);

/////////////////////
// MMU API      /////
/////////////////////
void sys_free(struct System_t* sys, char* block);
char* sys_alloc(struct System_t* sys, size_t len);

/////////////////////
// Lower level API //
/////////////////////
struct HeapHeader_t
{
    size_t size;
    char is_free;
    struct HeapHeader_t* next;
};

struct HeapHeader_t* get_free_block(struct System_t* sys, size_t size);
char* sys_sbrk(struct System_t* sys, int len);
#endif