#include "src/model/automation/task.h"
#include "src/model/automation/data_block.h"

struct AutomationHeader_t {
    struct AutomationTaskList_t tasks;
    struct AutomationDataBlockList_t data_blocks;
};
