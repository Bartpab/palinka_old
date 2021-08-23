/**
 * \file mmu.h
 * \brief Contains the Memory Management Unit functions.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#ifndef __SYS_MMU_H__
#define __SYS_MMU_H__

#include <stddef.h>

#include "src/utils/memory/mmu.h"

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

#endif