#include "src/model/plant/api.h"
#include "src/utils/alloc.h"
#include <stdlib.h>
#include <stdio.h>

int plant_init(struct Plant_t* plant, struct PlantCfg_t* cfg) 
{
    struct Error_t err; int code; char err_msg[ERROR_MSG_MAX_SIZE];
    struct System_t sys;
    struct SystemListCfgIterator_t sys_cfg_it;
    struct SystemCfg_t* sys_cfg;
    struct Allocator_t allocator;
    
    plant->base = malloc(cfg->memory_size);
    allocator = create_static_allocator(plant->base, cfg->memory_size);

    if (!plant->base)
    {
        snprintf(err_msg, ERROR_MSG_MAX_SIZE, "Cannot add anymore system to the plant.");
        plant_push_error(plant, ERR_NOT_ENOUGH_MEMORY_SPACE, err_msg);
        return ERR_REACHED_SYSTEMS_LIMIT;
    }
    
    // Get an iterator over system configurations
    sys_cfg_list_it_init(&sys_cfg_it, &cfg->systems);

    while(sys_cfg_it.next(&sys_cfg_it)) 
    {
        if(sys_cfg_it.get(&sys_cfg_it, &sys_cfg)) 
        {
            code = sys_init(&sys, sys_cfg, &allocator);
            
            // Something went wrong while initialising the system, we pop the error and push it at the plant level
            if (code > 0) 
            {               
                if (sys_pop_error(&sys, &err)) 
                {
                    snprintf(&err_msg, ERROR_MSG_MAX_SIZE, "%s - %s", sys.name, err.msg);
                    plant_push_error(plant, err.code, err_msg);
                }

                return code;
            }   

            // Add the system to the plant, if failed, return an error and stop the initialisation.
            if(!sys_list_add(&plant->systems, sys)) 
            {
                snprintf(err_msg, ERROR_MSG_MAX_SIZE, "Cannot add anymore system to the plant.");
                plant_push_error(plant, ERR_REACHED_SYSTEMS_LIMIT, err_msg);
                return ERR_REACHED_SYSTEMS_LIMIT;
            }
        }
    }

    return 0;
}

int plant_get_system(struct Plant_t* plant, unsigned char sys_id, struct SystemAccessor_t* sys_acc)
{
    return sys_list_get(&plant->systems, sys_id, sys_acc);
}


int plant_step(struct Plant_t * plant)
{
    int code;
    struct SystemContainerListIterator_t it;
    struct System_t *sys;
    
    // Initialise the iterator
    sys_list_it_init(&it, &plant->systems); 

    // Loop through all systems
    while(it.next(&it)) 
    {
        if(it.get(&it, &sys)) 
        {
            code = sys_step(sys);
            
            if (code > 0) {
                struct Error_t err;
                char err_msg[256];

                if (sys_pop_error(&sys, &err)) 
                {
                    snprintf(&err_msg, 256, "%s - %s", sys->name, err.msg);
                    plant_push_error(plant, err.code, err_msg);
                }

                return code;
            }   
        }
    }

    return 0;
}


void plant_push_error(struct Plant_t* plant, const int code, const char* msg) 
{
    write_error(&plant->err, code, msg);
}

/**
 *  \brief Pop an error.
 */
int plant_pop_error(struct Plant_t* plant, struct Error_t* output) 
{
    *output = plant->err;
    write_error(&plant->err, 0, "");
}
