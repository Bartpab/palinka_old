/**
 * \file api.h
 * \brief Contains the system common API (init_common, ...)
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#ifndef __COMMON_INIT__
#define __COMMON_INIT__

#include <cstdio>
#include "src/model/common/cfg.h"
#include "src/model/common/header.h"
#include "src/model/error.h"

/*
* \brief Initialise common data for the system
*
* This function must be called before any other init operations !
*
* struct System_t* sys: The system
* struct CommonCfg_t* cfg: The common configuration
* size_t reserved: The number of octets to reserve for system-specific header, next will point to the next entry after the common header.
*/
int init_common(struct System_t* sys, struct CommonCfg_t* common, size_t reserved) {
    struct CommonHeader_t* header;

    size_t total_header_size = sizeof(struct CommonHeader_t) + reserved;
    
    // Not enough memory size...
    if (total_header_size >= sys->memory_size) {
        char err_msg[256];
        snprintf(err_msg, 256, "Not enough memory to init system common, required: %d and got only %d", total_header_size, sys->memory_size);
        sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, err_msg);
        return ERR_NOT_ENOUGH_MEMORY_SPACE;
    }
    
    header = (struct CommonHeader_t*) sys->base);
    char* heap_base = sys->base[total_header_size];
    size_t heap_max_size = sys->memory_size - total_header_size;

    // We need to init the MMU
    mmu_init(*header->mmu, heap_base, heap_max_size);
    header->next = (char*) header + 1;

    return 0;
}

#endif