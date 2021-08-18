
#ifndef __SYSTEM_LIST_H__
#define __SYSTEM_LIST_H__

#include "src/model/system/container.h"
#include "src/model/system/accessor.h"

#include <stddef.h>

/**
 * \brief A list of systems
 */
struct SystemContainerList_t
{
    struct SystemContainer_t* tail;
    struct SystemContainer_t* head;
    struct SystemContainer_t* limit;
};

/**
 * \brief Initialise the list
 * 
 * Dynamic allocation of a list.
 * 
 * \param list The list
 * \param capacity The capacity of the list
 * \return 0 if succeeded, 1 if failed (alloc failed)
 */
int sys_list_init(struct SystemContainerList_t* list, size_t capacity);

/**
 * \brief Delete the list
 * 
 * \param list The list 
 */
void sys_list_delete(struct SystemContainerList_t* list);

/**
 * \brief Add a system to the list
 * 
 * \return 1 if succeeded, 0 if failed (no more space)
 */
int sys_list_add(struct SystemContainerList_t* list, struct System_t sys);

/**
 * \brief Get the system in the system by its id.
 * 
 * \eturn 1 if succeeded
 */
int sys_list_get(struct SystemContainerList_t* list, unsigned char sys_id, struct SystemAccessor_t* sys);

struct SystemContainerListIterator_t 
{
    struct SystemContainer_t* curr;
    struct SystemContainerList_t list;

    int (*next)(struct SystemContainerListIterator_t*);
    int (*get)(struct SystemContainerListIterator_t*, struct SystemAccessor_t*);
};

void sys_list_it_init(struct SystemContainerListIterator_t* it, struct SystemContainerList_t* list);
int sys_list_it_next(struct SystemContainerListIterator_t* it);
int sys_list_it_get(struct SystemContainerListIterator_t* it, struct SystemAccessor_t*);

#endif