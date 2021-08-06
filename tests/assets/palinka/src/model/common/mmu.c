#ifndef __MMU_H__
#define __MMU_H__

#include <stddef.h>

void mmu_init(struct MemoryManagementUnit_t* mmu, char* base_heap, size_t free_space_size)
{
    mmu->raw_tail = base_heap;
    mmu->raw_head = mmu.base;
    mmu->raw_end  = mmu.base + free_space_size;
}

struct HeapHeader_t* get_free_block(struct System_t* sys, size_t size)
{
    struct HeapHeader_t* curr = get_system_header(sys)->head;
    
    while(curr) {
        if(curr->is_free && curr->size >= size) {
            return curr;
        }

        curr = curr->next;
    }

    return NULL;
}

char* sys_sbrk(struct System_t* sys, int len)
{
    if (len > 0) {
        struct SystemData_t* sysdt = get_system_data(sys);
        
        // Cannot increase heap memory
        if (sysdt->mmu.raw_head + len >= sysdt->mmu.raw_end) 
        {
            return NULL;
        }

        char* block = sysdt->mmu.raw_head;
        sysdt->mmu.raw_head += len;
        return block;       
    } else if(len < 0) {
        if(sysdt->mmu.raw_head - len < sysdt->mmu.raw_tail) {
           sysdt->mmu.raw_head = sysdt->mmu.raw_tail; 
        } else {
            sysdt->mmu.raw_head -= len;
        }
        return NULL;
    } else {
        return sysdt->mmu.raw_head;
    }
}

void sys_free(struct System_t* sys, char* block)
{
    struct SystemData_t* sysdt = get_system_data(sys);
    struct HeapHeader_t* header, *it;

    header = (struct HeapHeader_t*) block - 1;
    char* raw_head = sys_sbrk(sys, 0);

    // We remove the tail element
    if (block + header->size == raw_head) 
    {
        if (sysdt->mmu.head == sysdt->mmu.tail) {
            sysdt->mmu.head = sysdt->mmu.tail = NULL;
        } else {
            it = sysdt->mmu.head;
            while (it) {
                if(it->next == sysdt->mmu.tail) {
                    it->next = NULL;
                    sysdt->mmu.tail = it;
                }
                it = it->next;
            }
        }

        sys_sbrk(0 - sizeof(struct HeapHeader_t) - header->size);
        return;
    }

    header->is_free = 1;
}


char* sys_alloc(struct System_t* sys, size_t len)
{
    struct SystemData_t* sysdt = get_system_data(sys);
    struct HeapHeader_t* header;

    header = get_free_block(sys, len);

    if(header != NULL) {
        header->is_free = 0;
        return (char*)(header + 1);
    }

    required_size = sizeof(HeapHeader_t) + len
    block = sys_sbrk(required_size);
    
    if (block == NULL) {
        return NULL;
    }

    header = (struct HeapHeader_t*) block;
    header->size = len;
    header->is_free = 0;
    headr->next = NULL;

    if(sysdt->mmu.head == NULL)
        sysdt->mmu.head = header;
    
    if(sysdt->mmu.tail != NULL) 
        sysdt->mmu.tail.next = header;

    return (char*)(header + 1);
}

#endif