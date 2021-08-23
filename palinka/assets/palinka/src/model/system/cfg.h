#ifndef __SYSTEM_CFG_H__
#define __SYSTEM_CFG_H__

#include "src/model/kernel/cfg.h"
#include "src/model/device/cfg.h"
#include "src/model/system/core.h"

/**
 * \brief System configuration
 */
struct SystemCfg_t 
{
    char name[SYSTEM_NAME_MAX_LENGTH];
    size_t memory_size;

    struct KernelCfg_t* base_cfg;

    /*! Physical device configurations */
    struct PhysicalDeviceCfgList_t pdevices;

    int (*init)(struct System_t*);
    int (*step)(struct System_t*);
};

void sys_cfg_init(struct SystemCfg_t* sys_cfg, const char* name, 
    struct KernelCfg_t* cfg, size_t cfg_size, 
    int (*init)(struct System_t*, struct KernelCfg_t*), 
    int(*step)(struct System_t*)
);
void sys_cfg_delete(struct SystemCfg_t* sys_cfg);

/**
 * \brief A list of system configurations
 */
struct SystemCfgList_t {
    struct SystemCfg_t* tail;
    struct SystemCfg_t* head;
    struct SystemCfg_t* limit;
};

/**
 * \brief Initialise the list of system configurations
 * 
 * \return 1 if succeeded, 0 if failed.
 */
int sys_cfg_list_init(struct SystemCfgList_t* list, size_t capacity);
int sys_cfg_list_add(struct SystemCfgList_t* list, struct SystemCfg_t cfg);
void sys_cfg_list_delete(struct SystemCfgList_t* list);

/**
 * \brief An iterator over a list of system configurations.
 */
struct SystemListCfgIterator_t {
    struct SystemCfg_t* curr;
    struct SystemCfgList_t* list;

    int (*next)(struct SystemListCfgIterator_t*);
    int (*get)(struct SystemListCfgIterator_t*, struct SystemCfgList_t**);
};

/**
 * \brief Initialise the iterator.
 */
void sys_cfg_list_it_init(struct SystemListCfgIterator_t* it, struct SystemCfgList_t* list);

/**
 * \brief Get the next element of the iterator
 */
int sys_cfg_list_it_next(struct SystemListCfgIterator_t* it);

/**
 * \brief Return the current element held by the iterator.
 */
int sys_cfg_list_it_get(struct SystemListCfgIterator_t* it, struct SystemCfg_t** out);

#endif