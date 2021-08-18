/**
 * \file task.c
 * \brief Implements the task API.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#include "src/model/automation/task.h"

int execute_task(struct System_t* sys, struct AutomationTask_t* task) 
{
    task->raw(sys);
    return 0;
}

void task_list_init(struct AutomationTaskList_t* list) {
    list->limit = list->tail + MAX_NUMBER_OF_TASKS - 1;
    list->head = NULL; 
}

struct AutomationTaskListIterator_t task_list_iter(struct AutomationTaskList_t* list) {
    struct AutomationTaskListIterator_t it;
    task_list_init_it(list, &it);
    return it;
}

int task_push(struct AutomationTaskList_t* list, void (*raw)(struct System_t*))
{
   if(list->head >= list->limit) {
       return 1;
   }

   if (list->head == NULL)
       list->head = list->tail;
   else 
       list->head++;

   list->head->raw = raw;
   list->head->is_active = 1;
   
   return 0;
}

void task_list_init_it(struct AutomationTaskList_t* list, struct AutomationTaskListIterator_t* it) 
{
    it->curr = NULL;
    it->list = list;
    it->next = task_list_it_next;
    it->get = task_list_it_get;
}

int task_list_it_next(struct AutomationTaskListIterator_t* it) 
{
    if(it->curr >= it->list->head) 
        return 0;

    if(it->curr == NULL)
        it->curr = it->list->tail;
    else   
        it->curr++;
    
    return 1;
}

int task_list_it_get(struct AutomationTaskListIterator_t* it, struct AutomaationTask_t** out)
{
    if(it->curr == NULL)
        return 0;
    
    *out = it->curr;
    
    return 1;
}