/**
 * \file mmu.h
 * \brief Contains the Memory Management Unit functions.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#ifndef __MMU_H__
#define __MMU_H__

#include <stddef.h>

/**
* \brief Memory Management Unit
*
* Each system has a MMU to manage dynamic allocation of memory.
*/
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
void mmu_init(struct MemoryManagementUnit_t* mmu, char* base_heap, size_t heap_max_size);

/////////////////////
// MMU API      /////
/////////////////////
/**
 * \brief System's memory allocator
 * 
 * \param sys The system
 * \param len The size of the memory block.
 * \return NULL if the allocation failed (eg: no more memory), else the address of the allocated block.
 */
void* sys_alloc(struct System_t* sys, size_t len);

/**
 * \brief System's memory free
 * 
 * Free the memory block
 * 
 * \param sys The system
 * \param block The memory block to free
 */
void sys_free(struct System_t* sys, void* block);

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

/**
 * \brief Change the data segment size.
 * 
 * The simulation allocate a fixed-size memory block at the beginning.
 * The system can get/release raw memory based on this memory block.
 * The raw memory is then used by the MMU to alloc/free memory.
 * 
 * \param sys The system 
 * \param len If > 0, add len bytes to the data segment, if < 0 remove len bytes to the data segment, if =0, return the head of the data segment.
 * \return NULL if the function failed (eg: no more memory), or the address of the allocated block.
 */
void* sys_sbrk(struct System_t* sys, int len);
#endif