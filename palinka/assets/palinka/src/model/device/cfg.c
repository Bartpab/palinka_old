#include "src/model/device/cfg.h"

int phy_dev_cfg_list_init(struct PhysicalDeviceCfgList_t *list, size_t capacity)
{
    list->tail = malloc(sizeof(struct PhysicalDeviceCfg_t) * capacity);
    
    if (list->tail == NULL)
        return 0;

    list->head = NULL;
    list->limit = list->tail + capacity - 1;

    return 1;
}

int phy_dev_cfg_list_add(struct PhysicalDeviceCfgList_t *list, struct PhysicalDeviceCfg_t cfg)
{
    if(list->head == list->limit)
        return 0;

    if(list->head == NULL)
        list->head = list->tail;
    else
        list->head++;

    *list->head = cfg;
    return 1;
}

void phy_dev_cfg_list_delete(struct PhysicalDeviceCfgList_t *list)
{
    struct PhysicalDeviceCfgListIterator_t it;
    struct PhysicalDeviceCfg_t* el;

    phy_dev_cfg_list_it_init(&it, list);
    
    while(it.next(&it)) 
    {
        if(it.get(&it, &el)) 
        {
            phy_dev_cfg_delete(el);
        }
    }

    free(list->tail);
    list->head = list->tail = list->limit = NULL;
}

void phy_dev_cfg_list_it_init(struct PhysicalDeviceCfgListIterator_t* it, struct PhysicalDeviceCfgList_t *list)
{
    it->curr = NULL;
    it->list = list;

    it->next = phy_dev_cfg_list_it_next;
    it->get = phy_dev_cfg_list_it_get;
}

int phy_dev_cfg_list_it_next(struct PhysicalDeviceCfgListIterator_t* it)
{
    if(it->curr == it->list->head)
        return 0;

    if (it->curr == NULL)
        it->curr = it->list->head;
    else 
        it->curr++;
    
    return 1;
}

int phy_dev_cfg_list_it_get(struct PhysicalDeviceCfgListIterator_t* it, struct PhysicalDeviceCfg_t** out)
{
    if(it->curr == NULL)
        return 0;
    
    *out = it->curr;
    return 1;
}