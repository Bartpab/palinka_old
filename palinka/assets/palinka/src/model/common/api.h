/**
 * \file api.h
 * \brief Contains the system common API (common_init, ...)
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#ifndef __COMMON_INIT__
#define __COMMON_INIT__

#include "src/model/system/api.h"
#include "src/model/common/cfg.h"

/**
* \brief Initialise system's common
*
* This function must be called before any other init operations !
*
* struct System_t* sys: The system
* struct CommonCfg_t* cfg: The common configuration
* size_t reserved: The number of octets to reserve for system-specific header, next will point to the next entry after the common header.
*/
int common_init(struct System_t* sys, struct CommonCfg_t* common, size_t reserved);

/**
 * \brief Delete common header
 */
void common_delete(struct System_t* sys);
#endif