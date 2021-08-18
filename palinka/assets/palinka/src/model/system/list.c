#include "src/model/system/list.h"

int sys_list_create(struct SystemContainerList_t* list, size_t size) 
{
    list->tail = (struct SystemContainer_t*) malloc(sizeof(struct SystemContainer_t) * size);

    if(list->tail == NULL)
        return 1;

    list->head = NULL;
    list->limit = list->tail + size - 1;

    return 0;
}

void sys_list_delete(struct SystemContainerList_t* list) 
{
    if(list->tail == NULL)
        return;
        
    free(list->tail);
    list->tail = list->head = list->limit = NULL;
}

int sys_list_add(struct SystemContainerList_t* list, struct System_t sys) {
    if(list->head == list->limit)
        return 0;
    
    if(list->head == NULL)
        list->head = list->tail;
    else
        list->head++;
    
    list->head->sys = sys;
    return 1;
}

int sys_list_get(struct SystemContainerList_t* list, unsigned char sys_id, struct SystemAccessor_t* sys)
{
    if(list->tail + sys_id > list->head) 
    {
        return 0;
    }

    sys->container = (list->tail + sys_id);
    return 1;
}

void sys_list_it_init(struct SystemContainerListIterator_t* it, struct SystemContainerList_t* list) 
{
    it->curr = NULL;
    it->list = *list;

    it->next = sys_list_it_next;
    it->get = sys_list_it_get;
}

int sys_list_it_next(struct SystemContainerListIterator_t* it) {
    if(it->curr == it->list.limit) 
        return 0;

    if(it->curr == NULL)
        it->curr = it->list.tail;
    
    it->curr++;
    return 1;
}

int sys_list_it_get(struct SystemContainerListIterator_t* it, struct SystemAccessor_t* out)
{
    if(it->curr == NULL)
        return 0;
    
    out->container = it->curr;
    return 1;
}   