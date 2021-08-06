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

void init_task_list(struct AutomationTaskList_t* list) {
    list->limit = list->arena[MAX_NUMBER_OF_TASKS];
    list->head = NULL; 
}

struct AutomationTaskListIterator_t iter_task_list(struct AutomationTaskList_t* list) {
    struct AutomationTaskListIterator_t it;
    init_task_list_it(list, &it);
    return it;
}

int push_task(struct AutomationTaskList_t* list, void (*raw)(struct System_t*))
{
   if(list->head == list->limit) {
       return 1;
   }

   if (list->head == NULL) {
       list->head = list->arena;
   } else {
       list->head++;
   }

   *list->head->raw = task;
   list->head->is_active = 1;
   
   return 0;
}

void init_task_list_it(struct AutomationTaskList_t* list, struct AutomationTaskListIterator_t* it) 
{
    it->curr = list->arena;
    it->limit = list->head;
    it->next = next_task_list_it;
}

int next_task_list_it(struct AutomationTaskListIterator_t* it) 
{
    if (it->curr == NULL)
        return 0;
    
    if(it->curr == it->limit) 
        return 0;
    
    it->curr++;
    return 1;
}
