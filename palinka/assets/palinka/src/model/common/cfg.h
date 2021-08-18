#ifndef __COMMON_CFG_H__
#define __COMMON_CFG_H__

#include <stddef.h>

/**
 * \brief System Common Configuration 
 */
struct CommonCfg_t 
{
    /*! Memory size of the system */
    size_t memory_size;

    /*! Number of Interrupt Requests possible */
    size_t irq_size;
};

#endif