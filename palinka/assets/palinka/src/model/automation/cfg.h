#include <stddef.h>

struct AutomationTaskCfg_t {
    void (**raws)(struct System_t*);
    size_t nb;
};

struct AutomationDataBlockCfg_t {
    size_t* sizes;
    size_t nb;
};

struct AutomationCfg_t {
    struct AutomationaskCfg_t tasks;
    struct AutomationDataBlockCfg_t data_blocks;
};