/**
 * \file plant.h
 * \brief Contains the plant representation, and its API.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */

#ifndef __PLANT_H__
#define __PLANT_H__

#include "src/model/system/list.h"
#include "src/model/plant/cfg.h"
#include "src/model/error.h"

/**
* \struct Plant_t
* \brief A handler to the simulated plant.
*/
struct Plant_t {
    struct SystemContainerList_t systems;
    struct Error_t err; 
};

///////////
/// API ///
///////////

/**
 * \brief Initialise a plant simulation.
 */
int plant_init(struct Plant_t* plant, struct PlantCfg_t* cfg);

/**
 * \brief Retrieve an accessor the system
 */
int plant_get_system(struct Plant_t* plant, unsigned char sys_id, struct SystemAccessor_t* sys_acc);

/**
 * \brief Delete the plant simulation
 */
void plant_delete(struct Plant_t* plant);

/**
 * \brief Execute a step of the simulation for the plant.
 */
int plant_step(struct Plant_t * plant);

/**
 * \brief Push an error.
 */
void plant_push_error(struct Plant_t* sys, const int code, const char* msg);

/**
 *  \brief Pop an error.
 */
int plant_pop_error(struct Plant_t* plant, struct Error_t* output);

#endif