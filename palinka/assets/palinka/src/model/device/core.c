#include "src/model/device/core.h"

int phy_dev_list_get(struct PhysicalDeviceList_t* list, unsigned char id, struct PhysicalDevice_t** out)
{
    if(list->tail + id > list->head) 
        return 0;
    
    *out = list->tail + id;

    return 1;
}

int phy_dev_list_add(struct PhysicalDeviceList_t* list, struct PhysicalDevice_t dev)
{
    if(list->head == list->limit)
        return 0;
    
    if(list->head == NULL)
        list->head = list->tail;
    else
        list->head++;
    
    *(list->head) = dev;
    
    return 1;
}

int phy_dev_list_init(struct PhysicalDeviceList_t* list, size_t capacity)
{
    list->tail = (struct PhysicalDevice_t*) malloc(sizeof(struct PhysicalDevice_t) * capacity);
    list->head = NULL;
    
    if(list->tail == NULL)
        return 0;

    list->limit = list->tail + capacity - 1;
    
    return 1;
}

void phy_dev_list_delete(struct PhysicalDeviceList_t* list)
{
    if(list->tail == NULL)
        return;

    free(list->tail);
    list->tail = list->head = list->limit = NULL;
}
