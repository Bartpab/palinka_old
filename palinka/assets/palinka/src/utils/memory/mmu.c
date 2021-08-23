#include <stddef.h>

#include "src/model/kernel/mmu.h"
#include "src/model/kernel/data.h"

void mmu_init(struct MemoryManagementUnit_t* mmu, char* base_heap, size_t free_space_size)
{
    mmu->raw_tail = mmu->raw_head = base_heap;
    mmu->raw_limit  = mmu->raw_tail + free_space_size - 1;
}

struct HeapHeader_t* get_free_block(struct MemoryManagementUnit_t* mmu, size_t size)
{
    struct HeapHeader_t* curr =mmu->head;
    
    while(curr) {
        if(curr->is_free && curr->size >= size) {
            return curr;
        }

        curr = curr->next;
    }

    return NULL;
}

void* mmu_sbrk(struct MemoryManagementUnit_t* mmu, int len)
{
    if (len > 0) { // If the len is > 0, we fetch raw memory 
        // Cannot increase heap memory
        if (mmu->raw_head + len > mmu->raw_limit) 
            return NULL;

        // Increase the raw head pointer by the size of the block
        void* block = mmu->raw_head;
        mmu->raw_head += len;
        return block;       
    } else if(len < 0) { // If the len is < 0, we release raw memory
        if(mmu->raw_head - len < mmu->raw_tail) {
           mmu->raw_head = mmu->raw_tail; 
        } else {
            mmu->raw_head -= len;
        }
        return NULL;
    } else { // If the len is 0, we return the raw head memory
        return mmu->raw_head;
    }
}

void mmu_free(struct MemoryManagementUnit_t* mmu, void* block)
{
    struct HeapHeader_t* header, *it;

    header = (struct HeapHeader_t*) block - 1;
    void* raw_head = mmu_sbrk(mmu, 0);

    // We remove the tail element
    if (block + header->size == raw_head) 
    {
        if (mmu->head == mmu->tail) {
            mmu->head = mmu->tail = NULL;
        } else {
            it = mmu->head;
            while (it) {
                if(it->next == mmu->tail) 
                {
                    it->next = NULL;
                    mmu->tail = it;
                }
                it = it->next;
            }
        }

        mmu_sbrk(sys, 0 - sizeof(struct HeapHeader_t) - header->size);
        return;
    }

    header->is_free = 1;
}


void* mmu_alloc(struct MemoryManagementUnit_t* mmu, size_t len)
{
    struct HeapHeader_t* header;
    size_t required_size;
    void* block;

    header = get_free_block(mmu, len);

    if(header != NULL) {
        header->is_free = 0;
        return (void*)(header + 1);
    }

    required_size = sizeof(struct HeapHeader_t) + len;
    block = mmu_sbrk(mmu, required_size);
    
    if (block == NULL) {
        return NULL;
    }

    header = (struct HeapHeader_t*) block;
    header->size = len;
    header->is_free = 0;
    header->next = NULL;

    if(mmu->head == NULL)
        mmu->head = header;
    
    if(mmu->tail != NULL) 
        mmu->tail->next = header;

    return (void*)(header + 1);
}
