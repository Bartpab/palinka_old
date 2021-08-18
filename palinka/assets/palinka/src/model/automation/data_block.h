/**
 * \file data_block.h
 * \brief Contains the data block API.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */


#ifndef __DATA_BLOCK_H__
#define __DATA_BLOCK_H__

#include <stddef.h>
#include "src/model/system/api.h"

#include "src/model/automation/api.h"

#define MAX_NUMBER_OF_DATA_BLOCKS 256

/*
* \struct AutomationDataBlock_t
* \brief A handler to a data block.
*/
struct AutomationDataBlock_t {
    size_t size; /*! Size of the data block */
    char* base; /*! Memory base of the data block */
};

/*
* \struct AutomationDataBlockList_t
* \brief A list of data block
*/
struct AutomationDataBlockList_t {
    struct AutomationDataBlock_t tail[MAX_NUMBER_OF_DATA_BLOCKS];
    struct AutomationDataBlock_t* head;
    struct AutomationDataBlock_t* limit;
};

/**
 * \brief Initialise a data block list.
 */
void init_data_block_list(struct AutomationDataBlockList_t* list);

/**
 * \brief Push a data block in the list.
 */
int data_block_push(struct AutomationDataBlockList_t* list, char* base, size_t size);

/**
 * \brief Open a data block
 * \param sys The automation system
 * \param db_id The data block identifier
 * \param db The handler of the data block
 * \return 0 if no error occured, else > 0 if an error occured.
 */
int data_block_open(struct System_t* sys, size_t db_id, struct AutomationDataBlock_t** db); 

/**
 * \brief Close the data block
 * \param db The handler of the data block
 * \return 0 if no error occured, else > 0 if an error occured.
 */
int close_data_block(struct AutomationDataBlock_t* db);

#endif