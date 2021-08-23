/**
 * \file core.h
 * \brief Contains the system's kernel (kernel_init, ...)
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#ifndef __COMMON_INIT__
#define __COMMON_INIT__

#include "src/model/system/core.h"
#include "src/model/kernel/cfg.h"

/**
 * \struct KernelHeader_t
 * \brief Contains the kernel data to manage kernel routines.
 *
 * Kernel routines include: Memory Management Unit [MMU], Device Management [DEV], ... 
 */
struct KernelHeader_t 
{
    struct MemoryManagementUnit_t mmu; /*! Memory Management unit */
    struct InterruptRequestTable_t irq; /*! Interrupt Request */
    struct NetDeviceList_t net_devices;
};

#define _get_kernel(sys) (struct KernelHeader_t*) sys->base 

struct KernelHeader_t* get_kernel_header(struct System_t* sys) 
{
    return (struct KernelHeader_t*) sys->base;
}


/**
* \brief Initialise system's kernel
*
* This function must be called before any other init operations !
*
* \param sys The system
* \param cfg: The kernel configuration
*/
int kernel_init(struct System_t* sys, struct KernelCfg_t* kernel);

/**
 * \brief Delete kernel header
 */
void kernel_delete(struct System_t* sys);

#endif