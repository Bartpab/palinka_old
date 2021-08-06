/**
 * \file data_block.c
 * \brief Implemens the data block API.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */


#include "src/model/automation/data_block.h"

void init_data_block_list(struct AutomationDataBlockList_t* list) 
{
    list->limit = list->arena[MAX_NUMBER_OF_DATA_BLOCKS];
    list->head = NULL; 
}

int push_data_block(struct AutomationDataBlockList_t* list, char* base, size_t size)
{
   if(list->head == list->limit) {
       return 1;
   }

   if (list->head == NULL) {
       list->head = list->arena;
   } else {
       list->head++;
   }

   *list->head->size = size;
   list->head->base = base;
   
   return 0;
}

int open_data_block(struct System_t* sys, size_t db_id, struct AutomationDataBlock_t** db)
{
    struct AutomationDataBlock_t* cursor;

    // Get the list of data blocks.
    struct AutomationHeader_t* header = get_automation_header(sys);
    cursor = header->data_blocks->arena[db_id];

    // We overshooted
    if(cursor > header->data_blocks->head) {
        char err_msg[256];
        snprintf(err_msg, 256, "The data block #%d is not allocated.", db_id);
        sys_push_error(sys, ERR_UNALLOCATED_DATA_BLOCK, err_msg);
        return ERR_UNALLOCATED_DATA_BLOCK; 
    }
    
    // We copy the value
    *db = cursor;
    return 0;
}

int close_data_block(struct AutomationDataBlock_t* db)
{
    return 0;
}