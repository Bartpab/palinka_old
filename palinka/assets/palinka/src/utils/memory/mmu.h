#ifndef __UTILS_MMU_H__
#define __UTILS_MMU_H__

struct MemoryManagementUnit_t
{
    void* raw_tail;
    void* raw_head;
    void* raw_limit;

    struct HeapHeader_t* head;
    struct HeapHeader_t* tail;
};

/**
 * \brief Initialise the MMU
 * 
 * \param mmu The Memory Management Unit
 * \param base_heap The address to the raw heap area
 * \param heap_max_size The maximum size of the raw heap area
 */
void mmu_init(struct MemoryManagementUnit_t* mmu, char* base, size_t size);

/**
 * \brief Allocate memory
 * 
 * \param sys The system
 * \param len The size of the memory block.
 * \return NULL if the allocation failed (eg: no more memory), else the address of the allocated block.
 */
void* mmu_alloc(struct MemoryManagementUnit_t* mmu, size_t len);

/**
 * \brief Free memory
 * 
 * Free the memory block
 * 
 * \param sys The system
 * \param block The memory block to free
 */
void mmu_free(struct MemoryManagementUnit_t* mmu, void* block);

struct HeapHeader_t
{
    size_t size;
    char is_free;
    struct HeapHeader_t* next;
};

struct HeapHeader_t* get_free_block(struct MemoryManagementUnit_t* mmu, size_t size);

/**
 * \brief Change the data segment size.
 * 
 * 
 * \param mmu The mmu 
 * \param len If > 0, add len bytes to the data segment, if < 0 remove len bytes to the data segment, if = 0, return the head of the data segment.
 * \return NULL if the function failed (eg: no more memory), or the address of the allocated block.
 */
void* mmu_sbrk(struct System_t* sys, int len);

#endif