#ifndef __AUTOMATION_API_H__
#define __AUTOMATION_API_H__

#include <stddef.h>

#include "src/model/automation/cfg.h"
#include "src/model/automation/header.h"
#include "src/model/system/core.h"

/**
* \brief Initialise the system as an automation system.
*
* Calls kernel_init internally.
*
* \param sys The system to initialise as an automation system.
* \param cfg The automation system configuration
* \return 0 if no error occured, else > 0 if an error occured.
*/
int automation_system_init(struct System_t* sys, struct AutomationCfg_t* cfg);

/**
 * \brief Execute a simulation step for the system
 * 
 * \param sys The related system.
 * \return 0 if no error occured, else > 0 if an error occured.
 */
int automation_system_step(struct System_t* sys);

// Lower Level //

/**
 * \brief Callback to initialise the automation system.
 * 
 * This works because cfg is the first attribute of AutomationCfg_t, and because
 * we ensure that the pointer is in fact a pointer to a full AutomationCfg_t value.
 */
int automation_system_init(struct System_t* sys, struct KernelgCfg_t* cfg);


#endif