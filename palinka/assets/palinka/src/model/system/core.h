/**
 * \file system.h
 * \brief Contains the system representation, and its API.
 * \author Gaël P.
 * \version 0.1
 * \date 06/08/2021
 */
#ifndef __SYSTEM_API_H__
#define __SYSTEM_API_H__

#include "src/model/system/cfg.h"
#include "src/model/error.h"
#include "src/utils/memory/alloc.h"

#include "src/model/device/core.h"

#include <stddef.h>

#define SYSTEM_NAME_MAX_LENGTH 256

/**
 * \struct System_t
 * \brief A handler to a simulated system.
 * 
 * Contains everything to manage the system, its memory (and size), the error (if any), and the hook functions (step)
 * 
 * When init a system, you must always perform the following operations in that order
 * - kernel_init(sys, sizeof(specific_header_t))
 * - <specific>_init(sys)
 * 
 * kernel_init will initialise everything kernel to a system such as the MMU, the DEV, etc and reserve space to put the specific_header_t.
 */
struct System_t {
    /*! Name of the system */
    char name[SYSTEM_NAME_MAX_LENGTH];

    /*! Memory base */
    void* base;         
    
    /*! Memory size */
    size_t memory_size;    
    
    /*! Physical devices */
    struct PhysicalDeviceList_t devices;

    /*! 
    * \brief Last known error, if a system-related functions returns an error code, the full error will be available here.
    *
    * Currently no error stack exist, this can managed in a future version 
    */
    struct Error_t err;     

    /*! 
    * Step function that will be executed when calling system_step 
    */
    int (*step)(struct System_t* system); 
};

/**
 * \brief Initialise the system
 */
int sys_init(struct System_t* sys, struct SystemCfg_t* cfg, struct Allocator_t* allocator);

/**
 * \brief Push an error.
 * 
 * If a system-related function fails, this function is used to push the related error so it can be retrieved and analysed/displayed.
 * The error is stored in a circular buffer and will remove old errors. 
 */
void sys_push_error(struct System_t* sys, const int code, const char* msg);

/**
 *  \brief Pop an error.
 * 
 * If a system-related function fails, this function is used to pop the related error from the system.
 * \param sys The related system
 * \param output The destination of the error (if returned value is 1)
 * \return 1 if an error is available, 0 if not error is available.
 */
int sys_pop_error(struct System_t* sys, struct Error_t* output);

/**
 * \brief System step function.
 * 
 * This will call the step function store in the system.
 * If an error occured (returned valued > 0), an error is pushed in the system's handler.
 * 
 * \return 0 if anything went well, > 0 if an error occured.
 */
int sys_step(struct System_t* sys);

/**
 * \brief System interrupt function
 * If an error occured (returned valued > 0), an error is pushed in the system's handler.
 * 
 * \return 0 if anything went well, > 0 if an error occured.
 */
int sys_interrupt(struct System_t* sys, unsigned char irq);

/**
 * \brief Send data to a physical device
 */
int sys_write_device(struct System_t* sys, size_t dev_id, unsigned char data);
#endif