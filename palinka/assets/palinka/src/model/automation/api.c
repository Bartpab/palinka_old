#include <stddef.h>

#include "src/model/automation/api.h"
#include "src/model/automation/cfg.h"
#include "src/model/automation/header.h"
#include "src/model/automation/task.h"
#include "src/model/common/header.h"
#include "src/model/common/init.h"
#include "src/model/system.h"
#include "src/model/error.h"

int init_automation_system(struct System_t* sys, struct AutomationSystemCfg_t* cfg) {
    int code;

    automation = get_automation_header(sys);

    // Init task list
    init_task_list(&automation->tasks);
    for (int i = 0; i < cfg->tasks.nb; i++) {
        code = push_task(&automation->tasks, cfg->tasks->raws[i]);

        if(code) {
            char err_msg[256];
            snprintf(err_msg, 256, "The automation system reached the limit of tasks.");
            sys_push_error(sys, ERR_REACHED_AUTOMATION_TASKS_LIMIT, err_msg);
            return ERR_REACHED_AUTOMATION_TASKS_LIMIT;
        }
    }

    // Init data block list
    init_data_block_list(&automation->data_blocks);
    
    for(int i = 0; i < cfg->data_blocks.nb; i++) {
        size_t db_size = cfg->data_blocks.sizes[i];

        // We allocate memory to store the data block content
        char* db_base = sys_alloc(sys, db_size);
        
        // We do not have any more memory to store the data block content...
        if(db_base == NULL) {
            char err_msg[256];
            snprintf(err_msg, 256, "Cannot allocate more memory to create data block.");
            sys_push_error(sys, ERR_NOT_ENOUGH_MEMORY_SPACE, err_msg);
            return ERR_NOT_ENOUGH_MEMORY_SPACE;            
        }

        code = push_data_block(&automation->data_blocks, db_base, db_size);
        
        if(code) {
            char err_msg[256];
            snprintf(err_msg, 256, "The automation system reached the limit of data blocks.");
            sys_push_error(sys, ERR_REACHED_AUTOMATION_DATA_BLOCK_LIMIT, err_msg);
            return ERR_REACHED_AUTOMATION_DATA_BLOCK_LIMIT;
        }
    }

    // Everything went well !
    return 0;
}

struct AutomationHeader_t* get_automation_header(struct System_t* sys) 
{
    struct CommonHeader_t* common;
    common = (struct CommandHeader_t*) sys->base;

    struct AutomationHeader_t* automation;
    automation = (struct AutomationHeader_t*) common->next;
    return automation;
}

int step_automation_system(struct System_t* sys) 
{
    int code;
    struct AutomationHeader_t* automation;
    struct AutomationTaskListIterator_t it;
    
    automation = get_automation_header(sys);

    it = iter_task_list(&automation->tasks);
    
    while(it.next(&it)) {
        code = execute_task(sys, it->curr);
        
        if(code)
            return code;
    }

    return 0;
}