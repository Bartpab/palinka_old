#include "src/model/system/cfg.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h> 

void sys_cfg_init(struct SystemCfg_t* sys_cfg, 
    const char* name, 
    struct CommonCfg_t* cfg, 
    size_t cfg_size, 
    int (*init_cbk)(struct System_t*, struct CommonCfg_t*), 
    int(*step_cbk)(struct System_t*)
    ) 
{
    snprintf(sys_cfg->name, SYSTEM_NAME_MAX_LENGTH, name);
    sys_cfg->base_cfg = malloc(cfg_size);
    
    memcpy(sys_cfg->base_cfg, cfg, cfg_size);
    sys_cfg->init_cbk = init_cbk;
    sys_cfg->step_cbk = step_cbk;
}

void sys_cfg_delete(struct SystemCfg_t* sys_cfg)
{
    if(sys_cfg->base_cfg == NULL)
        return;
    
    free(sys_cfg->base_cfg);
    sys_cfg->base_cfg = NULL;
}

int sys_cfg_list_init(struct SystemCfgList_t* list, size_t capacity) {
    list->tail = malloc(sizeof(struct SystemCfg_t) * capacity);
    
    if (list->tail == NULL)
        return 0;

    list->head = NULL;
    list->limit = list->tail + capacity - 1;
    return 1;
}

int sys_cfg_list_add(struct SystemCfgList_t* list, struct SystemCfg_t cfg) {
    if (list->head == list->limit)
        return 0;
    
    if (list->head == NULL)
        list->head = list->tail;
    else
        list->head++;
    
    *list->head = cfg;
    return 1;
}

void sys_cfg_list_delete(struct SystemCfgList_t* list) {
    struct SystemListCfgIterator_t it;
    struct SystemCfg_t* item;
    
    if (list->tail == NULL)
        return;

    sys_cfg_list_it_init(&it, list);

    while(it.next(&it)) {
        if (it.get(&it, &item)) {
            sys_cfg_list_delete(item);
        }
    }

    free(list->tail);
    list->tail = NULL;
}

void sys_cfg_list_it_init(struct SystemListCfgIterator_t* it, struct SystemCfgList_t* list) {
    it->curr = NULL;
    it->list = list;

    it->next = sys_cfg_list_it_next;
    it->get = sys_cfg_list_it_get;
}

int sys_cfg_list_it_next(struct SystemListCfgIterator_t* it) {
    if (it->curr = it->list->head)
        return 0;
    
    if(it->curr == NULL) 
        it->curr = it->list->tail;
    else
        it->curr++;

    return 1;
}

int sys_cfg_list_it_get(struct SystemListCfgIterator_t* it, struct SystemCfg_t** out) {
    if (it->curr == NULL)
        return 0;
    
    *out = it->curr;
    return 1;
}