#ifndef __PLANT_CFG_H__
#define __PLANT_CFG_H__

#include "src/model/system/cfg.h"

struct PlantCfg_t 
{
    size_t memory_size;
    struct SystemCfgList_t systems;
};

/**
 * \brief Initialise the plant configuration
 * 
 * \return 1 if succeeded, 0 if failed (could not initialise list of system configurations).
 */
int plant_cfg_init(struct PlantCfg_t* cfg, size_t system_capacity);

/**
 * \brief Delete the plant configuration
 */
void plant_cfg_delete(struct PlantCfg_t* cfg);

/**
 * \brief Add a system configuration in the plant configuration
 * 
 * \return 1 if succeeded, 0 if failed (no more space).
 */
int plant_cfg_add_sys(struct PlantCfg_t* plant_cfg, struct SystemCfg_t sys_cfg);

#endif