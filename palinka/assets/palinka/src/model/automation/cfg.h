#ifndef __AUTOMATION_CFG_H__
#define __AUTOMATION_CFG_H__

#include <stddef.h>
#include "src/model/common/cfg.h"

struct AutomationTaskCfg_t {
    void (*raws)(struct System_t*);
    size_t cout;
};

struct AutomationTaskCfgIterator_t {
    void (*curr)(struct System_t*);
    struct AutomationTaskCfg_t cfg;

    int (*next)(struct AutomationTaskCfgIterator_t*);
    int (*get)(struct AutomationTaskCfgIterator_t*, void (**curr)(struct System_t*));
};

void automation_task_cfg_it_init(struct AutomationTaskCfgIterator_t* it, struct AutomationTaskCfg_t* cfg);
int automation_task_cfg_it_next(struct AutomationTaskCfgIterator_t* it);
int automation_task_cfg_it_get(struct AutomationTaskCfgIterator_t* it, void (**out)(struct System_t*));

struct AutomationDataBlockCfg_t {
    size_t* sizes;
    size_t cout;
};

struct AutomationDataBlockCfgIterator_t {
    size_t* curr;
    struct AutomationDataBlockCfg_t cfg;

    int (*next)(struct AutomationDataBlockCfgIterator_t*);
    int (*get)(struct AutomationDataBlockCfgIterator_t*, size_t** out);
};

/**
 * \brief Initialise an iterator over the list of data block configurations.
 */
void automation_data_block_cfg_it_init(struct AutomationDataBlockCfgIterator_t* it, struct AutomationDataBlockCfg_t* cfg);
/**
 * \brief Fetch the next element in the list.
 * 
 * \param it The iterator
 * \return 1 if another element was fetched, 0 else.
 */ 
int automation_data_block_cfg_it_next(struct AutomationDataBlockCfgIterator_t* it);

/**
 * \brief Get the element behind the current iterator state.
 * 
 * \param it The iterator
 * \param out The output
 * \return 1 if an element exists, 0 else.
 */ 
int automation_data_block_cfg_it_get(struct AutomationDataBlockCfgIterator_t* it, size_t** out);

struct AutomationCfg_t {
    struct CommonCfg_t common;
    struct AutomationTaskCfg_t tasks;
    struct AutomationDataBlockCfg_t data_blocks;
};

#endif