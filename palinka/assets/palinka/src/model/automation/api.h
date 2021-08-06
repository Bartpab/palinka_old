#include <stddef.h>

#include "src/model/automation/cfg.h"
#include "src/model/automation/header.h"
#include "src/model/system.h"

/**
* \brief Initialise the system as an automation system.
*
* Calls init_common internally.
*
* \param sys The system to initialise as an automation system.
* \param cfg The automation system configuration
* \return 0 if no error occured, else > 0 if an error occured.
*/
int init_automation_system(struct System_t* sys, struct AutomationSystemCfg_t* cfg);

/**
 * \brief Execute a simulation step for the system
 * 
 * \param sys The related system.
 * \return 0 if no error occured, else > 0 if an error occured.
 */
int step_automation_system(struct System_t* sys);

// Lower Level //

/**
 * \brief Return the automation system's header
 * \return The automation header of the system.
 */
struct AutomationHeader_t* get_automation_header(struct System_t* sys);