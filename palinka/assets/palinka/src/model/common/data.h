/**
 * \file header.h
 * \brief Contains the system common header.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#ifndef __COMMON_HEADER__
#define __COMMON_HEADER__

#include "src/model/common/mmu.h"
#include "src/model/common/irq.h"
#include "src/model/system/api.h"

/**
 * \struct CommonHeader_t
 * \brief Contains the common data to manage common routines.
 *
 * Common routines include: Memory Management Unit [MMU], Device Management [DEV], ... 
 */
struct CommonHeader_t 
{
    struct MemoryManagementUnit_t mmu; /*! Memory Management unit */
    struct InterruptRequestTable_t irq; /*! Interrupt Request */
};

struct CommonHeader_t* get_common_header(struct System_t* sys) 
{
    return (struct CommonHeader_t*) sys->base;
}

#endif