#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/net01.h"
void sys_net01_init(struct System_t * system) {
    sys.nb_blocks = 2;
    sys.data_blocks = (struct DataBlock_t *) malloc(sizeof(struct DataBlock_t) * 2);
    sys.data_blocks[0]->offset = 0;
    sys.data_blocks[1]->offset = 0;
}
void sys_net01_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 0);
    sys_net01_cpy_relay(plant, & sys);
    close_system(& sys);
}
void sys_net01_relay(struct Plant_t * plant, struct System_t * sys) {
    sys_net01_cpy_relay_DLNK1(plant, sys);
    sys_net01_cpy_relay_DLNK2(plant, sys);
}
void sys_net01_cpy_relay_DLNK1(struct Plant_t * sys, struct System_t * sys) {
    struct DataBlock_t idb;
    struct System_t other_sys;
    struct DataBlock_t other_idb;
    idb = open_data_block(sys, 0);
    other_sys = open_system(plant, 3);
    other_idb = open_data_block(& sys, 2);
    memcpy(idb.base, other_idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
    other_sys = open_system(plant, 4);
    other_idb = open_data_block(& sys, 1);
    memcpy(other_idb.base, idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
}
void sys_net01_cpy_relay_DLNK2(struct Plant_t * sys, struct System_t * sys) {
    struct DataBlock_t idb;
    struct System_t other_sys;
    struct DataBlock_t other_idb;
    idb = open_data_block(sys, 1);
    other_sys = open_system(plant, 4);
    other_idb = open_data_block(& sys, 2);
    memcpy(idb.base, other_idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
    other_sys = open_system(plant, 5);
    other_idb = open_data_block(& sys, 1);
    memcpy(other_idb.base, idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
}