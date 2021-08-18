#ifndef __SYS_ACCESSOR_H__
#define __SYS_ACCESSOR_H__

#include "src/model/system/container.h"

struct SystemAccessor_t 
{
    struct SystemContainer_t* container;
};

/**
 * \brief Open an access to the system.
 * 
 * 
 * \return 1 if succeeded, 0 if failed.
 */
int sys_open(struct SystemAccessor_t* sys, struct System_t** out);

/**
 * \brief Close the access to the system.
 * 
 * Important to call it once the access is no longer required !
 */
void sys_close(struct SystemAccessor_t* sys);

#endif