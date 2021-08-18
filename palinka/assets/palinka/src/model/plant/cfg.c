#include "src/model/plant/cfg.h"

int plant_cfg_init(struct PlantCfg_t* cfg, size_t system_capacity) 
{
    cfg->memory_size = 0;
    
    if(!sys_cfg_list_init(&cfg->systems, system_capacity))
        return 0;

    return 1;
}

void plant_cfg_delete(struct PlantCfg_t* cfg) 
{
    sys_cfg_list_delete(&cfg->systems);
}

int plant_cfg_add_sys(struct PlantCfg_t* plant_cfg, struct SystemCfg_t sys_cfg) 
{
    if(!sys_cfg_list_add(&plant_cfg->systems, sys_cfg))
        return 0;
    
    plant_cfg->memory_size += sys_cfg.base_cfg->memory_size;
}