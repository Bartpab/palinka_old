/**
 * \file task.h
 * \brief Contains the task API.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#ifndef __TASK_H__
#define __TASK_H__

#include <stddef.h>
#include "src/model/system/core.h"

#define MAX_NUMBER_OF_TASKS 256
/**
 * \struct AutomationTask_t 
 * \brief Represents a task executed by the automation system.
 */
struct AutomationTask_t {
    void (*raw)(struct System_t*); /*! The C-function containing the task program */
    char is_active; /*! 0: deactivated, 1: activated */
};

/**
 * \brief Execute the task on the system.
 * \return 0 if no error occured, else > 0.
 */
int execute_task(struct System_t* sys, struct AutomationTask_t* task);

/**
 * \struct AutomationTaskList_t
 * \brief Represents a list of automation tasks.
 */
struct AutomationTaskList_t {
    struct AutomationTask_t tail[MAX_NUMBER_OF_TASKS];
    struct AutomationTask_t* head;
    struct AutomationTask_t* limit;
};

/**
 * \brief Initialise the list
 */
void task_list_init(struct AutomationTaskList_t* list);

/**
 * \brief Return an iterator for the list.
 * \return The iterator
 */
struct AutomationTaskListIterator_t task_list_iter(struct AutomationTaskList_t* list);

/**
 * \brief Add a task to the list.
 * \return 1 if no element can be added to the list, 0 else.
 */
int task_push(struct AutomationTaskList_t* list, void (*raw)(struct System_t*));

/**
* \struct AutomationTaskListIterator_t
* \brief An iterator for an automation task list.
*/
struct AutomationTaskListIterator_t {
    struct AutomationTask_t* curr;
    struct AutomationTaskList_t* list;

    int (*next)(struct AutomationTaskListIterator_t* it);
    int (*get)(struct AutomationTaskListIterator_t*, struct AutomationTask_t**);
};

/**
 * \brief Initialise the iterator
 */
void task_list_init_it(struct AutomationTaskList_t* list, struct AutomationTaskListIterator_t* it);

/**
 * \brief Get the next element on the list.
 * \return 0 if the iterator is exhausted, 1 if an element has been fetched.
 */
int task_list_it_next(struct AutomationTaskListIterator_t* it);

int task_list_it_get(struct AutomationTaskListIterator_t* it, struct AutomaationTask_t** out);
#endif