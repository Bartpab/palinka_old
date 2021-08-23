#ifndef __COMMON_CFG_H__
#define __COMMON_CFG_H__

#include <stddef.h>

#include "src/model/device/cfg.h"

/**
 * \brief System Kernel Configuration 
 */
struct KernelCfg_t 
{
    /*! Memory size of the system */
    size_t memory_size;

    /*! Reserved memory */
    size_t reserved;

    /*! Number of Interrupt Requests possible */
    size_t irq_size;
};

#endif