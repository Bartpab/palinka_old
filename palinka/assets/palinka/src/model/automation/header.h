#ifndef __AUTOMATION_HEADER_H__
#define __AUTOMATION_HEADER_H__

#include "src/model/automation/task.h"
#include "src/model/automation/data_block.h"

/**
 * \brief Automation System's specific header
 */ 
struct AutomationHeader_t 
{
    struct AutomationTaskList_t         tasks;
    struct AutomationDataBlockList_t    data_blocks;
};

/**
 * \brief Return the automation system's header
 * \return The automation header of the system.
 */
struct AutomationHeader_t* get_automation_header(struct System_t* sys);

#endif