#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/NET01.h"
void sys_NET01_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 0);
    sys_NET01_copy_relay(plant, & sys);
    close_system(& sys);
}
void sys_NET01_relay(struct Plant_t * plant, struct System_t * sys) {
    sys_NET01_cpy_relay_0(plant, sys);
    sys_NET01_cpy_relay_1(plant, sys);
}
void sys_NET01_cpy_relay_0(struct Plant_t * sys, struct System_t * sys) {
    struct DataBlock_t idb;
    struct System_t other_sys;
    struct DataBlock_t other_idb;
    idb = open_data_block(sys, 0);
    other_sys = open_system(plant, 1);
    other_idb = open_data_block(& sys, 1);
    memcpy(idb.base, other_idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
    other_sys = open_system(plant, 2);
    other_idb = open_data_block(& sys, 4);
    memcpy(other_idb.base, idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
}
void sys_NET01_cpy_relay_1(struct Plant_t * sys, struct System_t * sys) {
    struct DataBlock_t idb;
    struct System_t other_sys;
    struct DataBlock_t other_idb;
    idb = open_data_block(sys, 1);
    other_sys = open_system(plant, 2);
    other_idb = open_data_block(& sys, 5);
    memcpy(idb.base, other_idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
    other_sys = open_system(plant, 3);
    other_idb = open_data_block(& sys, 1);
    memcpy(other_idb.base, idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
}