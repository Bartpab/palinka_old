#include <stddef.h>

#include "src/model/common/mmu.h"
#include "src/model/common/data.h"

void mmu_init(struct MemoryManagementUnit_t* mmu, char* base_heap, size_t free_space_size)
{
    mmu->raw_tail = mmu->raw_head = base_heap;
    mmu->raw_limit  = mmu->raw_tail + free_space_size - 1;
}

struct HeapHeader_t* get_free_block(struct System_t* sys, size_t size)
{
    struct HeapHeader_t* curr = get_common_header(sys)->mmu.head;
    
    while(curr) {
        if(curr->is_free && curr->size >= size) {
            return curr;
        }

        curr = curr->next;
    }

    return NULL;
}

void* sys_sbrk(struct System_t* sys, int len)
{

    struct CommonHeader_t* common = get_common_header(sys);

    if (len > 0) { // If the len is > 0, we fetch raw memory 
        // Cannot increase heap memory
        if (common->mmu.raw_head + len > common->mmu.raw_limit) 
            return NULL;

        // Increase the raw head pointer by the size of the block
        char* block = common->mmu.raw_head;
        common->mmu.raw_head += len;
        return block;       
    } else if(len < 0) { // If the len is < 0, we release raw memory
        if(common->mmu.raw_head - len < common->mmu.raw_tail) {
           common->mmu.raw_head = common->mmu.raw_tail; 
        } else {
            common->mmu.raw_head -= len;
        }
        return NULL;
    } else { // If the len is 0, we return the raw head memory
        return common->mmu.raw_head;
    }
}

void sys_free(struct System_t* sys, void* block)
{
    struct CommonHeader_t* common = get_common_header(sys);
    struct HeapHeader_t* header, *it;

    header = (struct HeapHeader_t*) block - 1;
    void* raw_head = sys_sbrk(sys, 0);

    // We remove the tail element
    if (block + header->size == raw_head) 
    {
        if (common->mmu.head == common->mmu.tail) {
            common->mmu.head = common->mmu.tail = NULL;
        } else {
            it = common->mmu.head;
            while (it) {
                if(it->next == common->mmu.tail) {
                    it->next = NULL;
                    common->mmu.tail = it;
                }
                it = it->next;
            }
        }

        sys_sbrk(sys, 0 - sizeof(struct HeapHeader_t) - header->size);
        return;
    }

    header->is_free = 1;
}


void* sys_alloc(struct System_t* sys, size_t len)
{
    struct CommonHeader_t* common = get_system_data(sys);
    struct HeapHeader_t* header;
    size_t required_size;
    void* block;

    header = get_free_block(sys, len);

    if(header != NULL) {
        header->is_free = 0;
        return (void*)(header + 1);
    }

    required_size = sizeof(struct HeapHeader_t) + len;
    block = sys_sbrk(sys, required_size);
    
    if (block == NULL) {
        return NULL;
    }

    header = (struct HeapHeader_t*) block;
    header->size = len;
    header->is_free = 0;
    header->next = NULL;

    if(common->mmu.head == NULL)
        common->mmu.head = header;
    
    if(common->mmu.tail != NULL) 
        common->mmu.tail->next = header;

    return (char*)(header + 1);
}
