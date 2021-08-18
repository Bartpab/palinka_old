#include "src/model/automation/cfg.h"

void automation_task_cfg_it_init(struct AutomationTaskCfgIterator_t* it, struct AutomationTaskCfg_t* cfg) {
    it->curr = NULL;
    it->cfg = *cfg;
    it->next = automation_task_cfg_it_next;
    it->get = automation_task_cfg_it_get;
}

int automation_task_cfg_it_next(struct AutomationTaskCfgIterator_t* it) {
    if (it->curr == it->cfg.raws + it->cfg.cout) {
        return 0;
    }

    if(it->curr == NULL)
        it->curr = it->cfg.raws;
    else
        it->curr++;

    return 1;
}

int automation_task_cfg_it_get(struct AutomationTaskCfgIterator_t* it, void (**out)(struct System_t*)) {
    if(it->curr == NULL)
        return 0;
    
    *out = it->curr;
    return 1;
}

void automation_data_block_cfg_it_init(struct AutomationDataBlockCfgIterator_t* it, struct AutomationDataBlockCfg_t* cfg)
{
    it->curr = NULL;
    it->cfg = *cfg;
    it->next = automation_data_block_cfg_it_next;
    it->get = automation_data_block_cfg_it_get;
}

int automation_data_block_cfg_it_next(struct AutomationDataBlockCfgIterator_t* it)
{
    if (it->curr == it->cfg.sizes + it->cfg.cout) {
        return 0;
    }

    if(it->curr == NULL)
        it->curr = it->cfg.sizes;
    else
        it->curr++;

    return 1;
}

int automation_data_block_cfg_it_get(struct AutomationDataBlockCfgIterator_t* it, size_t** out)
{
    if(it->curr == NULL)
        return 0;
    
    *out = it->curr;
    return 1;
}