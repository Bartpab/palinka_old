#include <stddef.h>
#include <stdio.h>

#include "src/model/automation/core.h"
#include "src/model/automation/cfg.h"
#include "src/model/automation/header.h"
#include "src/model/automation/task.h"
#include "src/model/kernel/data.h"
#include "src/model/kernel/core.h"
#include "src/model/system/core.h"
#include "src/model/error.h"

int automation_system_init(struct System_t* sys, struct AutomationCfg_t* cfg) {
    int code; char err_msg[256];

    struct AutomationDataBlockCfgIterator_t db_it;
    struct AutomationTaskCfgIterator_t task_it;
    
    void (*raw_task_curr)(struct System_t*);
    size_t *db_size_curr;

    code = kernel_init(sys, cfg, sizeof(struct AutomationHeader_t));

    if(code)
        return code;

    struct AutomationHeader_t* automation = get_automation_header(sys);

    // Init task list
    task_list_init(&automation->tasks);
    
    // Iter over the task raw functions
    automation_task_cfg_it_init(&task_it, &cfg->tasks);
    
    while(task_it.next(&task_it)) {
        if (task_it.get(&task_it, &raw_task_curr)) {
            code = task_push(&automation->tasks, raw_task_curr);

            if(code) {
                snprintf(err_msg, 256, "The automation system reached the limit of tasks.");
                sys_push_error(sys, ERR_REACHED_AUTOMATION_TASKS_LIMIT, err_msg);
                return ERR_REACHED_AUTOMATION_TASKS_LIMIT;
            }
        }
    }

    // Init data block list
    init_data_block_list(&automation->data_blocks);
    
    // Create the iterator
    automation_data_block_cfg_it_init(&db_it, &cfg->data_blocks);
    while(db_it.next(&db_it)) {
        if(db_it.get(&db_it, &db_size_curr)) {
            // We allocate memory to store the data block content
            void* db_base = sys_alloc(sys, *db_size_curr);
            
            // We do not have any more memory to store the data block content...
            if(db_base == NULL) {
                snprintf(err_msg, 256, "Cannot allocate more memory to create data block.");
                sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, err_msg);
                return ERR_NOT_ENOUGH_MEMORY_SPACE;            
            }

            code = data_block_push(&automation->data_blocks, db_base, *db_size_curr);
            
            if(code) {
                snprintf(err_msg, 256, "The automation system reached the limit of data blocks.");
                sys_push_error(sys, ERR_REACHED_AUTOMATION_DATA_BLOCK_LIMIT, err_msg);
                return ERR_REACHED_AUTOMATION_DATA_BLOCK_LIMIT;
            }
        }
    }
    // Everything went well !
    return 0;
}

int automation_system_step(struct System_t* sys) 
{
    int code;
    struct AutomationHeader_t* automation;
    struct AutomationTaskListIterator_t it;
    struct AutomationTask_t* curr;
    
    automation = get_automation_header(sys);

    it = task_list_iter(&automation->tasks);
    
    while(it.next(&it)) 
    {
        if (it.get(&it, &curr)) 
        {
            code = execute_task(sys, curr);
        
            if(code)
                return code;
        }

    }

    return 0;
}

int automation_system_init(struct System_t* sys, struct KernelgCfg_t* cfg) {
   return automation_system_init(sys, (struct AutomationCfg_t*) cfg);
}

